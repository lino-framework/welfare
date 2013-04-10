from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino_welfare','setup_info.py'),globals())

from atelier.test import SubProcessTestCase


class WelfareTestCase(SubProcessTestCase):
    default_environ = dict(DJANGO_SETTINGS_MODULE="lino_welfare.demo.settings")
    project_root = ROOTDIR
    
class DocsTests(WelfareTestCase):
    
    #~ env.docs_doctests.append('tested/misc.rst')
    #~ env.docs_doctests.append('tested/debts.rst')
    

    def test_00(self): self.run_django_manage_test('docs')
    def test_01(self): self.run_docs_doctests('tested/misc.rst')
    def test_02(self): self.run_docs_doctests('tested/debts.rst')
    


