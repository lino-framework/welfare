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

ROOTDIR = Path(__file__).parent.parent

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_welfare.settings.test"

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino_welfare', 'project_info.py'), globals())

from djangosite.utils.pythontest import TestCase


class BaseTestCase(TestCase):
    project_root = ROOTDIR


class DjangoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DjangoTests.test_docs
    """
    def test_docs(self):
        self.run_django_manage_test('lino_welfare/projects/docs')
    
    # def test_eupen(self):
    #     self.run_django_manage_test('lino_welfare/projects/eupen')

    # def test_chatelet(self):
    #     self.run_django_manage_test('lino_welfare/projects/chatelet')

    
class SimpleTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])


class DocsTests(BaseTestCase):
    
    def test_integ(self):
        return self.run_docs_doctests('tested/integ.rst')

    def test_general(self):
        return self.run_docs_doctests('tested/general.rst')

    def test_newcomers(self):
        return self.run_docs_doctests('tested/newcomers.rst')

    def test_misc(self):
        return self.run_docs_doctests('tested/misc.rst')

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

