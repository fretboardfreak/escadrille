========
Squadron
========

:author: Curtis Sand <curtissand@gmail.com>

:homepage: http://www.fretboardfreak.com/squadron/

Squadron:
    A flock of pelicans.

Originally the idea was to provide automation around the python based
``pelican`` website generator tool. Now it is the system that keeps my website
running.

Written in python 3, squadron is a system of python modules that can be
composed via an INI format configuration file to create various custom
websites. Squadron operates by performing tasks that are specified within the
configuration file. Some tasks perform very basic operations like making
directories or copying files around. Other tasks perform higher level
operations such as generating RST source pages from various source content (git
repository log, directories of images, etc.).
