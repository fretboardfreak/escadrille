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
"""A basic script to read and help debug issues with the config file."""
import sys


from lib.cmdline import DebugUI
from lib.config import ConfigFile
from lib.tasks import load_tasks


VERSION = "0.1"


def main():
    """Main method for config_debug.py"""
    user_interface = DebugUI(version=VERSION)
    user_interface.description = "A tool for debugging squadron config files."
    options = user_interface.parse_cmd_line()

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
