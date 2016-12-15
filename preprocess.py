#!/usr/bin/env python3
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
