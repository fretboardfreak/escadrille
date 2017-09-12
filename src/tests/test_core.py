# Copyright 2017 Curtis Sand <curtissand@gmail.com>
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
"""Tests for escadrille's core module."""
import unittest

import escadrille.core as core


class TestInterfaceCore(unittest.TestCase):
    """Test the logic of escadrille.core.InterfaceCore"""

    def setUp(self):
        """Configure the test case for each unittest."""
        self.test_obj = core.InterfaceCore()

    def test_required_methods(self):
        """Ensure the core object has the required methods."""
        missing = []
        required_methods = ['build', 'validate_args', '_main', 'config_file',
                            'tasks', 'skip', 'list_tasks']

        for method_name in required_methods:
            if method_name not in dir(self.test_obj):
                missing.append(method_name)
        if missing:
            self.fail('The InterfaceCore test object is missing: %s' %
                      ', '.join(missing))
