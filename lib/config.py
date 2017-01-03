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
    output_dir = os.environ.get('HOME', '/tmp/')
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

    def write_default_config(self):
        """Write an empty, default config file."""
        default_parser = SafeConfigParser(interpolation=ExtendedInterpolation)
        for section in Sections:
            default_parser.add_section(section.name)
            if not section.value:
                continue
            for option in section.value:
                default_parser.set(section.name, option.name, option.value)

        with open(self.filename, 'w') as fout:
            default_parser.write(fout)

    @property
    def enabled_tasks(self):
        """Retrieve a list of the enabled tasks from the config file."""
        enabled = self.parser.get(Sections.general.name,
                                  GeneralOpts.enabled_tasks.name)
        return [task for task in str(enabled).split(',')
                if task != '']
