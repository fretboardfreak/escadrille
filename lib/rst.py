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
"""A simple library to help generate valid reStructuredText source."""


SECTION_LEVELS = ['=', '_', '-', "'", '"', '^', "#", '*']
HORIZONTAL_RULE = '\n\n----\n\n'


def title(text, underline_char=None, top_line=False):
    """Format a string as an RST section title."""
    if not underline_char:
        underline_char = SECTION_LEVELS[0]
    text = text.strip()
    underline = underline_char * len(text)
    ret_val = ""
    if top_line:
        ret_val += underline + '\n'
    ret_val += text + '\n'
    ret_val += underline + '\n\n'
    return ret_val


def metadata(data):
    """Convert a dictionary of strings into an RST metadata block."""
    template = ":%s: %s\n"
    return ''.join(template % (key, data[key]) for key in data)
