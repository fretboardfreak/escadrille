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

from .cmdline import UserInterface
from .verbosity import vprint
from .verbosity import dprint
from .config import ConfigFile
from .tasks import load_tasks
from .version import VERSION


def main(config_file, tasks=None, skip=None):
    """Main business logic for Escadrille."""
    if tasks is None:
        tasks = load_tasks()
    for task_name in config_file.enabled_tasks:
        if task_name in skip:
            vprint('Skipping task "%s".' % task_name)
            continue
        task = tasks[task_name](config_file=config_file)
        task()
        if task.status is not None and task.status != 0:
            print('Task "%s" did not succeed: errno %s\n  Warnings:\n    %s\n'
                  '  Errors:\n    %s' % (task_name, task.status,
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


def cli_main():
    """Escadrille's main entry point for CLI usage."""
    try:
        user_interface = UserInterface(version=VERSION)
        options = user_interface.parse_cmd_line()
        dprint('loading configuration...')
        config_file = ConfigFile(options.config)
        config_file.load()
        tasks = load_tasks()
        if options.default_config:
            config_file.print_default_config(tasks)
            return 0
        if options.debug_config:
            return user_interface.print_config_debug(options)
        sys.exit(main(config_file, tasks, options.skip))
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
