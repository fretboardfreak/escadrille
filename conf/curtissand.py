#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import time
from os.path import join

AUTHOR = u'Curtis Sand'
ABOUT_AUTHOR_URL = "pages/about-me.html"
SITENAME = u'Quizzical Silicon'
SITESUBTITLE=u'A charge carrier is not a wallet.'
SITEURL = 'http://curtissand.com/cs'
SITETHUMBNAIL_URL = SITEURL + '/images/site_thumb.jpg'
SITETHUMBNAIL_ALTTEXT = "Mah Guitjo!"
FOOTER_TEXT='Powered by pain and suffering, reading, beer and the sun.'

TIMEZONE = 'America/Edmonton'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M'

ABOUT_SITE_URL = "pages/about-the-site.html"
SITE_LOGS = ["blog", "fret", "music"]
LOG_PATH = "pages/%s-log.html"
LAST_UPDATED = time.strftime(DEFAULT_DATE_FORMAT)
WITH_FUTURE_DATES = False

DEFAULT_LANG = u'en'

THEME = 'theme/fretstrap'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

# Menu
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = (#('songs to learn', SITEURL+'/pages/songs-to-learn.html'),
             ('what\'s interesting?', SITEURL+'/pages/whats-interesting.html'),
             ('links', SITEURL+'/pages/links.html'))

# LINKS go in the sidebar
LINKS = (('More Tags',      join(SITEURL, 'tags.html')),
         ('Archives',       join(SITEURL, 'archives.html')),
         ('About Me',       join(SITEURL, 'about-me.html')),
         ('About the Site', join(SITEURL, 'about-the-site.html')),
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

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PDF_GENERATOR = False

# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'style' ]

# tag cloud
TAG_CLOUD_SAYING = "Random Tags"
TAG_CLOUD_STEPS = 10
TAG_CLOUD_MAX_ITEMS = 15
TAG_CLOUD_SIZE = 15

JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols']

PYGMENTS_RST_OPTIONS = {'linenos': 'table'}
