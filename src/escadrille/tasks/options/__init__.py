"""tasks.options package.

.. note:

    It has been decided to use a more static package construction here
    compared to what is used inside "../tasks/__init__.py" because the options
    should be more static than the Tasks themselves are intended to be.
"""
from . import general_dirs
from . import other_dirs
from . import output_dir

GeneralDirsOpt = general_dirs.GeneralDirsOpt
OtherDirsOpt = other_dirs.OtherDirsOpt
OutputDirOpt = output_dir.OutputDirOpt

__ALL__ = [GeneralDirsOpt, OtherDirsOpt, OutputDirOpt]
