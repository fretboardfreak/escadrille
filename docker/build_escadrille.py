#!/usr/bin/env python3
"""Helper script to simplify building the escadrille docker image."""

import sys
import argparse
import os
import subprocess
from time import strftime

VERSION = "0.1"
VERBOSE = False


def main():
    """Main method for the script"""
    args = parse_cmd_line(**generate_arg_defaults())
    vprint(args)
    validate_path_and_cwd(args)
    build_docker(args)
    return 0


def build_docker(args):
    """Execute the docker build command with the specified arguments."""
    command = ""
    if os.getuid() != 0:
        command += "sudo "
    command += ("docker build --rm -f %s --build-arg user=%s "
                "--build-arg uid=%s --build-arg gid=%s "
                "--tag escadrille:%s ." % (
                    args.dockerfile, args.user, args.uid, args.gid, args.tag))
    print('Creating Escadrille docker image using tag, "escadrille:%s", '
          'and user "%s" (uid=%s, gid=%s)' %
          (args.tag, args.user, args.uid, args.gid))
    vprint('Executing command: %s' % command)
    subprocess.check_call(command, shell=True)


def generate_arg_defaults():
    """Return a dict of programmatically determined argument defaults."""
    return {'user': os.getlogin(),
            'uid': os.getuid(),
            'gid': os.getgid(),
            'tag': strftime('%y%m%d%H%M'),
            'dockerfile': './docker/escadrille'}


def validate_path_and_cwd(args):
    """Ensure that the script was executed from an appropriate location."""
    if not os.path.exists(args.dockerfile):
        vprint('Could not find the dockerfile at path "%s"' % args.dockerfile)
        sys.exit(1)


def parse_cmd_line(user=None, uid=None, gid=None, tag=None, dockerfile=None):
    """Parse the command line options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', help='Print the version and exit.', action='version',
        version='%(prog)s {}'.format(VERSION))
    VerboseAction.add_parser_argument(parser)
    parser.add_argument('-u', '--user',
                        help=("Create a user with this name "
                              "in the docker image. (default: %s)" % user),
                        default=user)
    parser.add_argument('-U', '--uid',
                        help=("Create a user with this UID in the "
                              "docker image. (default: %s)" % uid),
                        default=uid)
    parser.add_argument('-g', '--gid',
                        help=("Create a user with this GID int he "
                              "docker image. (default: %s)" % gid),
                        default=gid)
    parser.add_argument('-t', '--tag',
                        help=("Create the docker image using this "
                              "version tag. (default: %s)" % tag),
                        default=tag)
    parser.add_argument('-d', '--dockerfile',
                        help=("The path to the escadrille dockerfile "
                              "(default: '%s'" % dockerfile),
                        default=dockerfile)
    return parser.parse_args()


def vprint(msg):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(msg)


class VerboseAction(argparse.Action):
    """Enable the verbose output mechanism."""

    sflag = '-v'
    flag = '--verbose'
    help = 'Enable verbose output.'

    @classmethod
    def add_parser_argument(cls, parser):
        """Add the parser argument represented by this action."""
        parser.add_argument(cls.sflag, cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        """Initialie the argparse Action with the appropriate settings."""
        super(VerboseAction, self).__init__(option_strings, dest, nargs=0,
                                            default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Enable Verbose output."""
        print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        print('Unhandled Error:\n{}'.format(exc))
        sys.exit(1)
