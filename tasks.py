from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_welfare",
    languages=['en', 'de', 'fr'],
    # tolerate_sphinx_warnings=True,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_welfare/modlib/welfare/locale',
    cleanable_files=[
        'docs/api/lino_welfare.*',
        'docs/api/lino_weleup.*',
        'docs/api/lino_welcht.*'],
    demo_projects=[
        'lino_welfare.projects.gerd',
        'lino_welfare.projects.mathieu']
)

