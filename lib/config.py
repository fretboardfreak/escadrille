"""Squadron Config File API
"""

import os
from configparser import SafeConfigParser
from configparser import ExtendedInterpolation
from enum import Enum


class GeneralOpts(Enum):
    """Options for the General Section."""
    output_dir = os.environ.get('HOME', '/tmp/')
    enabled_tasks = ''


class Sections(Enum):
    """The sections of the config file."""
    general = GeneralOpts
    copy_files = None  # Dynamic Option Discovery


class ConfigFile(object):
    """Config File API for Squadron."""

    default_path = os.path.abspath('./squadron.cfg')

    def __init__(self, filename):
        self.filename = filename
        self.parser = SafeConfigParser(interpolation=ExtendedInterpolation())
        self.loaded = False

    def load(self):
        """Load the configuration file into memory."""
        self.parser.read(self.filename)
        self.loaded = True

    def write_default_config(self):
        """Write an empty, default config file."""
        default_parser = SafeConfigParser(interpolation=ExtendedInterpolation)
        for section in Sections:
            default_parser.add_section(section.name)
            if not section.value:
                continue
            for option in section.value:
                default_parser.set(section.name, option.name, option.value)

        with open(self.filename, 'w') as fout:
            default_parser.write(fout)

    def get_copy_files_map(self):
        """Generate a map of files and destinations for the Copy Files Task."""
        pass
