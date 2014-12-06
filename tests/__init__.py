# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_welfare.settings.test"

from lino.utils.pythontest import TestCase

import lino_welfare


class BaseTestCase(TestCase):
    project_root = Path(__file__).parent.parent


class ProjectsTests(BaseTestCase):
    """
    $ python setup.py test -s tests.ProjectsTests
    """
    def test_docs(self):
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'docs', 'tests').absolute()
        self.run_subprocess([cwd.child('run_tests.sh')], cwd=cwd)
    
    def test_eupen(self):
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'eupen', 'tests').absolute()
        self.run_subprocess([cwd.child('run_tests.sh')], cwd=cwd)

    # def test_chatelet(self):
    #     self.run_django_manage_test('lino_welfare/projects/chatelet')

    
class SimpleTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(lino_welfare.SETUP_INFO['packages'])


class DocsTests(BaseTestCase):
    
    def test_households(self):
        return self.run_simple_doctests('docs/tested/households.rst')

    def test_integ(self):
        return self.run_simple_doctests('docs/tested/integ.rst')

    def test_general(self):
        return self.run_simple_doctests('docs/tested/general.rst')

    def test_newcomers(self):
        return self.run_docs_doctests('tested/newcomers.rst')

    def test_misc(self):
        return self.run_docs_doctests('tested/misc.rst')

    def test_aids_de(self):
        return self.run_simple_doctests('docs_de/aids.rst')

    def test_aids(self):
        return self.run_simple_doctests('docs/tested/aids.rst')

    def test_debts(self):
        return self.run_docs_doctests('tested/debts.rst')

    def test_cbss(self):
        return self.run_docs_doctests('tested/cbss.rst')

    def test_pcsw(self):
        return self.run_simple_doctests('docs/tested/pcsw.rst')

    def test_courses(self):
        return self.run_docs_doctests('tested/courses.rst')

    def test_jobs(self):
        return self.run_simple_doctests('docs/tested/jobs.rst')

