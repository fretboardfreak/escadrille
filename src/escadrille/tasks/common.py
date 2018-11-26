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
"""Common code used by various tasks tasks."""

from escadrille.verbosity import dprint
from escadrille.verbosity import vprint


def build_output_input_file_pairs(top_path, path, fname):
    """Build the pair of output and input paths."""
    input_file_map = {}
    infile = os.path.join(path, fname)
    name_parts = fname.split('.')
    out_fname = '.'.join(name_parts[:-1] + ['pkl'])
    partial = path.replace(top_path, '')
    if partial.startswith('/'):
        partial = partial[1:]
    outfile = os.path.join(self.output_dir, partial,
                           out_fname)
    input_file_map[outfile] = infile
    return input_file_map
