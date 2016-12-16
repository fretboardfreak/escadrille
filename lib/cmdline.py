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
"""Library of command line tools for Squadron Automation."""

import os
import argparse
import errno

from lib.config import ConfigFile


VERBOSE = False
DEBUG = False


class ConfigMixin(object):
    """Mixin class to add options for the configuration file."""
    def build(self):
        """Add config file options to the parser."""
        self.parser.add_argument(
            '-c', '--config', action='store', dest='config',
            default=ConfigFile.default_path,
            help='Specify the config file to use.')
        super().build()

    def validate_args(self, args):
        """If provided, ensure that the config file path exists."""
        if not os.path.exists(args.config):
            raise FileNotFoundError(errno.ENOENT, "Config File not found",
                                    args.config)
        super().validate_args(args)


class BaseUI(object):
    """A base class for the User Interface."""

    description = "A description of the UI tool."

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
        self.built = True

    def validate_args(self, args):
        """Subclasses can implement this to verify validity of given args."""
        pass

    def parse_cmd_line(self):
        """Parse the options from the command line."""
        if not self.built:
            self.build()
        args = self.parser.parse_args()
        self.validate_args(args)
        return args


class PreprocessUI(ConfigMixin, BaseUI):
    """UI Interface for the Preprocessor Command Line tool."""

    description = """Squadron Preprocessor Tool."""


def dprint(msg):
    """Conditionally print a debug message."""
    if DEBUG:
        print('dbg:', msg)


def vprint(msg):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(msg)


class DebugAction(argparse.Action):
    """Enable the debugging output mechanism."""

    shortflag = '-d'
    flag = '--debug'
    help = 'Enable debugging output.'

    @classmethod
    def add_parser_argument(cls, parser):
        """Add the action argument."""
        parser.add_argument(cls.shortflag, cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, nargs=0,
                         default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Enable debugging output."""
        print('Enabling debugging output.')
        global DEBUG
        DEBUG = True
        setattr(namespace, self.dest, True)


class VerboseAction(DebugAction):
    """Enable the verbose output mechanism."""

    shortflag = '-v'
    flag = '--verbose'
    help = 'Enable verbose output.'

    def __call__(self, parser, namespace, values, option_string=None):
        """Enable verbose output."""
        print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)
