# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Functionality for uploading files to the server and managing them.

Lino-Welfare extension of :mod:`lino.modlib.uploads`

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo

"""

from lino.modlib.uploads import Plugin


class Plugin(Plugin):

    extends_models = ['UploadType', 'Upload']

    def setup_main_menu(config, site, profile, m):
        system = site.plugins.system
        m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
        m.add_action('uploads.MyExpiringUploads')
        m.add_action('uploads.MyUploads')
