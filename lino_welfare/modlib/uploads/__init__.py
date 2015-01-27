# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Functionality for uploading files to the server and managing them.
This is an extension of :mod:`lino.modlib.uploads`.

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo2

"""

from lino.modlib.uploads import Plugin


class Plugin(Plugin):

    extends_models = ['UploadType', 'Upload']

    def setup_main_menu(config, site, profile, m):
        mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('uploads.MyExpiringUploads')
        m.add_action('uploads.MyUploads')
