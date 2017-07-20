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
"""RST Image Galleries Task."""

import os
from collections import OrderedDict

import escadrille.rst as rst
from escadrille.verbosity import dprint

from .core import Task
from .options import OutputDirOpt


class GalleriesTask(OutputDirOpt, Task):
    """Make RST source pages for sets of images."""

    config_name = 'galleries'
    galleries_default = ""
    stubs_key = "stubs"
    stubs_default = {}
    stubs_dir_default = ""

    def __init__(self, *args, **kwargs):
        """Set up defaults for Galleries Task instances."""
        self.suffix = 'rst'  # TODO: add to general config file section
        self.galleries = self.galleries_default
        self.stubs_dir = self.stubs_dir_default
        self.stubs = self.stubs_default
        super().__init__(*args, **kwargs)

    def load_stubs(self):
        """Load a list of stub files from the directory in the config file."""
        stubs_dir = self.config_file.get(self.tag, self.stubs_key)
        if stubs_dir is None:
            self.stubs = self.stubs_default
            self.stubs_dir = self.stubs_dir_default
            return
        self.stubs = {}
        self.stubs_dir = os.path.abspath(os.path.expanduser(stubs_dir))
        # TODO: reimplement this to be recursive, not needed at this time
        for fname in os.listdir(self.stubs_dir):
            if fname.lower().endswith(self.suffix):
                name = fname.replace('.%s' % self.suffix, '')
                self.stubs[name] = os.path.join(self.stubs_dir, fname)

    def _load_config(self):
        """Load task options from the config file."""
        super()._load_config()
        galleries = self.config_file.get(self.tag, self.config_name)
        if galleries is None:
            self.galleries = self.galleries_default
        else:
            self.galleries = galleries
        self.load_stubs()

    def write_content(self, fout, title, path, fnames, thumbs=False):
        """Write the actual image content for the gallery pages."""
        for image in fnames:
            image_path = os.path.join(path, image)
            if thumbs:
                thumb_path = os.path.join(path, 'thumbs', image)
                if (thumb_path.endswith('jpg') or
                        thumb_path.endswith('JPG')):
                    thumb_path = thumb_path[:-3] + 'png'
                fout.write('    <a href="%s" data-lightbox="%s">'
                           '<img src="%s"/></a>\n' %
                           (image_path, title, thumb_path))
            else:
                thumb_path = image_path
                fout.write('    <a href="%s" data-lightbox="%s">'
                           '<img src="%s" style="width: 300px"/></a>\n' %
                           (image_path, title, thumb_path))

    def write_stubbed_gallery(self, title, path, fnames, thumbs=False):
        """Write an RST Gallery page using a pre-written stub file."""
        output_filename = os.path.join(self.output_dir,
                                       "%s.%s" % (title, self.suffix))
        self.dprint('  writing stubbed gallery: %s' % output_filename)
        with open(output_filename, 'w') as fout:
            with open(self.stubs[title], 'r') as stub_in:
                fout.write(stub_in.read())
            fout.write('\n.. raw:: html\n\n    <div class="gallery">\n\n')
            self.write_content(fout, title, path, fnames, thumbs)
            fout.write('\n.. raw:: html\n\n    </div>')

    def write_generated_gallery(self, title, path, fnames, thumbs=False):
        """Write an RST Gallery page from scratch using fallback metadata."""
        output_filename = os.path.join(self.output_dir,
                                       "%s.%s" % (title, self.suffix))
        self.dprint('  writing generated gallery: %s' % output_filename)
        with open(output_filename, 'w') as fout:
            fout.write(rst.title(title, underline_char=rst.SECTION_LEVELS[0],
                                 top_line=True))
            # TODO: add fallback metadata to config file
            metadata = OrderedDict()
            metadata['date'] = "1990-01-01 01:01"
            metadata['category'] = 'pics'
            metadata['tags'] = 'pics'
            metadata['summary'] = ''
            fout.write(rst.metadata(metadata))
            fout.write('\n.. raw:: html\n\n    <div class="gallery">\n\n')
            self.write_content(fout, title, path, fnames, thumbs)
            fout.write('\n.. raw:: html\n\n    </div>')

    def __call__(self, *args, **kwargs):
        """Execute the Galleries Task."""
        print('Starting Galleries Task.')
        super().__call__(*args, **kwargs)
        tmp = self.galleries
        self.galleries = tmp if tmp.endswith('/') else tmp + '/'
        for dirpath, dirnames, fnames in os.walk(self.galleries):
            dprint('GALLERY DIRPATH=%s' % dirpath)
            if dirpath.endswith('thumbs') or dirpath.endswith('thumbs/'):
                continue
            common_prefix = os.path.commonprefix([dirpath, self.galleries])
            relative_path = dirpath[len(common_prefix):]
            if relative_path == "":
                continue
            name = relative_path.replace('/', '-')
            media_prefix = './images'  # TODO: add to config file
            thumbs = False
            if "thumbs" in dirnames:
                thumbs = True
            cwd = '.'
            if cwd in fnames:
                fnames.remove(cwd)
            fnames.sort()
            path = os.path.join(media_prefix, relative_path)
            if len(fnames) == 0:
                self.vprint('Skipping %s, no images.' % name)
                continue
            self.vprint('Creating gallery: %s.%s - %s images' %
                        (name, self.suffix, len(fnames)))
            if name in self.stubs:
                self.write_stubbed_gallery(name, path, fnames, thumbs)
            else:
                self.write_generated_gallery(name, path, fnames, thumbs)
        self._set_status()

    def debug_msg(self):
        """Return some debug outut about the current state of the task."""
        msg = super().debug_msg() + "\n"
        msg += self.config_snippet_output_dir
        msg += "  %s: %s\n" % (self.config_name, self.galleries)
        msg += "  %s: %s\n" % (self.stubs_key, self.stubs)
        msg += "  stubs_dir: %s\n" % self.stubs_dir
        return msg

    @property
    def default_config(self):
        """Return a string of default example section for config file."""
        config = "[%s_tag]\n" % self.config_name
        config += self.config_snippet_name
        config += self.config_snippet_output_dir
        config += "  %s: %s\n" % (self.config_name, self.galleries_default)
        config += "  %s: %s\n" % (self.stubs_key, '')
        config += "  stubs_dir: %s\n" % self.stubs_dir_default
        return config
