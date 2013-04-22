"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino_welfare','setup_info.py'),globals())

from atelier.test import SubProcessTestCase
#~ from djangosite.utils.test import TestCase
"""
Note that we cannot import :mod:`djangosite.utils.test` here
because that's designed for unit tests within a particular Django project 
(run using `djange-admin test`).
"""
from djangosite.utils import testcase_setup



class BaseTestCase(SubProcessTestCase):
#~ class BaseTestCase(TestCase):
    default_environ = dict(DJANGO_SETTINGS_MODULE="lino_welfare.demo.settings")
    project_root = ROOTDIR
    
    def setUp(self):
        #~ settings.SITE.never_build_site_cache = self.never_build_site_cache
        #~ settings.SITE.remote_user_header = 'REMOTE_USER'
        testcase_setup.send(self)
        super(BaseTestCase,self).setUp()
    
    
class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """
    def test_admin(self): self.run_django_admin_test('lino_welfare.demo.settings')
    
class DocsTests(BaseTestCase):
    
    #~ env.docs_doctests.append('tested/misc.rst')
    #~ env.docs_doctests.append('tested/debts.rst')

    #~ def test_docs(self): self.run_django_manage_test('docs')
    def test_misc(self): self.run_docs_doctests('tested/misc.rst')
    def test_debts(self): self.run_docs_doctests('tested/debts.rst')
    def test_cbss(self): self.run_docs_doctests('tested/cbss.rst')
    def test_pcsw(self): self.run_docs_doctests('tested/pcsw.rst')
    def test_courses(self): self.run_docs_doctests('tested/courses.rst')
    
    


class PackagesTests(BaseTestCase):
    def test_packages(self): self.run_packages_test(SETUP_INFO['packages'])

