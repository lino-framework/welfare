# -*- coding: utf-8 -*-

from lino.sphinxcontrib import configure
configure(globals(), 'lino_welfare.projects.gerd.settings.doctests')
project = "Lino Welfare"
copyright = '2012-2021 Rumma & Ko Ltd'

extensions += ['lino.sphinxcontrib.logo']
# autodoc_default_options = {'members': None}

html_title = "Lino Welfare"

html_context.update(public_url='https://welfare.lino-framework.org')
