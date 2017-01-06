# Copyright 2016 Curtis Sand <curtissand@gmail.com>
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
"""Squadron Config File API."""

import os
from configparser import SafeConfigParser
from configparser import ExtendedInterpolation
from enum import Enum


class GeneralOpts(Enum):
    """Options for the General Section."""
    tmp_dir = os.path.join(os.environ.get('HOME', '/tmp/'), 'www')
    output_dir = os.path.join(tmp_dir, 'output')
    staging_dir = os.path.join(tmp_dir, 'staging')
    enabled_tasks = ''


class Sections(Enum):
    """The sections of the config file."""
    general = GeneralOpts


class ConfigFile(object):
    """Config File API for Squadron."""

    default_path = os.path.abspath('./squadron.cfg')

    def __init__(self, filename):
        self.filename = filename
        self.parser = SafeConfigParser(interpolation=ExtendedInterpolation())
        self.loaded = False

    def set_general_defaults(self):
        """Add default values to the parser for the general section."""
        key = Sections.general.name
        self.parser[key] = {}
        for opt in GeneralOpts:
            self.parser[key][opt.name] = opt.value

    def load(self):
        """Load the configuration file into memory."""
        self.set_general_defaults()
        self.parser.read(self.filename)
        self.loaded = True

    def get(self, *args, **kwargs):
        """Wrapper to simplify calls to self.parser.get()."""
        return None if not self.parser else self.parser.get(*args, **kwargs)

    def default_config(self):
        """Return the string of an empty, default config file."""
        for section in Sections:
            default = "[%s]\n" % section.name
            for option in section.value:
                default += "%s: %s\n" % (option.name, option.value)
            default += "\n"
        return default

    @property
    def enabled_tasks(self):
        """Retrieve a list of the enabled tasks from the config file."""
        enabled = self.get(Sections.general.name,
                           GeneralOpts.enabled_tasks.name)
        return [task for task in str(enabled).split(' ')
                if task != '']

    @property
    def tmp_dir(self):
        """The temporary directory to use for the squadron run."""
        return self.get(Sections.general.name,
                        GeneralOpts.tmp_dir.name)

    @property
    def output_dir(self):
        """The output directory to use for the finished product."""
        return self.get(Sections.general.name,
                        GeneralOpts.output_dir.name)

    @property
    def staging_dir(self):
        """The staging directory to use for the squadron run."""
        return self.get(Sections.general.name,
                        GeneralOpts.staging_dir.name)

    def print_default_config(self, tasks):
        """Print the default config example including stubs for each task."""
        print(self.default_config)
        for task in tasks.values():
            task_obj = task(config_file=self)
            print(task_obj.default_config)
