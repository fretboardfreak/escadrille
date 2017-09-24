# Copyright 2016-2017 Curtis Sand <curtissand@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Escadrille Config File API."""

import os
from configparser import SafeConfigParser
from configparser import ExtendedInterpolation
from enum import Enum

from .verbosity import dprint


class GeneralOpts(Enum):
    """Options for the General Section."""

    tmp_dir = '/tmp/escadrille'
    output_dir = os.path.join(tmp_dir, 'output')
    staging_dir = os.path.join(tmp_dir, 'staging')
    date_format = '%Y-%m-%d %H:%M'
    enabled_tasks = []


class Sections(Enum):
    """The sections of the config file."""

    general = GeneralOpts


class ConfigFile(object):
    """Config File API for Escadrille."""

    default_path = os.path.abspath('./escadrille.cfg')
    list_sep = ' '
    indent = '  '
    msg_template = '%s%s=%s\n'

    def __init__(self, filename=None):
        """Setup instance vars for ConfigFile objects."""
        self.filename = self.default_path
        if filename is not None:
            self.filename = filename
        self.parser = None
        self.loaded = False

    def set_parser_general_defaults(self):
        """Add default values to the parser for the general section."""
        key = Sections.general.name
        self.parser[key] = {}
        for opt in GeneralOpts:
            if isinstance(opt.value, list):
                self.parser[key][opt.name] = self.list_sep.join(opt.value)
            else:
                self.parser[key][opt.name] = opt.value

    def load(self):
        """Load the configuration file into memory."""
        if self.filename is not None:
            self.parser = SafeConfigParser(
                interpolation=ExtendedInterpolation())
            self.set_parser_general_defaults()
            if not os.path.exists(self.filename):
                dprint('%s: given config file "%s" could not be loaded.'
                       'No config file loaded. Defaults loaded.' %
                       (self.__class__.__name__, self.filename))
            else:
                self.parser.read(self.filename)
        self.loaded = True

    @property
    def default_config(self):
        """Return the string of an empty, default config file."""
        for section in Sections:
            default = "[%s]\n" % section.name
            for option in section.value:
                if isinstance(option.value, list):
                    default += self.msg_template % (
                        self.indent, option.name,
                        self.list_sep.join(option.value))
                else:
                    default += self.msg_template % (self.indent, option.name,
                                                    option.value)
            default += "\n"
        return default

    def print_default_config(self, tasks):
        """Print the default config example including stubs for each task."""
        print(self.default_config)
        for task in tasks.values():
            task_obj = task(config_file=self)
            print(task_obj.default_config)

    def get(self, section, option, *args, **kwargs):
        """Wrapper to simplify calls to self.parser.get."""
        if not self.parser:
            return None
        if (self.parser.has_section(section) and
                option in self.parser.options(section)):
            return self.parser.get(section, option, *args, **kwargs)

    def getboolean(self, section, option, *args, **kwargs):
        """Wrapper to simplify calls to self.parser.get()."""
        if not self.parser:
            return None
        if (self.parser.has_section(section) and
                option in self.parser.options(section)):
            return self.parser.getboolean(section, option, *args, **kwargs)

    def has_section(self, section):
        """Wrapper to simplify calls to self.parser.has_section."""
        if not self.parser:
            return False
        return self.parser.has_section(section)

    def section(self, section):
        """Helper method to simplify retrieving config sections for Tasks."""
        return None if not self.parser else self.parser[section]

    @property
    def enabled_tasks(self):
        """Retrieve a list of the enabled tasks from the config file."""
        enabled = self.get(Sections.general.name,
                           GeneralOpts.enabled_tasks.name)
        if enabled is None:
            return GeneralOpts.enabled_tasks.value
        return [task for task in str(enabled).split(self.list_sep)
                if task != '']

    @property
    def tmp_dir(self):
        """The temporary directory to use for the escadrille run."""
        tmp_dir = self.get(Sections.general.name,
                           GeneralOpts.tmp_dir.name)
        return tmp_dir if tmp_dir is not None else GeneralOpts.tmp_dir.value

    @property
    def output_dir(self):
        """The output directory to use for the finished product."""
        output_dir = self.get(Sections.general.name,
                              GeneralOpts.output_dir.name)
        default = GeneralOpts.output_dir.value
        return output_dir if output_dir is not None else default

    @property
    def staging_dir(self):
        """The staging directory to use for the escadrille run."""
        staging_dir = self.get(Sections.general.name,
                               GeneralOpts.staging_dir.name)
        default = GeneralOpts.staging_dir.value
        return staging_dir if staging_dir is not None else default

    @property
    def date_format(self):
        """Retrieve the configured date format string.

        The provided string must be compatible with ``time.strftime``.
        """
        date_format = self.get(Sections.general.name,
                               GeneralOpts.date_format.name)
        default = GeneralOpts.date_format.value
        return date_format if date_format is not None else default

    def get_task_name(self, tag):
        """Retrieve the task name from the section with the given tag."""
        name_key = "task"
        return self.get(tag, name_key)
