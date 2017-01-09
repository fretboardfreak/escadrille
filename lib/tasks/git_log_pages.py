# Copyright 2016 Curtis Sand <curtissand@gmail.com>
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
"""Git Log Pages Task."""

from .core import Task
from .core import OutputDirOpt


class GitLogPagesTask(OutputDirOpt, Task):
    """Make RST source pages out of Git Repository Logs."""

    config_key = 'git_log_pages'

    def __call__(self, *args, **kwargs):
        self.vprint('Starting Git Log Pages Task.')
        super().__call__(*args, **kwargs)
        # TODO: implement
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += self.config_snippet_output_dir
        return msg

    @property
    def default_config(self):
        """Return a string of the default example section for the config file.
        """
        config = "[%s]\n" % self.config_key
        config += self.config_snippet_output_dir
        config += '\n'
        return config
