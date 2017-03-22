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
"""Generate a file of Checksums representing the output fileset."""

import os
from collections import OrderedDict

import escadrille.rst as rst

from .core import Task


class ChecksumUploadTask(Task):
    """Compare checksums and upload only files that are new or changed."""

    config_key = 'checksums'
    filename_default = ""
    filename_key = "filename"
    filename_default = ""

    def __init__(self, *args, **kwargs):
        """Set up defaults for Checksum Upload Task instances."""
        self.suffix = 'rst'  # TODO: add to general config file section
        self.filename = self.filename_default
        super().__init__(*args, **kwargs)

    def _load_config(self):
        """Load task options from the config file."""
        super()._load_config()

    def __call__(self, *args, **kwargs):
        """Execute the Checksum Upload task."""
        print('Starting Checksum Upload Task.')
        super().__call__(*args, **kwargs)
        # Get the remote/old checksum file and compare with the new file.
        # For each file that is new or different, upload to the target
        # location.
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += "  %s: %s\n" % (self.filename_key, self.filename)
        msg += "  stubs_dir: %s\n" % self.stubs_dir
        return msg

    @property
    def default_config(self):
        """Return a string of default example section for config file."""
        config = "[%s]\n" % self.config_key
        config += "  %s: %s\n" % (self.filename_key, self.filename_default)
        return config
