"""The setuptools deployment script."""
# Copyright 2015 Curtis Sand
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
import os
import subprocess
import distutils.log
from distutils.cmd import Command
from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test


def install_requires():
    """Read the requirements for installing the project."""
    with open('requirements.txt', 'r') as reqf:
        return reqf.read().splitlines()


def tests_require():
    """Read the requirements for testing the project."""
    with open('dev_requirements.txt', 'r') as dev_req:
        return dev_req.read().splitlines()


def readme():
    """Read the readme file for the long description."""
    with open('README.rst', 'r') as readmef:
        return readmef.read()


class SetupCommand(Command):
    """Base command for distutils in the project."""

    def initialize_options(self):
        """Set defaults for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run the custom setup command."""
        # if self.distribution.install_requires:
        #     self.distribution.fetch_build_eggs(
        #         self.distribution.install_requires)

    def _run_command(self, command):
        """Execute the command."""
        self.announce('running command: %s' % str(command),
                      level=distutils.log.INFO)
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as exc:
            self.announce('Non-zero returncode "%s": %s' %
                          (exc.returncode, exc.cmd),
                          level=distutils.log.INFO)
            return 1

    @property
    def setup_path(self):
        """Get the path to the setup.py script."""
        return os.path.dirname(__file__)

    @property
    def software_package(self):
        """Get the path to the software parkace."""
        return os.path.join(self.setup_path, 'src/escadrille')

    @property
    def test_paths(self):
        """Get the list of paths for python files that should be tested."""
        return [self.software_package, __file__]


class DevelopmentCommand(SetupCommand):
    """Base command for project development and testing."""

    def run(self):
        """Run the custom dev/test commands."""
        super().run()
        # if self.distribution.tests_require:
        #     self.distribution.fetch_build_eggs(
        #         self.distribution.tests_require)


class PylintCommand(DevelopmentCommand):
    """A custom command to run Pylint on all Python source files."""

    description = "Run pylint on the python sources."
    user_options = [
        ('pylint-rcfile=', None, 'path to Pylint config file.')
    ]

    def initialize_options(self):
        """Set defaults for options."""
        self.pylint_rcfile = ''

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                'Cannot find config file "%s"' % self.pylint_rcfile)

    def run(self):
        """Prepare and run the Pylint command."""
        super().run()
        command = ['pylint']
        if self.pylint_rcfile:
            command.append('--rcfile=%s' % self.pylint_rcfile)
        command.extend(self.test_paths)
        self._run_command(command)


class Pep8Command(DevelopmentCommand):
    """A custom command to run pep8 on all python source files."""

    description = "Run pep8 on all python sources."
    user_options = []

    def run(self):
        """Run the pep8 checker."""
        super().run()
        self._run_command(['pep8', '--statistics', '--verbose'] +
                          self.test_paths)


class Pep257Command(DevelopmentCommand):
    """A custom command to run pep257 on all Python source files."""

    description = "Run pep257 on all python sources."
    user_options = []

    def run(self):
        """Run the pep257 checker."""
        super().run()
        self._run_command(['pep257', '--count', '--verbose'] +
                          self.test_paths)


class Test(test):
    """Combine unittest, pep8 and pylint checks all into one command."""

    description = "Run pep8, pylint and unittest commands together."
    user_options = [('interactive', 'i', 'Enable interactive pauses.')]

    def __init__(self, *args, **kwargs):
        self.interactive = None
        super().__init__(*args, **kwargs)

    def _interactive_pause(self):
        """Pause for the use to press enter. So interactive."""
        if self.interactive:
            input('enter to continue...')

    def run(self):
        """Run all tests and checkers for project."""
        # Skip parent method to avoid reinstalling packages
        # super().run()
        self.run_command('pep8')
        self._interactive_pause()
        self.run_command('pep257')
        self._interactive_pause()
        self.run_command('pylint')
        self._interactive_pause()


setup(
    name='escadrille',
    version='0.1',
    description='',
    long_description=readme(),
    url='https://github.com/fretboardfreak/escadrille',
    author='Curtis Sand',
    author_email='curtissand@gmail.com',
    license='Apache',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': ['escadrille=escadrille.core:CliInterface.main']
    },
    use_2to3=False,
    install_requires=install_requires(),
    zip_safe=True,
    include_package_data=True,
    # test_suite='escadrille.tests',
    tests_require=tests_require(),
    keywords='escadrille net html site website generator rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Documentation',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    cmdclass={
        'pylint': PylintCommand,
        'pep8': Pep8Command,
        # 'unittest': test,
        'pep257': Pep257Command,
        'test': Test})
