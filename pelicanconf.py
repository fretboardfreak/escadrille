#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Curtis Sand'
SITENAME = u'Quizical Silicon'
SITESUBTITLE=u'A charge carrier is not a wallet.'
SITEURL = 'http://curtissand.com/cs/'

TIMEZONE = 'America/Edmonton'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M'

DEFAULT_LANG = u'en'

THEME = 'theme/bootstrap'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

# Blogroll
LINKS =  (('tags', 'http://curtissand.com/cs/tags.html'),
          ('archives', 'http://curtissand.com/cs/archives.html'),
          )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 4

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PDF_GENERATOR = False

# static paths will be copied without parsing their contents
STATIC_PATHS = ['images', ]

# tag cloud
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
