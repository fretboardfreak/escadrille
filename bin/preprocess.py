#!/usr/bin/env python3
"""preprocess.py : A script to do some preprocessing tasks."""

import sys
import os
import argparse
import shutil
import glob

try:
    import ConfigParser as configparser
except ImportError:  # python 2
    import configparser


VERSION = "0.1"
VERBOSE = False
DEBUG = False


def main():
    args = parse_cmd_line()
    dprint(args)

    config = Config(args.config)
    if args.write_config:
        if os.path.exists(args.config):
            print('Config file already exists. Cowardly quitting.')
            return 1
        config.write_default_config()
        print('Example config file written to "%s". Don\'t forget '
              'to fill it in.' % args.config)
        return 0
    config.load()

    for task in [CopyFilesTask()]:
        task(config)

    return 0


def parse_cmd_line():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--version', help='Print the version and exit.', action='version',
        version='%(prog)s {}'.format(VERSION))
    DebugAction.add_parser_argument(parser)
    VerboseAction.add_parser_argument(parser)
    parser.add_argument('-c', '--config', help=('The config file to use. '
                                                '*REQUIRED*'),)

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-w', '--write-config', dest='write_config',
                       action='store_true', help='Write an empty config file.')
    return parser.parse_args()


def dprint(msg):
    """Conditionally print a debug message."""
    if DEBUG:
        print(msg)


def vprint(msg):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(msg)


class DebugAction(argparse.Action):
    """Enable the debugging output mechanism."""

    flag = '--debug'
    help = 'Enable debugging output.'

    @classmethod
    def add_parser_argument(cls, parser):
        parser.add_argument(cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        super(DebugAction, self).__init__(option_strings, dest, nargs=0,
                                          default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling debugging output.')
        global DEBUG
        DEBUG = True
        setattr(namespace, self.dest, True)


class VerboseAction(DebugAction):
    """Enable the verbose output mechanism."""

    flag = '--verbose'
    help = 'Enable verbose output.'

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)


class ConfigSections(list):
    def __init__(self):
        super(ConfigSections, self).__init__(['paths'])
        for attr in self:
            setattr(self, attr, attr)

    @property
    def example_paths_section(self):
        """Source and dest. paths are specified with "_dst"/"_src" suffix.

        Paths ending with "_dst" must be directories.
        """
        return {'content_dir': '/some/path',
                'first_dst': '%(content_dir)s',
                'first_src': ('/space/separated /list/of/file/*patterns '
                              '~/to/copy/to/destination')}


class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.parser = configparser.SafeConfigParser()
        self.sections = ConfigSections()
        self.loaded = False

    def load(self):
        self.parser.read(self.filename)
        self.loaded = True

    def write_default_config(self):
        default_parser = configparser.SafeConfigParser()
        for section in self.sections:
            default_parser.add_section(section)
        for key, value in self.sections.example_paths_section.items():
            default_parser.set(self.sections.paths, key, value)

        with open(self.filename, 'w') as fout:
            default_parser.write(fout)

    def get_files_to_copy(self):
        dest_suffix = '_dst'
        src_suffix = '_src'
        file_map = {}
        for option in self.parser.options(self.sections.paths):
            if not option.endswith(dest_suffix):
                continue
            if (option.replace(dest_suffix, src_suffix) not in
                    self.parser.options(self.sections.paths)):
                raise Exception('Mismatched _src and _dst keys in config '
                                'file.')

            dest = self.parser.get(self.sections.paths, option)
            sources = self.parser.get(self.sections.paths,
                                      option.replace(dest_suffix, src_suffix))
            file_map[dest] = []
            for path in sources.split(' '):
                file_map[dest].extend(glob.glob(os.path.expanduser(path)))
        return file_map


class CopyFilesTask(object):
    """Help construct a content source directory by copying files as needed.

    In the "paths" section of the config, define destination directories with
    the suffixe "_dst" in the key name. The source files are specified as a
    space separated list of paths in a config variable using a key suffix of
    "_src" where the part of the key before the suffix matches a destination
    key.
    """
    def __call__(self, config):
        vprint('Copying Files:')
        file_map = config.get_files_to_copy()
        vprint('File Map: %s' % file_map)
        for destination in file_map:
            if not os.path.exists(destination):
                dprint('making missing directory: %s' % destination)
                os.makedirs(destination)
            for source in file_map[destination]:
                vprint('  %s -> %s' % (source, destination))
                if os.path.exists(os.path.join(destination, os.path.split(source)[1])):
                    raise Exception('Duplicate content files exist. Cowardly '
                                    'skipping the duplicated file. %s' %
                                    source)
                shutil.copy(source, destination)



if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if DEBUG:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
