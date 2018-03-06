# Copyright 2017 Curtis Sand <curtissand@gmail.com>
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
"""Debug task to print the shared state in the escadrille engine."""

from .core import Task


class PrintSharedState(Task):
    """Debug task to prints the shared state saved in the escadrille engine."""

    config_name = 'print_shared_state'

    def __call__(self, *args, **kwargs):
        """Parse input files into doctree and pickle results."""
        print('Starting print_shared_state Task.')
        super().__call__(*args, **kwargs)
        print(self.shared_state)

    def debug_msg(self):
        """Return debug output about current task state."""
        msg = super().debug_msg() + "\n"
        return msg

    @property
    def default_config(self):
        """Return default example section for config file."""
        config = "[%s_tag]\n" % self.config_name
        config += self.config_snippet_name
        return config
