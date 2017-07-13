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
"""Clean Task."""

import subprocess

from .core import Task
from .options import GeneralDirsOpt
from .options import OtherDirsOpt


class CleanTask(GeneralDirsOpt, OtherDirsOpt, Task):
    """Clean out directories as needed."""

    config_name = 'clean'

    def _remove(self, path):
        """Remove a path."""
        self.vprint('%sremoving %s' % (self.indent, path))
        try:
            subprocess.check_call(['rm', '-r', '-f', path])
        except subprocess.CalledProcessError:
            err = '%sfailed to remove %s' % (self.indent, path)
            self.vprint(err)
            self.warnings.append(err)

    def __call__(self, *args, **kwargs):
        """Execute the Clean Task."""
        print('Starting Clean Task.')
        super().__call__(*args, **kwargs)
        if self.general_dirs:
            dirs = [self.config_file.output_dir, self.config_file.staging_dir,
                    self.config_file.tmp_dir]
            for path in dirs:
                self._remove(path)
        for path in self.other_dirs:
            self._remove(path)
        self._set_status()

    def _get_option_snippet(self):
        """Return a string representing the options for this task."""
        retval = self.config_snippet_name
        retval += self.config_snippet_general_dirs
        retval += self.config_snippet_other_dirs
        return retval

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += self._get_option_snippet()
        return msg

    @property
    def default_config(self):
        """Return a string of default example section for config file."""
        config = "[%s_tag]\n" % self.config_name
        config += self._get_option_snippet()
        config += '\n'
        return config
