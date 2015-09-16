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


class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests
    """

    def test_std(self):
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


class AdminTests(BaseTestCase):
    def test_printing(self):
        return self.run_simple_doctests('docs/admin/printing.rst')


class SpecsTests(BaseTestCase):
    def test_chatelet(self):
        return self.run_simple_doctests('docs/specs/chatelet.rst')

    def test_art61(self):
        return self.run_simple_doctests('docs/specs/art61.rst')

    def test_tasks(self):
        return self.run_simple_doctests('docs/specs/tasks.rst')

    def test_choicelists(self):
        return self.run_simple_doctests('docs/specs/choicelists.rst')

    def test_ledger(self):
        return self.run_simple_doctests('docs/specs/ledger.rst')

    def test_clients(self):
        return self.run_simple_doctests('docs/specs/clients.rst')

    def test_cal(self):
        return self.run_simple_doctests('docs/specs/cal.rst')

    def test_countries(self):
        return self.run_simple_doctests('docs/specs/countries.rst')

    def test_households(self):
        return self.run_simple_doctests('docs/specs/households.rst')

    def test_integ(self):
        return self.run_simple_doctests('docs/specs/integ.rst')

    def test_main(self):
        return self.run_simple_doctests('docs/specs/main.rst')

    def test_uploads(self):
        return self.run_simple_doctests('docs/specs/uploads.rst')

    def test_dupable(self):
        return self.run_simple_doctests('docs/specs/dupable_clients.rst')

    def test_plausibility(self):
        return self.run_simple_doctests('docs/specs/plausibility.rst')

    def test_users(self):
        return self.run_simple_doctests('docs/specs/users.rst')

    def test_ddh(self):
        return self.run_simple_doctests('docs/specs/ddh.rst')

    def test_excerpts(self):
        return self.run_simple_doctests('docs/specs/excerpts.rst')

    def test_addresses(self):
        return self.run_simple_doctests('docs/specs/addresses.rst')

    def test_immersion(self):
        return self.run_simple_doctests('docs/specs/immersion.rst')

    def test_clients_eupen(self):
        return self.run_simple_doctests('docs/specs/clients_eupen.rst')

    def test_cv2(self):
        return self.run_simple_doctests('docs/specs/cv2.rst')

    def test_polls(self):
        return self.run_simple_doctests('docs/specs/polls.rst')

    def test_general(self):
        return self.run_simple_doctests('docs/specs/general.rst')

    def test_eupen(self):
        return self.run_simple_doctests('docs/specs/eupen.rst')

    def test_misc(self):
        return self.run_simple_doctests('docs/specs/misc.rst')

    def test_aids(self):
        return self.run_simple_doctests('docs/specs/aids.rst')

    def test_pcsw(self):
        return self.run_simple_doctests('docs/specs/pcsw.rst')

    def test_jobs(self):
        return self.run_simple_doctests('docs/specs/jobs.rst')

    def test_reception(self):
        return self.run_simple_doctests('docs/specs/reception.rst')

    def test_newcomers(self):
        return self.run_simple_doctests('docs/specs/newcomers.rst')

    def test_debts(self):
        return self.run_simple_doctests('docs/specs/debts.rst')

    def test_notes(self):
        return self.run_simple_doctests('docs/specs/notes.rst')

    def test_courses(self):
        return self.run_simple_doctests('docs/specs/courses.rst')

    def test_courses2(self):
        return self.run_simple_doctests('docs/specs/courses2.rst')


class DocsTests(BaseTestCase):
    
    def test_autoevents(self):
        return self.run_simple_doctests('docs/tour/autoevents.rst')

    def test_aids_de(self):
        return self.run_simple_doctests('docs_de/aids.rst')

    def test_cbss(self):
        return self.run_docs_doctests('specs/cbss.rst')

    def test_20150219(self):
        return self.run_simple_doctests('docs/tested/2015/0219.rst')

    def test_20150715(self):
        return self.run_simple_doctests('docs/tested/2015/0715.rst')

    def test_20150717(self):
        return self.run_simple_doctests('docs/tested/2015/0717.rst')



