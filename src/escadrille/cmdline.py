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
"""Library of command line tools for Escadrille Automation."""

import os
import argparse
import errno

from escadrille.config import ConfigFile
from escadrille.tasks import load_tasks

from escadrille.verbosity import DebugAction, VerboseAction


class InterfaceCore(object):
    """A base class for mixins that can add features to the UserInterface."""
    def build(self):
        """Construct the self.parser object."""
        pass

    def validate_args(self, args):
        """Validate the provided options meet requirements."""
        pass


class ConfigMixin(InterfaceCore):
    """Mixin class to add options for the configuration file."""
    def build(self):
        """Add config file options to the parser."""
        self.parser.add_argument(
            '-c', '--config', action='store', dest='config',
            default=None,
            help='Specify the config file to use.')
        self.parser.add_argument(
            '--default-config', action='store_true', dest='default_config',
            default=False, help='Print a default config section and exit.')
        self.parser.add_argument(
            '--debug-config', action='store_true', dest='debug_config',
            default=False, help='Debug the config file instead of running '
            'escadrille tasks.')
        super().build()

    def validate_args(self, args):
        """If provided, ensure that the config file path exists."""
        if args.config is not None and not os.path.exists(args.config):
            raise FileNotFoundError(errno.ENOENT, "Config File not found",
                                    args.config)
        super().validate_args(args)

    def print_config_debug(self, options):
        """A procedure to parse and help identify issues with config files."""
        print('cmdline args: %s' % options)
        print('Parsing Config File...')
        config_file = ConfigFile(options.config)
        config_file.load()
        print('Config Sections: %s' % config_file.parser.sections())
        for section in config_file.parser.sections():
            print('Options in section %s: %s' %
                  (section, config_file.parser.options(section)))
        print('Enabled Tasks: %s' % config_file.enabled_tasks)
        for task in load_tasks().values():
            task_obj = task(config_file=config_file)
            print(task_obj.debug_msg())

        return 0


class UserInterface(ConfigMixin, InterfaceCore):
    """A base class for the User Interface."""

    description = """Escadrille: Automated Website Generation"""

    def __init__(self, version):
        self.parser = argparse.ArgumentParser(description=__doc__)
        self.version = version
        self.built = False

    def build(self):
        """Build the argument parser."""
        self.parser.add_argument(
            '--version', help='Print the version and exit.', action='version',
            version='%(prog)s {}'.format(self.version))
        DebugAction.add_parser_argument(self.parser)
        VerboseAction.add_parser_argument(self.parser)
        super().build()
        self.built = True

    def parse_cmd_line(self):
        """Parse the options from the command line."""
        if not self.built:
            self.build()
        args = self.parser.parse_args()
        self.validate_args(args)
        return args
