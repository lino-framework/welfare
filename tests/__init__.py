# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd.
# License: BSD (see file COPYING for details)

"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.test_docs
"""
from unipath import Path
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = "lino_welfare.settings.test"

from lino.utils.pythontest import TestCase
# from atelier.test import TestCase

import lino_welfare


class BaseTestCase(TestCase):
    project_root = Path(__file__).parent.parent


class DemoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests
    """

    def test_std(self):
        # print("20180502 test_std()")
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'std').absolute()
        self.run_django_manage_test(cwd)
    
    def test_eupen(self):
        # print("20180502 test_eupen()")
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'eupen').absolute()
        self.run_django_manage_test(cwd)

    def test_chatelet(self):
        # print("20180502 test_chatelet()")
        cwd = self.project_root.child(
            'lino_welfare', 'projects', 'chatelet').absolute()
        self.run_django_manage_test(cwd)


class PackagesTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(lino_welfare.SETUP_INFO['packages'])

        
