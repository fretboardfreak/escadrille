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
"""Preprocessor script for Squadron."""
import sys


from lib.cmdline import PreprocessUI
from lib.cmdline import dprint
from lib.cmdline import vprint
from lib.config import ConfigFile


VERSION = "0.0"


def main():
    """Main method for Squadron preprocessor."""
    user_interface = PreprocessUI(version=VERSION)
    options = user_interface.parse_cmd_line()
    dprint('cmdline args: %s' % options)
    vprint('Parsing Config File...')
    config_file = ConfigFile(options.config)
    config_file.load()
    dprint('Config Sections: %s' % config_file.parser.sections())
    for section in config_file.parser.sections():
        dprint('Options in section %s: %s' %
               (section, config_file.parser.options(section)))
    dprint('Enabled Tasks: %s' % config_file.enabled_tasks)
    dprint('Copy Files Jobs:')
    for cfj in list(config_file.copy_files_jobs):
        dprint("%s:" % cfj.name)
        dprint("  sources: %s" % ' '.join(cfj.value.sources.value))
        dprint("  destination: %s" % cfj.value.destination.value)

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
