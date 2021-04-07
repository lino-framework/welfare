# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd.
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.test_docs
"""
from unipath import Path

from lino.utils.pythontest import TestCase

import lino_welfare


class BaseTestCase(TestCase):
    project_root = Path(__file__).parent.parent


class PackagesTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(lino_welfare.SETUP_INFO['packages'])
