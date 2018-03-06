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
"""Git Log Pages Task."""

import os
import time
import subprocess
from collections import OrderedDict

import escadrille.rst as rst

from .core import Task
from .options import OutputDirOpt


class GitLogPagesTask(OutputDirOpt, Task):
    """Make RST source pages out of Git Repository Logs."""

    config_name = 'git_log_pages'
    repos_default = {}

    def __init__(self, *args, **kwargs):
        """Set up defaults for Git Log Pages Task instances."""
        self.repos = self.repos_default
        super().__init__(*args, **kwargs)

    def _load_config(self):
        """Load task options from the config file."""
        super()._load_config()
        self.repos = self.repos_default
        for option in self.config_file.section(self.tag):
            self.dprint('Loading option %s' % option)
            if option in [OutputDirOpt.output_dir_key, 'task']:
                continue
            self.repos[option] = os.path.abspath(os.path.expanduser(
                self.config_file.get(self.tag, option)))

    def read_git_log(self, path):
        """Return a string representing git log output.

        Ensure that the log is RST compatible by using the "raw" directive to
        force the log to be preformatted text.
        """
        log = "::\n\n"
        command = "git -C %s log --decorate=no | sed 's/<.*>//g'" % path
        output = subprocess.getoutput(command).replace('\n', '\n    ')
        log += '    ' + output
        return log + "\n\n[End of log]"

    def construct_log_page(self, path, title):
        """Build an write a log page with the given options.

        Path is the path to the repository that the log will be created from.
        Title is the string used for the RST Document title.
        """
        page = rst.title(title, underline_char=rst.SECTION_LEVELS[0],
                         top_line=True)
        metavars = OrderedDict()
        metavars['date'] = time.strftime(self.config_file.date_format)
        metavars['summary'] = ("A log of activity from the %s repository." %
                               title.lower())
        page += rst.metadata(metavars) + rst.HORIZONTAL_RULE
        return page + self.read_git_log(path)

    def write_log_page(self, page, output_filename):
        """Write a page stringe to a file."""
        with open(output_filename, 'w') as fout:
            fout.write(page)

    def __call__(self, *args, **kwargs):
        """Execute the Git Log Pages Task."""
        print('Starting Git Log Pages Task.')
        super().__call__(*args, **kwargs)
        for repo in self.repos:
            if repo == OutputDirOpt.output_dir_key:
                continue
            # TODO: add filename suffix to config file
            output_filename = os.path.join(self.output_dir, "%s_log.rst" %
                                           repo)
            title = "%s log" % repo.title()
            self.vprint('Writing Log File %s: %s' % (title, output_filename))
            page = self.construct_log_page(self.repos[repo], title)
            self.write_log_page(page, output_filename)
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += self.config_snippet_name
        msg += self.config_snippet_output_dir
        msg += str(self.repos) + "\n"
        return msg

    @property
    def default_config(self):
        """Return a string of default example section for config file."""
        config = "[%s_tag]\n" % self.config_name
        config += self.config_snippet_name
        config += self.msg_template % (self.indent, self.output_dir_key,
                                       self.output_dir_default)
        comment = ['Add key pairs for each repository (repo_name=repo_path)']
        config += '; %s\n\n' % '\n; '.join(comment)
        return config
