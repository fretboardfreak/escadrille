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
"""The core escadrille business logic."""
import sys
import os
import argparse
import errno

from .config import ConfigFile
from .tasks import load_tasks
from .verbosity import DebugAction
from .verbosity import VerboseAction
from .verbosity import vprint
from .verbosity import dprint
from .version import VERSION


class InterfaceCore(object):
    """A base class for mixins that can add features to the UserInterface."""
    def __init__(self):
        self.config_file = None
        self.tasks = None
        self.skip = None
        self.list_tasks = None

    def build(self):
        """Construct the self.parser object."""
        pass

    def validate_args(self, args):
        """Validate the provided options meet requirements."""
        pass

    def _main(self):
        """Main business logic for Escadrille."""
        self.skip = self.skip if self.skip else []
        if self.tasks is None:
            self.tasks = load_tasks()
        if self.list_tasks is not None and self.list_tasks:
            for index, task_name in enumerate(
                    self.config_file.enabled_tasks, 1):
                print('%2d: %s' % (index, task_name))
            return 0
        for task_name in self.config_file.enabled_tasks:
            if task_name in self.skip:
                vprint('Skipping task "%s".' % task_name)
                continue
            task = self.tasks[task_name](config_file=self.config_file)
            task()
            if task.status is not None and task.status != 0:
                print('Task "%s" did not succeed: errno %s\n  Warnings:\n'
                      '    %s\n  Errors:\n    %s' %
                      (task_name, task.status,
                       '\n    '.join(task.warnings),
                       '\n    '.join(task.errors)))
                return task.status
            elif task.warnings:
                print('Task "%s" succeeded with warnings:\n    %s' %
                      (task_name, '\n    '.join(task.warnings)))
            else:
                vprint('Task %s succeeded with no errors.' % task_name)
        vprint('All Tasks Completed. Exiting.')
        return 0


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


class CliInterface(ConfigMixin, InterfaceCore):
    """A Command Line User Interface."""

    description = """Escadrille: Automated Website Generation"""

    def __init__(self):
        super(CliInterface, self).__init__()
        self.parser = argparse.ArgumentParser(description=__doc__)
        self.version = VERSION
        self.built = False

    def build(self):
        """Build the argument parser."""
        self.parser.add_argument(
            '--version', help='Print the version and exit.', action='version',
            version='%(prog)s {}'.format(self.version))
        DebugAction.add_parser_argument(self.parser)
        VerboseAction.add_parser_argument(self.parser)
        self.parser.add_argument(
            '-s', '--skip', dest='skip', action='append', metavar='TASK',
            help='Specify an enabled task to skip.')
        self.parser.add_argument(
            '-l', '--list', dest='list', action='store_true',
            help='List the enabled tasks in the config file.')
        super().build()
        self.built = True

    def parse_cmd_line(self):
        """Parse the options from the command line."""
        if not self.built:
            self.build()
        args = self.parser.parse_args()
        self.validate_args(args)
        return args

    def _main(self):
        options = self.parse_cmd_line()
        dprint('loading configuration...')
        self.config_file = ConfigFile(options.config)
        self.config_file.load()
        self.tasks = load_tasks()
        self.skip = options.skip
        self.list_tasks = options.list
        if options.default_config:
            self.config_file.print_default_config(self.tasks)
            return 0
        if options.debug_config:
            return self.print_config_debug(options)
        return super()._main()

    @classmethod
    def main(cls):
        """Escadrille's main entry point for CLI usage."""
        try:
            cls = CliInterface()
            sys.exit(cls._main())
        except SystemExit:
            sys.exit(0)
        except KeyboardInterrupt:
            print('...interrupted by user, exiting.')
            sys.exit(1)
        except Exception as exc:
            import escadrille.verbosity
            if escadrille.verbosity.DEBUG:
                raise
            else:
                print(exc)
                sys.exit(1)
