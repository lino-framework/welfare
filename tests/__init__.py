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
execfile(ROOTDIR.child('lino_welfare','project_info.py'),globals())

from djangosite.utils.pythontest import TestCase


class BaseTestCase(TestCase):
    project_root = ROOTDIR


class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """
    def test_admin(self):
        self.run_django_manage_test()

    
class DocsTests(BaseTestCase):
    
    def test_general(self):
        return self.run_docs_doctests('tested/general.rst')

    def test_newcomers(self): return self.run_docs_doctests('tested/newcomers.rst')
    def test_misc(self): return self.run_docs_doctests('tested/misc.rst')
    def test_debts(self): return self.run_docs_doctests('tested/debts.rst')
    def test_cbss(self): return self.run_docs_doctests('tested/cbss.rst')
    def test_pcsw(self): return self.run_docs_doctests('tested/pcsw.rst')
    def test_courses(self): return self.run_docs_doctests('tested/courses.rst')
    def test_jobs(self): return self.run_docs_doctests('tested/jobs.rst')

    def test_packages(self): self.run_packages_test(SETUP_INFO['packages'])

