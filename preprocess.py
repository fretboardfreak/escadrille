#!/usr/bin/env python3
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
"""A script to run the squadron preprocessing tasks."""
import sys


from lib.cmdline import PreprocessUI
from lib.cmdline import vprint
from lib.cmdline import dprint
from lib.config import ConfigFile
from lib.tasks import load_tasks


VERSION = "0.1"


def main():
    """Main method for preprocess.py"""
    user_interface = PreprocessUI(version=VERSION)
    options = user_interface.parse_cmd_line()

    dprint('loading configuration...')
    config_file = ConfigFile(options.config)
    config_file.load()
    tasks = load_tasks()
    if options.default_config:
        config_file.print_default_config(tasks)
        return 0
    for task_name in config_file.enabled_tasks:
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


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        import lib.cmdline
        if lib.cmdline.DEBUG:
            raise
        else:
            print(exc)
            sys.exit(1)
