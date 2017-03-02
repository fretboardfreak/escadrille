=====================
Escadrille Change Log
=====================

- 0.2: TBD

  - Add command line flag "-s|--skip" to facilitate skipping one or more tasks
    without changing the configuration file.
  - Remove livefire widget from fretstrap theme.
  - Add command line flag "-l|--list" to list the enabled tasks within a config
    file.
  - combine the cmdline.py and top level core.py modules for a simpler API.
  - clean task: use short flags for the rm utility to improve compatibility.
    (The MacOS version of rm only accepts short flags.)

- 0.1: 170207

  - Achieve functional unity with old, fragile website automation.
  - Rename project to "Escadrille" meaning "small squadron" in French. This
    is required because PyPI already has a package called squadron, so I need
    to find something which hasn't already been used in order to upload my
    releases to PyPI and make them publically available.
  - Configure project to use setuptools.
