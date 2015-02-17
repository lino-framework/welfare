# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = "lino_welfare.settings.test"

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
            'lino_welfare', 'projects', 'std').absolute()
        self.run_django_manage_test(cwd)
    
    def test_eupen(self):
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'eupen').absolute()
        self.run_django_manage_test(cwd)

    def test_chatelet(self):
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'chatelet').absolute()
        self.run_django_manage_test(cwd)


class PackagesTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(lino_welfare.SETUP_INFO['packages'])


class DocsTests(BaseTestCase):
    
    def test_households(self):
        return self.run_simple_doctests('docs/tested/households.rst')

    def test_integ(self):
        return self.run_simple_doctests('docs/tested/integ.rst')

    def test_main(self):
        return self.run_simple_doctests('docs/tested/main.rst')

    def test_uploads(self):
        return self.run_simple_doctests('docs/tested/uploads.rst')

    def test_dedupe(self):
        return self.run_simple_doctests('docs/tested/dedupe.rst')

    def test_users(self):
        return self.run_simple_doctests('docs/tested/users.rst')

    def test_excerpts(self):
        return self.run_simple_doctests('docs/tested/excerpts.rst')

    def test_immersion(self):
        return self.run_simple_doctests('docs/tested/immersion.rst')

    def test_cv2(self):
        return self.run_simple_doctests('docs/tested/cv2.rst')

    def test_polls(self):
        return self.run_simple_doctests('docs/tested/polls.rst')

    def test_general(self):
        return self.run_simple_doctests('docs/tested/general.rst')

    def test_aids_de(self):
        return self.run_simple_doctests('docs_de/aids.rst')

    def test_aids(self):
        return self.run_simple_doctests('docs/tested/aids.rst')

    def test_pcsw(self):
        return self.run_simple_doctests('docs/tested/pcsw.rst')

    def test_jobs(self):
        return self.run_simple_doctests('docs/tested/jobs.rst')

    def test_reception(self):
        return self.run_simple_doctests('docs/tested/reception.rst')

    def test_newcomers(self):
        return self.run_simple_doctests('docs/tested/newcomers.rst')

    def test_misc(self):
        return self.run_docs_doctests('tested/misc.rst')

    def test_debts(self):
        return self.run_docs_doctests('tested/debts.rst')

    def test_cbss(self):
        return self.run_docs_doctests('tested/cbss.rst')

    def test_courses(self):
        return self.run_docs_doctests('tested/courses.rst')

