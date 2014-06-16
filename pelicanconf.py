#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import time

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
SITE_LOGS = ["blog", "fret"]
LOG_PATH = "pages/%s-log.html"
LAST_UPDATED = time.strftime(DEFAULT_DATE_FORMAT)

DEFAULT_LANG = u'en'

THEME = 'theme/bootstrap'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

# Menu
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = (('links for later', SITEURL+'/pages/links-for-later.html'),
             ('songs to learn', SITEURL+'/pages/songs-to-learn.html'),
             ('what\'s interesting?', SITEURL+'/pages/whats-interesting.html'))

# LINKS go in the sidebar
LINKS = (('tags', 'http://curtissand.com/cs/tags.html'),
         ('archives', 'http://curtissand.com/cs/archives.html'),
         )

# FOOTER_LINKS go in the footer
FOOTER_LINKS = (('About this Site', SITEURL+'/pages/site.html'),
                ('Pelican', "http://getpelican.com/"),
                ('Twitter Bootstrap', 'http://twitter.github.com/bootstrap/'),
                ('Magnific Popup', 'http://dimsemenov.com/plugins/magnific-popup/'),
                )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PDF_GENERATOR = False

# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', 'style' ]

# tag cloud
TAG_CLOUD_SAYING = "Random Tags"
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SIZE = 5

JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols']
