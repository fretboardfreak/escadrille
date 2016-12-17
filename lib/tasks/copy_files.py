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
"""Copy Files Task."""

from .core import Task


class CopyFilesTask(Task):
    """Base Task object for Squadron.

    The config_key attribute is used to reference the tasks from the config
    file.
    The __init__ and __call__ methods should be implemented by the subclasses.
    """

    config_key = 'copy_files'

    def __init__(self, sources, destination, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sources = sources
        self.destination = destination

    def __call__(self, *args, **kwargs):
        pass
