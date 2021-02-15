# how to run a single test:
# $ python -m unittest tests.test_demo.TestCase.test_noi1e_maketour
# $ python -m unittest tests.test_demo.TestCase.test_lydia

from django import VERSION

from lino import PYAFTER26
from lino.utils.pythontest import TestCase


class TestCase(TestCase):

    def do_test_demo_project(self, prjname):
        """Run :manage:`test` and :manage:`demotest` in a subprocess in the given demo project.
        """
        pth = 'lino_welfare/projects/' + prjname
        self.run_django_manage_test(pth)
        self.run_django_admin_command_cd(pth, "demotest")

    def test_gerd(self): self.do_test_demo_project('gerd')
    def test_mathieu(self): self.do_test_demo_project('mathieu')
