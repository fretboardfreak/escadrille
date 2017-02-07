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
"""Library to provide different levels of output verbosity."""

import argparse


VERBOSE = False
DEBUG = False


def dprint(msg):
    """Conditionally print a debug message."""
    prefix = 'dbg: '
    line_sep = '\n%s' % prefix
    if DEBUG:
        lines = msg.split('\n')
        print(prefix + line_sep.join(lines))


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
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)
