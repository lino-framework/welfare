# -*- coding: utf-8 -*-

import sys, os

extlinks = {}
extensions = []
intersphinx_mapping = {}

from lino.sphinxcontrib import configure
configure(globals(), 'lino_welfare.projects.gerd.settings.doctests')
project = "Lino Welfare"
copyright = '2012-2021 Rumma & Ko Ltd'

from atelier.sphinxconf import interproject
interproject.configure(globals(), 'atelier',
    # book=('https://www.lino-framework.org/', None),
    hg=('https://hosting.lino-framework.org/', None))

# extensions += ['lino.sphinxcontrib.actordoc']
extensions += ['lino.sphinxcontrib.logo']
# extensions += ['sphinx.ext.autosummary']
autosummary_generate = True
# autodoc_default_flags = ['members']
autodoc_default_options = {'members': None}

unused_docs = []
exclude_patterns = ['.build/*', 'shared/include/*']
pygments_style = str('sphinx')
html_title = "Lino Welfare"
html_static_path = ['.static']
html_last_updated_fmt = str('%b %d, %Y')
html_sidebars = {
    '**': ['globaltoc.html',
           'searchbox.html', 'links.html'],
}
html_use_modindex = False
html_use_index = True
html_copy_source = False
html_use_opensearch = ''
htmlhelp_basename = 'welfare'
latex_documents = [
  ('index', 'lino.tex', 'lino', 'Luc Saffre', 'manual'),
]
