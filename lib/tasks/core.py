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

import enum
import pkgutil
import inspect


def find_tasks(module, prefix):
    """Return an enum of config file tasks maping names to task callables."""
    print('finding tasks in %s (prefix: %s)' % (module, prefix))
    task_map = {}
    for importer, modname, ispkg in pkgutil.walk_packages([module], prefix):
        print('inspecting module %s' % modname)
        if ispkg:
            continue
        module = importer.find_module(modname).load_module(modname)
        for name, cls in inspect.getmembers(module, inspect.isclass):
            print('Checking class %s' % name)
            if issubclass(cls, Task) and cls != Task:
                task_map[name] = cls
    return enum.Enum('tasks', task_map)


class Task(object):
    """Base Task object for Squadron.

    The config_key attribute is used to reference the tasks from the config
    file.
    The __init__ and __call__ methods should be implemented by the subclasses.
    """

    config_key = 'noop'

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass
