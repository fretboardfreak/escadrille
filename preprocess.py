#!/usr/bin/env python3
"""
"""

import sys


from lib.cmdline import PreprocessUI
from lib.cmdline import dprint
from lib.cmdline import vprint


VERSION = "0.0"


def main():
    user_interface = PreprocessUI(version=VERSION)
    dprint(user_interface.parse_cmd_line())
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
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
