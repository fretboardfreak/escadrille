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

from lib.tasks.core import TaskCore


class GeneralDirsOpt(TaskCore):
    """A mixin class for a config boolean option called "general_dirs"."""

    general_dirs_key = 'general_dirs'
    general_dirs_default = True

    def __init__(self, *args, general_dirs=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.general_dirs = self.general_dirs_default
        if general_dirs is not None:
            self.general_dirs = general_dirs

    def _load_config(self):
        """Load the general_dirs boolean from the config file."""
        general_dirs = self.config_file.getboolean(
            self.config_key, self.general_dirs_key)
        if general_dirs is None:
            self.general_dirs = self.general_dirs_default
        else:
            self.general_dirs = bool(int(general_dirs))
        super()._load_config()

    @property
    def config_snippet_general_dirs(self):
        """Return a string representing the general_dirs config option."""
        return ("%s%s: %s\n" % (self.indent, self.general_dirs_key,
                                self.general_dirs))
