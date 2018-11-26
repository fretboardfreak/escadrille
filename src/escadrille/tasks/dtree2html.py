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
"""Task to publish RST files to a pickled doctree format."""

import os
import pickle

from docutils.core import publish_doctree
from docutils.io import FileInput

from .core import Task
from .options import OutputDirOpt


class Rst2dtreeTask(OutputDirOpt, Task):
    """Make doctree itermediary files from RST source files."""

    config_name = 'rst2dtree'
    inputs_key = 'inputs'
    inputs_default = {}  # output_file: input_file
    output_dir_default = ''

    def __init__(self, *args, **kwargs):
        """Set up defaults for Galleries Task instances."""
        # TODO: add suffix to general config file section
        self.suffix = 'rst'
        self.input_file_map = self.inputs_default
        self.dtree_key = 'dtrees'
        super().__init__(*args, **kwargs)

    def _load_config(self):
        """Load task options from the config file."""
        super()._load_config()
        self.load_input_output_pairs()

    def load_input_output_pairs(self):
        """Create a mapping of output to input files.

        Recursively search input directories for RST files.
        """
        inputs = self.config_file.get(self.tag, self.inputs_key)
        self.input_file_map = self.inputs_default
        for item in inputs.split(' '):
            sane_path = self.sanitize_path(item)
            if (os.path.isfile(sane_path) and
                    sane_path.endswith('.rst')):
                # input files are mapped directly to output dir
                path, fname = os.path.split(sane_path)
                self.build_output_input_pair(
                    sane_path, path, fname)
            elif os.path.isdir(sane_path):
                for path, dirs, files in os.walk(sane_path):
                    # skip hidden dirs
                    dirs = [dirname for dirname in dirs
                            if not dirname.startswith('.')]
                    for fname in files:
                        if fname.startswith('.'):
                            continue  # skip hidden files
                        if fname.endswith('.rst'):
                            self.build_output_input_pair(
                                sane_path, path, fname)
            else:
                print('Cannot load input "%s", skipping...' %
                      item)

    def build_output_input_pair(self, top_path, path, fname):
        """Build the pair of output and input paths."""
        infile = os.path.join(path, fname)
        name_parts = fname.split('.')
        out_fname = '.'.join(name_parts[:-1] + ['pkl'])
        partial = path.replace(top_path, '')
        if partial.startswith('/'):
            partial = partial[1:]
        outfile = os.path.join(self.output_dir, partial,
                               out_fname)
        self.input_file_map[outfile] = infile

    def __call__(self, *args, **kwargs):
        """Parse input files into doctree and pickle results."""
        print('Starting rst2dtree Task.')
        super().__call__(*args, **kwargs)
        dtree_map = {}
        for outfile in self.input_file_map:
            outdir, _ = os.path.split(outfile)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            with open(self.input_file_map[outfile], 'r') as fin:
                doctree = publish_doctree(
                    source=fin, source_class=FileInput)
            with open(outfile, 'wb') as fout:
                pickle.dump(doctree, fout)
            dtree_map[doctree['title']] = outfile
        self._set_status()
        self.shared_state[self.dtree_key] = dtree_map
        return self.shared_state

    def debug_msg(self):
        """Return debug output about current task state."""
        msg = super().debug_msg() + "\n"
        msg += self.config_snippet_output_dir
        msg += self.msg_template % (
            self.indent, self.inputs_key, str(self.input_file_map))
        return msg

    @property
    def default_config(self):
        """Return default example section for config file."""
        config = "[%s_tag]\n" % self.config_name
        config += self.config_snippet_name
        config += self.config_snippet_output_dir
        config += self.msg_template % (
            self.indent, self.inputs_key, ' ')
        return config
