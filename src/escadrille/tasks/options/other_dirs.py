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
"""General Dirs Option for Tasks."""

from ..core import TaskCore


class OtherDirsOpt(TaskCore):
    """A mixin class for a config list option called "other_dirs"."""

    other_dirs_key = 'other_dirs'
    other_dirs_default = []

    def __init__(self, *args, **kwargs):
        """Set up defaults for the Other Dirs Option."""
        self.other_dirs = self.other_dirs_default
        super().__init__(*args, **kwargs)

    def _load_config(self):
        """Load the other_dirs list from the config file."""
        other_dirs_val = self.config_file.get(
            self.tag, self.other_dirs_key)
        if other_dirs_val is None:
            self.other_dirs = self.other_dirs_default
        else:
            self.other_dirs = [path for path in
                               other_dirs_val.split(self.config_file.list_sep)
                               if path != '']
        super()._load_config()

    @property
    def config_snippet_other_dirs(self):
        """Return a string representing the other_dirs config option."""
        return (self.msg_template % (
            self.indent, self.other_dirs_key,
            self.config_file.list_sep.join(self.other_dirs)))
