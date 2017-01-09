# Copyright 2016-2017 Curtis Sand <curtissand@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tasks core library."""

import pkgutil
import inspect

from lib.verbosity import dprint
from lib.verbosity import vprint


def find_tasks(module, prefix):
    """Return an enum of config file tasks maping names to task callables."""
    dprint('lib.tasks.core: finding tasks in %s (prefix: %s)' %
           (module, prefix))
    task_map = {}
    for importer, modname, ispkg in pkgutil.walk_packages([module], prefix):
        if ispkg:
            continue
        module = importer.find_module(modname).load_module(modname)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, Task) and cls != Task:
                task_map[cls.config_key] = cls
    return task_map


class TaskCore(object):
    """An internal class that can be shared by option mixins and Task objects.
    """

    config_key = 'noop'

    # constant for easy output formatting
    indent = '  '

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.warnings, self.errors, self.status = None, None, None
        self._clear_status()
        self.loaded = False

    def load_config(self):
        """A method that can be subclassed to load info from the config file.
        """
        if not self.loaded:
            self.dprint('Loading the config for %s.' % self.config_key)
            self._load_config()
        self.loaded = True

    def _load_config(self):
        """An internal method for subclasses to load their config values."""
        pass

    def _clear_status(self):
        """Reset the warnings and errors lists and the status code."""
        self.warnings = []
        self.errors = []
        self.status = None

    def _set_status(self):
        """Set the error status to the length of the warnings and errors lists.
        """
        self.status = len(self.errors)

    def dprint(self, msg):
        """Call the conditional debug print method."""
        dprint(msg)

    def vprint(self, msg):
        """Call the conditional verbose print method."""
        vprint(msg)


class Task(TaskCore):
    """Base Task object for Squadron.

    The config_key attribute is used to reference the tasks from the config
    file.

    The __init__ and __call__ methods should be implemented by the subclasses.

    The constructor should configure the task with everything needed to perform
    the task. A well designed task does not have state and can therefore be
    repeated. The task subclass needs to implement any checks or validation
    required to operation in this way.

    The call method clears the "warnings", "errors" and "status" attributes
    before starting the task and then can use the "_set_status" method to
    update the status appropriately at the end of the task.
    """

    def __init__(self, config_file=None):
        super().__init__(config_file)

    def __call__(self, *args, **kwargs):
        self._clear_status()
        self.load_config()
        self.dprint(self.debug_msg())

    def debug_msg(self):
        """If supported, generate and return a debug string."""
        self.load_config()
        return "%s Debug" % self.__class__.__name__

    @property
    def default_config(self):
        """Return a string of the default example section for the config file.
        """
        self.load_config()
        return ""



class GeneralDirsOpt(TaskCore):
    """A mixin class for a config boolean option called "general_dirs"."""

    general_dirs_key = 'general_dirs'
    general_dirs_default = True

    def __init__(self, *args, general_dirs=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.general_dirs = self.general_dirs_default
        if general_dirs is not None:
            self.general_dirs = general_dirs

    def _load_config(self):
        """Load the general_dirs boolean from the config file."""
        general_dirs = self.config_file.getboolean(
            self.config_key, self.general_dirs_key)
        if general_dirs is None:
            self.general_dirs = self.general_dirs_default
        else:
            self.general_dirs = bool(int(general_dirs))
        super()._load_config()

    @property
    def config_snippet_general_dirs(self):
        """Return a string representing the general_dirs config option."""
        return ("%s%s: %s\n" % (self.indent, self.general_dirs_key,
                                self.general_dirs))


class OtherDirsOpt(TaskCore):
    """A mixin class for a config list option called "other_dirs"."""

    other_dirs_key = 'other_dirs'
    other_dirs_default = []

    def __init__(self, *args, other_dirs=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_dirs = self.other_dirs_default
        if other_dirs is not None:
            self.other_dirs = other_dirs

    def _load_config(self):
        """Load the other_dirs list from the config file."""
        other_dirs_val = self.config_file.get(
            self.config_key, self.other_dirs_key)
        if other_dirs_val is None:
            self.other_dirs = self.other_dirs_default
        else:
            self.other_dirs = [path for path in
                               other_dirs_val.split(self.config_file.list_sep)
                               if path != '']
        super()._load_config()

    @property
    def config_snippet_other_dirs(self):
        """Return a string representing the other_dirs config option."""
        return ("%s%s: %s\n" % (
            self.indent, self.other_dirs_key,
            self.config_file.list_sep.join(self.other_dirs)))


class OutputDirOpt(TaskCore):
    """A mixin class to provide a Task object with an Output Dir config value.
    """

    output_dir_key = 'output_dir'

    def __init__(self, *args, output_dir=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_dir = self.output_dir_default
        if output_dir is not None:
            self.output_dir = output_dir

    @property
    def output_dir_default(self):
        """Default value is based on existing option in general section."""
        return self.config_file.staging_dir

    def _load_config(self):
        """Load the output dir path option from the config file."""
        output_dir = self.config_file.get(self.config_key, self.output_dir_key)
        if output_dir is None:
            self.output_dir = self.output_dir_default
        else:
            self.output_dir = output_dir.strip()
        super()._load_config()

    @property
    def config_snippet_output_dir(self):
        """Return a string representing the output_dir config option."""
        return ("%s%s: %s\n" % (self.indent, self.output_dir_key,
                                self.output_dir))
