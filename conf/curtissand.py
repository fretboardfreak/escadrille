#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import time
from os.path import join

AUTHOR = u'Curtis Sand'
SITENAME = u'Quizzical Silicon'
SITESUBTITLE=u'A charge carrier is not a wallet.'
SITEURL = 'http://curtissand.com/cs'
SITETHUMBNAIL_URL = SITEURL + '/images/site_thumb.jpg'
SITETHUMBNAIL_ALTTEXT = "Mah Guitjo!"
FOOTER_TEXT='Powered by pain and suffering, reading, beer and the sun. Curtis Sand, 2015. Unauthorized use and/or duplication of this material without express and written permission from this blog’s author and/or owner is strictly prohibited. Excerpts and links may be used, provided that full and clear credit is given to Curtis Sand and Quizzical Silicon with appropriate and specific direction to the original content.'

FAVICON=''

TIMEZONE = 'America/Edmonton'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M'

SITE_LOGS = ["blog", "fret", "music"]
LOG_PATH = "pages/%s-log.html"
LAST_UPDATED = time.strftime(DEFAULT_DATE_FORMAT)

DEFAULT_LANG = u'en'

THEME = 'theme/fretstrap'

TOC_PAGES = ["music", "pics", "ref"]

TWITTER_USERNAME = 'fretboardfreak'
GITHUB_URL = 'https://github.com/fretboardfreak'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

# Menu
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = (#('songs to learn', SITEURL+'/pages/songs-to-learn.html'),
             #('what\'s interesting?', SITEURL+'/pages/whats-interesting.html'),
             ('links', SITEURL+'/pages/links.html'),)

# LINKS go in the sidebar
LINKS = (('More Tags',      join(SITEURL, 'tags.html')),
         ('Archives',       join(SITEURL, 'archives.html')),
         ('About Me',       join(SITEURL, 'pages/about-me.html')),
         ('About the Site', join(SITEURL, 'pages/about-the-site.html')),
         ('RSS Feed',       join(SITEURL, 'all.rss.xml')),
         )

# FOOTER_LINKS go in the footer
FOOTER_LINKS = (('About this Site', SITEURL+'/pages/about-the-site.html'),
                ('Pelican', "http://getpelican.com/"),
                ('Twitter Bootstrap', 'http://twitter.github.com/bootstrap/'),
                ('Magnific Popup', 'http://dimsemenov.com/plugins/magnific-popup/'),
                ('Tag Cloud', 'http://addywaddy.github.io/jquery.tagcloud.js/'),
                )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 25

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PDF_GENERATOR = False

# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'style', 'js']

# tag cloud
TAG_CLOUD_SAYING = "Random Tags"
TAG_CLOUD_STEPS = 10
TAG_CLOUD_MAX_ITEMS = 15
TAG_CLOUD_SIZE = 15

JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols']

PYGMENTS_RST_OPTIONS = {'linenos': 'table'}
