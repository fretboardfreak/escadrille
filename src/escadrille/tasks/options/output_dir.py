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


class OutputDirOpt(TaskCore):
    """Mixin class to provide Task object with an Output Dir config value."""

    output_dir_key = 'output_dir'

    def __init__(self, *args, **kwargs):
        """Set up defaults for Output Dir Option."""
        super().__init__(*args, **kwargs)
        self.output_dir = self.output_dir_default

    @property
    def output_dir_default(self):
        """Default value is based on existing option in general section."""
        return self.config_file.staging_dir

    def _load_config(self):
        """Load the output dir path option from the config file."""
        output_dir = self.config_file.get(self.config_key, self.output_dir_key)
        if output_dir is None:
            self.output_dir = self.output_dir_default
        else:
            self.output_dir = output_dir.strip()
        super()._load_config()

    @property
    def config_snippet_output_dir(self):
        """Return a string representing the output_dir config option."""
        return ("%s%s: %s\n" % (self.indent, self.output_dir_key,
                                self.output_dir))
