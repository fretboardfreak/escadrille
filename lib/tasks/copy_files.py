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


class CopyFilesJob(object):
    def __init__(self, name, sources, destination):
        self.name = name
        self.sources = sources
        self.destination = destination


class CopyFilesTask(Task):
    """Base Task object for Squadron.

    The config_key attribute is used to reference the tasks from the config
    file.
    The __init__ and __call__ methods should be implemented by the subclasses.
    """

    config_key = 'copy_files'

    def __init__(self, *args, **kwargs):
        self.jobs = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)

    def load_from_config(self):
        """Generate a map of files and destinations for the Copy Files Task."""
        super().load_from_config()
        jobs, src_suffix, dest_suffix = {}, '_src', '_dst'
        for option in self.config_file.parser.options(self.config_key):
            parts = option.split('_')
            if not (option.endswith(src_suffix) or
                    option.endswith(dest_suffix)):
                continue
            if parts[0] in jobs:
                continue
            job = {'name': parts[0]}
            if option.endswith(src_suffix):
                source_opt = option
                dest_opt = option.replace(src_suffix, dest_suffix)
            elif option.endswith(dest_suffix):
                source_opt = option.replace(dest_suffix, src_suffix)
                dest_opt = option
            sources_string = ' '.join(str(self.config_file.parser.get(
                self.config_key, source_opt)).split('\n'))
            job['sources'] = [
                pth.strip() for pth in sources_string.split(' ')]
            job['destination'] = self.config_file.parser.get(
                self.config_key, dest_opt)
            jobs[parts[0]] = CopyFilesJob(**job)
        self.jobs = jobs.values()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        for job in self.jobs:
            msg += '  %s:\n' % job.name
            msg += '    sources:\n    '
            msg += '\n      '.join(job.sources)
            msg += '\n    destination: %s\n' % job.destination
        return msg
