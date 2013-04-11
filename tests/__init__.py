"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino_welfare','setup_info.py'),globals())

from atelier.test import SubProcessTestCase


class BaseTestCase(SubProcessTestCase):
    default_environ = dict(DJANGO_SETTINGS_MODULE="lino_welfare.demo.settings")
    project_root = ROOTDIR
    
class DocsTests(BaseTestCase):
    
    #~ env.docs_doctests.append('tested/misc.rst')
    #~ env.docs_doctests.append('tested/debts.rst')
    

    def test_docs(self): self.run_django_manage_test('docs')
    def test_misc(self): self.run_docs_doctests('tested/misc.rst')
    def test_debts(self): self.run_docs_doctests('tested/debts.rst')
    #~ def test_02(self): self.run_docs_django_tests('tested/debts.rst')
    


class PackagesTests(BaseTestCase):
    def test_packages(self): self.run_packages_test(SETUP_INFO['packages'])

