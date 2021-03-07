# how to run a single test:
# $ python -m unittest tests.test_demo.TestCase.test_noi1e_maketour
# $ python -m unittest tests.test_demo.TestCase.test_lydia

from django import VERSION

from lino import PYAFTER26
from lino.utils.pythontest import TestCase


class TestCase(TestCase):

    demo_projects_root = 'lino_welfare/projects'

    def test_gerd(self): self.do_test_demo_project('gerd')
    def test_mathieu(self): self.do_test_demo_project('mathieu')
