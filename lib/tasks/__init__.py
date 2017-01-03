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
"""Tasks package provides procedures that can be composed to build a website.

Rather than hardcoding the list of available Tasks, the find_tasks method
provides a mechanism for searching the tasks package for appropriate task
objects.
"""
import os

from . import core


TASK_PATH, _ = os.path.split(core.__file__)
TASK_PREFIX = core.__package__ + '.'


def load_tasks():
    """Wrap tasks.core.find_tasks with the required arguments."""
    return core.find_tasks(TASK_PATH, TASK_PREFIX)
