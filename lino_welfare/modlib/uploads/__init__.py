# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino.modlib.uploads`
"""

from lino.modlib.uploads import Plugin


class Plugin(Plugin):

    extends_models = ['UploadType', 'Upload']
