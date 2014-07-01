#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://curtissand.com/cs/'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

FEED_DOMAIN = SITEURL
FEED_MAX_ITEMS = 100
FEED_ALL_RSS = 'all.rss.xml'

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
