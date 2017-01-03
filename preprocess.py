#!/usr/bin/env python3
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

    config_file = ConfigFile(options.config)
    config_file.load()
    tasks = load_tasks()
    for enabled_task in config_file.enabled_tasks:
        if enabled_task in tasks:
            vprint('Starting task %s' % enabled_task)
        task = tasks[enabled_task](config_file=config_file)
        dprint(task.debug_msg())
        task()
        if task.status is not None and task.status != 0:
            print('Task "%s" did not succeed: errno %s\n  Warnings:\n    %s\n'
                  '  Errors:\n    %s' % (enabled_task, task.status,
                                   '\n    '.join(task.warnings),
                                   '\n    '.join(task.errors)))

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
