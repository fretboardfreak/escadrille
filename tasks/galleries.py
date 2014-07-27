#!/usr/bin/env python

""" Create simple gallery pages for each directory in content_dir/images/
"""

import sys, os.path
import commands # rather dirty but quick for these scripts
from argparse import ArgumentParser

_DEST = "pages/galleries/"

GALLERY_START = '\n.. raw:: html\n\n    <div class="gallery">\n\n'
GALLERY_END = '\n.. raw:: html\n\n    </div>\n\n'

def get_content_dir():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(dest='content_dir')
    args = parser.parse_args()
    return os.path.abspath(args.content_dir)

def get_galleries(content_dir):
    image_root = os.path.join(content_dir, 'images')
    cmd = "find %s -type d" % image_root
    image_dirs = commands.getoutput(cmd).split('\n')
    galleries = {} # name: image_dir, ...
    for img_dir in image_dirs:
        name = img_dir.replace(image_root, '')
        name.replace('/', ' - ')
        if name == '':
            name = "Images"
        if name[0] == '/':
            name = name[1:]
        galleries[name] = img_dir.replace(content_dir, '.')
    return galleries

def get_image_directive(src, alt_text):
    return """
.. image:: %s
    :alt: %s
    :width: 300
    :align: center
""" % (src, alt_text)

def write_gallery(write, name, content_dir, img_dir):
    print "    %s : %s" % (name, img_dir)
    write('=' * len(name))
    write('\n%s\n' % name)
    write('=' * len(name))
    write('\n' + GALLERY_START)
    imgs = commands.getoutput('find %s -iname "*.jpg"' %
                              os.path.join(content_dir, img_dir)).split('\n')
    imgs.sort()
    for img in imgs:
        _, alt_text = os.path.split(img)
        write('\n%s' % get_image_directive(img, alt_text))
    write('\n' + GALLERY_END)

def main():
    prog = sys.argv[0]
    print "%s: building galleries" % prog
    content_dir = get_content_dir()
    for name, img_dir in get_galleries(content_dir).iteritems():
        dest = "%s.rst" % os.path.join(content_dir,
                                       _DEST,
                                       name.replace(' ', ''))
        try:
            os.makedirs(os.path.dirname(dest))
        except OSError, exc:
            if exc.errno != 17:
                raise
        print "Writing %s" % dest
        with open(dest, 'w') as fout:
            write_gallery(fout.write, name, content_dir, img_dir)



if __name__=="__main__":
    sys.exit(main())
