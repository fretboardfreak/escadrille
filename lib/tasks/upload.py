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
"""Upload Task."""

import subprocess

from .core import Task


class UploadTask(Task):
    """Use rsync to upload the results to a webserver."""

    config_key = 'upload'
    ssh_port_key = 'ssh_port'
    ssh_port_default = '22'
    source_dir_key = 'source_dir'
    source_dir_default = ''
    user_key = 'user'
    user_default = ''
    server_key = 'server'
    server_default = ''
    remote_path_key = 'remote_path'
    remote_path_default = ''
    rsync_options_key = 'rsync_options'
    rsync_options_default = ''

    def __init__(self, *args, **kwargs):
        self.ssh_port = self.ssh_port_default
        self.source_dir = self.source_dir_default
        self.user = self.user_default
        self.server = self.server_default
        self.remote_path = self.remote_path_default
        self.rsync_options = self.rsync_options_default
        super().__init__(*args, **kwargs)

    def _load_config(self):
        """Load task options from the config file."""
        ssh_port = self.config_file.get(self.config_key, self.ssh_port_key)
        if ssh_port is not None:
            self.ssh_port = ssh_port
        source_dir = self.config_file.get(self.config_key, self.source_dir_key)
        if source_dir is not None:
            self.source_dir = self.sanitize_path(source_dir)
            if source_dir[-1] == "/":
                self.source_dir = self.source_dir + "/"
        user = self.config_file.get(self.config_key, self.user_key)
        if user is not None:
            self.user = user
        server = self.config_file.get(self.config_key, self.server_key)
        if server is not None:
            self.server = server
        remote_path = self.config_file.get(self.config_key,
                                           self.remote_path_key)
        if remote_path is not None:
            # note: cannot sanitize remote path
            self.remote_path = remote_path
        rsync_options = self.config_file.get(self.config_key,
                                             self.rsync_options_key)
        if rsync_options is not None:
            self.rsync_options = rsync_options
        super()._load_config()

    def __call__(self, *args, **kwargs):
        self.vprint('Starting Upload Task.')
        super().__call__(*args, **kwargs)
        command = 'rsync -e "ssh -p %s" %s %s %s@%s:%s' % (
            self.ssh_port, self.rsync_options, self.source_dir, self.user,
            self.server, self.remote_path)
        self.dprint('command: %s' % command)
        subprocess.check_call(command, shell=True)
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        for indent, key, val in [
                (self.indent, self.ssh_port_key, self.ssh_port),
                (self.indent, self.source_dir_key, self.source_dir),
                (self.indent, self.user_key, self.user),
                (self.indent, self.server_key, self.server),
                (self.indent, self.remote_path_key, self.remote_path)]:
            msg += self.msg_template % (indent, key, val)
        return msg

    @property
    def default_config(self):
        """Return a string of the default example section for the config file.
        """
        config = "[%s]\n" % self.config_key
        for indent, key, val in [
                (self.indent, self.ssh_port_key, self.ssh_port_default),
                (self.indent, self.source_dir_key, self.source_dir_default),
                (self.indent, self.user_key, self.user_default),
                (self.indent, self.server_key, self.server_default),
                (self.indent, self.remote_path_key, self.remote_path_default)]:
            config += self.msg_template % (indent, key, val)
        return config
