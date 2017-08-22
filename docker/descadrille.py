#!/usr/bin/env python3
"""Utility script to simplify use of the escadrille docker container."""

import sys
import argparse
import os
import subprocess

VERSION = "0.1"
VERBOSE = False


def main():
    """Main method for the script"""
    args = parse_cmd_line(**generate_arg_defaults())
    vprint(args)
    run_escadrille_docker(args)
    return 0


def generate_arg_defaults():
    """Return a dict of programmatically determined argument defaults."""
    return {'image': 'escadrille:latest',
            'command': (
                '/bin/bash -c "source /opt/escadrille_env/bin/activate; '
                'escadrille --help"'),
            'mount': [],
            'run_opts': ['--rm', '--interactive', '--tty']}


def parse_cmd_line(image=None, command=None, mount=None, run_opts=None):
    """Parse the command line options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', help='Print the version and exit.', action='version',
        version='%(prog)s {}'.format(VERSION))
    VerboseAction.add_parser_argument(parser)
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help="Print steps instead of executing them.")
    parser.add_argument(
        '-i', '--image', default=image,
        help=("The 'name:tag' of the docker image to run. default=['%s']" %
              image))
    parser.add_argument(
        '-c', '--command', default=command,
        help=("The command string to pass to the docker image. "
              "default=['%s']" % command))
    parser.add_argument(
        '-m', '--mount', dest='mounts', action='append', default=mount,
        help="Pass '--mount' arguments to docker run. default=%s" % mount)
    parser.add_argument(
        '-r', '--run_opts', dest='run_opts', action='append', default=run_opts,
        help=("Pass other docker options to the run command. default=%s" %
              run_opts))
    return parser.parse_args()


def run_escadrille_docker(args):
    """Build a docker command and execute the docker image."""
    command = (add_sudo() +
               "docker run {} {} {} {}".format(
                   ' '.join(args.run_opts), format_mounts(args.mounts),
                   image_name(args.image), args.command))
    execute_docker(command, dry_run=args.dry_run)


def add_sudo():
    """Return the sudo cmd prefix if it is required to run docker."""
    if os.getuid() == 0:
        return ""
    else:
        return "sudo "


def format_mounts(mount_opts):
    """Format the mount volumes for the docker run command."""
    return ' '.join([i + j for i, j in
                     zip(['--mount '] * len(mount_opts), mount_opts)])


def image_name(image):
    """Find an appropriate image name for the run command."""
    if image.find(':') > 0:
        return image.strip()
    else:
        return "escadrille:" + image.strip()


def execute_docker(command, dry_run=False):
    """Execute the docker command obeying the dry_run flag."""
    if dry_run:
        print("dry_run: " + command)
    else:
        vprint("Executing: " + command)
        subprocess.check_call(command, shell=True)


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
