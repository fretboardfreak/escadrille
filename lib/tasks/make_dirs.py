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
"""Make Dirs Task."""

import os

from .core import Task
from .core import OtherDirsOpt
from .options import GeneralDirsOpt


class MakeDirsTask(GeneralDirsOpt, OtherDirsOpt, Task):
    """Create any directories that may be needed by the squadron run."""

    config_key = 'make_dirs'

    def _make_dir(self, path):
        """Make a directory."""
        self.vprint('%s%s' % (self.indent * 2, path))
        if not os.path.exists(path):
            os.makedirs(path)

    def __call__(self, *args, **kwargs):
        self.vprint('Starting Make Files Task.')
        super().__call__(*args, **kwargs)
        if self.general_dirs:
            self.vprint('%sMaking General Dirs' % self.indent)
            self._make_dir(self.config_file.tmp_dir)
            self._make_dir(self.config_file.output_dir)
            self._make_dir(self.config_file.staging_dir)
        if self.other_dirs:
            self.vprint('%sMaking Other Dirs' % self.indent)
        for path in self.other_dirs:
            self._make_dir(path)
        self._set_status()

    def _get_option_snippet(self):
        """Return a string representing the options for this task."""
        retval = self.config_snippet_general_dirs
        retval += self.config_snippet_other_dirs
        return retval

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += self._get_option_snippet()
        return msg

    @property
    def default_config(self):
        """Return a string of the default example section for the config file.
        """
        config = "[%s]\n" % self.config_key
        config += self._get_option_snippet()
        config += '\n'
        return config
