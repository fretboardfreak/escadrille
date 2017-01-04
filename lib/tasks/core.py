# Copyright 2016 Curtis Sand <curtissand@gmail.com>
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

from lib.cmdline import dprint
from lib.cmdline import vprint


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


class Task(object):
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

    config_key = 'noop'

    # constant for easy output formatting
    indent = '  '

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.warnings, self.errors, self.status = None, None, None
        self._clear_status()
        self.load_from_config()

    def load_from_config(self):
        """A method that can be subclassed to load info from the config file.
        """
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

    def __call__(self, *args, **kwargs):
        self._clear_status()

    def debug_msg(self):
        """If supported, generate and return a debug string."""
        return "%s Debug" % self.__class__.__name__

    @property
    def default_config(self):
        """Return a string of the default example section for the config file.
        """
        pass

    def dprint(self, msg):
        """Call the conditional debug print method."""
        dprint(msg)

    def vprint(self, msg):
        """Call the conditional verbose print method."""
        vprint(msg)
