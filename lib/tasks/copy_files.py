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
"""Copy Files Task."""

import os
import subprocess
import glob
import shlex

from .core import Task


class CopyFilesJob(object):

    """Data object to represent one Copy Files Job."""

    def __init__(self, name, sources, destination):
        self.name = name
        self.sources = sources
        self.destination = destination


class CopyFilesTask(Task):
    """Copy Files from around the system into the squadron build.

    Option keys use the suffixes "_dest" and "_src". Files listed in space
    separated strings as absolute paths are copied from options with the "_src"
    suffix to the single destination expected in the "_dest" option with the
    corresponding slug.

    (i.e "pics_src=/home/user/pics/*.jpeg /home/user/ref/images/*"
    would all get copied to "pics_dest=/tmp/squadron/staging/")

    note: This behaviour disallows files containing spaces in their path. For
          paths containing spaces you can workaround this limitation by using
          an asterisk in place of a space. The wildcard will match the spaces
          and there is a very good chance that the rest of the path will
          preclude any other matches but the intended target.
    """

    config_key = 'copy_files'

    def __init__(self, *args, **kwargs):
        self.jobs = []
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.vprint('Starting Copy Files Task')
        super().__call__(*args, **kwargs)
        self.dprint('%d copy jobs loaded from config file.' % len(self.jobs))
        for index, job in enumerate(self.jobs, 1):
            self.vprint('%s(%d/%d) %s' %
                        (self.indent, index, len(self.jobs), job.name))
            destination = os.path.abspath(os.path.expanduser(job.destination))
            if not os.path.exists(destination):
                os.makedirs(destination)
            for source_dir in job.sources:
                source_dir = os.path.abspath(os.path.expanduser(source_dir))
                source_paths = [shlex.quote(path) for path in
                                glob.glob(source_dir, recursive=True)]
                if not source_paths:
                    self.vprint('%sno files to copy at "%s"' %
                                (self.indent * 2, source_dir))
                    continue
                self.vprint('%scopying "%s"...' % (self.indent * 2,
                                                   source_dir))
                subprocess.check_call(' '.join(['cp', '--recursive',
                                                *source_paths, destination]),
                                      shell=True)
        self._set_status()

    def _load_config(self):
        """Generate a map of files and destinations for the Copy Files Task."""
        super()._load_config()
        jobs, src_suffix, dest_suffix = {}, '_src', '_dst'
        options = []
        if (self.config_file.parser and
                self.config_file.has_section(self.config_key)):
            options = self.config_file.section(self.config_key).keys()
        for option in options:
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
            sources_string = ' '.join(str(self.config_file.get(
                self.config_key, source_opt)).split('\n'))
            job['sources'] = [
                pth.strip() for pth in sources_string.split(' ')]
            job['destination'] = self.config_file.get(
                self.config_key, dest_opt)
            jobs[parts[0]] = CopyFilesJob(**job)
        self.jobs = jobs.values()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        for job in self.jobs:
            msg += '  %s:\n' % job.name
            msg += '    sources:\n      '
            msg += '\n      '.join(job.sources)
            msg += '\n    destination: %s\n' % job.destination
        return msg

    @property
    def default_config(self):
        """Return a string of the default example section for the config file.
        """
        config = "[%s]\n" % self.config_key
        comment = ["Add key pairs using the suffixes '_dst' and '_src'.",
                   "The keys with the '_dst' suffix should be a string",
                   "path to the destination for the matching source key.",
                   "The matching source key with the '_src' suffix is a",
                   "list of paths to be copied into the destination."]
        config += '; %s\n\n' % '\n; '.join(comment)
        return config
