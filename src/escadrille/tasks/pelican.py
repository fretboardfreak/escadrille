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
"""Pelican Task."""

import subprocess

from .core import Task
from .options import OutputDirOpt


class PelicanTask(OutputDirOpt, Task):
    """Run pelican using the options in the escadrille configuration file."""

    config_key = 'pelican'
    output_dir_default = ''
    input_dir_key = 'input_dir'
    input_dir_default = ''
    pelican_config_key = 'pelican_config'
    pelican_config_default = ''
    theme_dir_key = 'theme_dir'
    theme_dir_default = ''
    pelican_options_key = 'pelican_options'
    pelican_options_default = '-D'

    def __init__(self, *args, **kwargs):
        """Setup default values for Pelican Task instances."""
        self.input_dir = self.input_dir_default
        self.pelican_config = self.pelican_config_default
        self.theme_dir = self.theme_dir_default
        self.pelican_options = self.pelican_options_default
        super().__init__(*args, **kwargs)

    def _load_config(self):
        """Load task options from the config file."""
        input_dir = self.config_file.get(self.config_key, self.input_dir_key)
        if input_dir is not None:
            self.input_dir = self.sanitize_path(input_dir)
        pelican_config = self.config_file.get(self.config_key,
                                              self.pelican_config_key)
        if pelican_config is not None:
            self.pelican_config = self.sanitize_path(pelican_config)
        theme_dir = self.config_file.get(self.config_key, self.theme_dir_key)
        if theme_dir is not None:
            self.theme_dir = self.sanitize_path(theme_dir)
        pelican_options = self.config_file.get(self.config_key,
                                               self.pelican_options_key)
        if pelican_options is not None:
            self.pelican_options = pelican_options
        super()._load_config()

    def __call__(self, *args, **kwargs):
        """Execute the Pelican Task."""
        print('Starting Pelican Task.')
        super().__call__(*args, **kwargs)
        command = "pelican %s -o %s -s %s -t %s %s" % (
            self.input_dir, self.output_dir, self.pelican_config,
            self.theme_dir, self.pelican_options)
        subprocess.check_call(command, shell=True)
        self.vprint('command: %s' % command)
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += self.config_snippet_output_dir
        msg += self.msg_template % (self.indent, self.input_dir_key,
                                    self.input_dir)
        msg += self.msg_template % (self.indent, self.pelican_config_key,
                                    self.pelican_config)
        msg += self.msg_template % (self.indent, self.theme_dir_key,
                                    self.theme_dir)
        msg += self.msg_template % (self.indent, self.pelican_options_key,
                                    self.pelican_options)
        return msg

    @property
    def default_config(self):
        """Return a string of default example section for config file."""
        config = "[%s]\n" % self.config_key
        config += self.config_snippet_output_dir
        config += self.msg_template % (self.indent, self.input_dir_key,
                                       self.input_dir_default)
        config += self.msg_template % (self.indent, self.pelican_config_key,
                                       self.pelican_config_default)
        config += self.msg_template % (self.indent, self.theme_dir_key,
                                       self.theme_dir_default)
        config += self.msg_template % (self.indent, self.pelican_options_key,
                                       self.pelican_options_default)
        return config
