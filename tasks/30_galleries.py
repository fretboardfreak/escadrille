#!/usr/bin/env python

""" Create simple gallery pages for each directory in content_dir/images/
"""

import sys, os.path
import commands # rather dirty but quick for these scripts
from argparse import ArgumentParser

_DEST = "galleries/"

GALLERY_START = '\n.. raw:: html\n\n    <div class="gallery">\n\n'
GALLERY_END = '\n.. raw:: html\n\n    </div>\n\n'

PAGE_SOURCES = "../fret/galleries/"

PROG = ''

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
        galleries[name] = img_dir
    return galleries

def get_image_directive(src, alt_text):
    return """
.. image:: %s
    :alt: %s
    :width: 300
    :align: center
""" % (src, alt_text)

def get_title(title_name):
    val = '=' * len(title_name)
    val += '\n%s\n' % title_name
    val += '=' * len(title_name)
    return val

def get_page(fname, title):
    if os.path.exists(fname):
        with open(fname, 'r') as fin:
            return fin.read()
    else:
        return (get_title(title) +
                "\n\n:summary:\n:date: 1900-01-01 01:01\n\n")

def write_gallery(write, name, content_dir, img_dir):
    title_name = name.replace('/', ' - ')
    _name = name.replace('/', '-')
    url = os.path.join(_DEST, "%s.html" % _name)
    fname = os.path.join(PAGE_SOURCES, "%s.rst" % _name)

    write(get_page(fname, title_name))
    write('\n:save_as: ' + url + '\n' + GALLERY_START + '\n')
    imgs = commands.getoutput('find %s -iname "*.jpg" -o -iname "*.png"' %
                              img_dir).split('\n')
    imgs.sort()
    for img in imgs:
        _, alt_text = os.path.split(img)
        img = img.replace(content_dir, '../..')
        write('\n%s' % get_image_directive(img, alt_text))
    write('\n' + GALLERY_END)

def main():
    global PROG
    _, PROG = os.path.split(sys.argv[0])
    print "%s: building galleries" % PROG
    content_dir = get_content_dir()
    for name, img_dir in get_galleries(content_dir).iteritems():
        fname = name.replace(' ', '')
        fname = fname.replace('/', '-')
        dest = "%s.rst" % os.path.join(content_dir, _DEST, fname)
        try:
            os.makedirs(os.path.dirname(dest))
        except OSError, exc:
            if exc.errno != 17:
                raise
        print "%s: Writing %s" % (PROG, dest)
        with open(dest, 'w') as fout:
            write_gallery(fout.write, name, content_dir, img_dir)

if __name__=="__main__":
    sys.exit(main())
