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
"""Generate a file of checksums representing the output file set."""

import os
import subprocess
from collections import OrderedDict


import escadrille.rst as rst

from .core import Task


class ChecksumsTask(Task):
    """Generate a file of checksums representing the file set."""

    config_key = 'checksums'
    filename_default = "checksums.txt"
    filename_key = "filename"
    target_dir_key = 'target_dir'
    target_dir_default = "{general:output_dir}"

    def __init__(self, *args, **kwargs):
        """Set up defaults for Checksums Task instances."""
        self.suffix = 'rst'  # TODO: add to general config file section
        self.filename = self.filename_default
        super().__init__(*args, **kwargs)
        self.target_dir = self.config_file.output_dir

    def _load_config(self):
        """Load task options from the config file."""
        super()._load_config()

    def _which(self, binary):
        """Run the bash 'which' command to search for a binary in PATH."""
        error, output = subprocess.getstatusoutput("which %s" % binary)
        if not error:
            return output
        return ""

    @property
    def shasum_command(self):
        """Return a valid SHA 512 bash command for the current system.

        Should support both MacOS and linux by looking for first the "shasum"
        command (use the option "-a 512" with "shasum") or otherwise look for
        the binary sha512 explicitly.
        """
        command = self._which('xshasum')
        if not command:
            self.dprint('Cannot find "shasum" command looking for '
                        '"shas512sum" instead...')
            command = self._which('sha512sum')
        return command

    def __call__(self, *args, **kwargs):
        """Execute the Checksums task."""
        print('Starting Checksums Task.')
        super().__call__(*args, **kwargs)
        self.dprint('running command: %s' % self.shasum_command)
        # Create one checksums.txt file containing the checksum for each file
        # in the general.output_dir
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += "  %s: %s\n" % (self.filename_key, self.filename)
        msg += "  %s: %s\n" % (self.target_dir_key, self.target_dir)
        return msg

    @property
    def default_config(self):
        """Return a string of default example section for config file."""
        config = "[%s]\n" % self.config_key
        config += "  %s: %s\n" % (self.filename_key, self.filename_default)
        config += "  %s: %s\n" % (self.target_dir_key, self.target_dir_default)
        return config
