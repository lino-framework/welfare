from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_welfare",
    languages=['en', 'de', 'fr'],
    # tolerate_sphinx_warnings=True,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_welfare/modlib/welfare/locale',
    cleanable_files=['docs/api/lino_welfare.*'],
    demo_projects=[
        'lino_welfare/projects/std',
        'lino_welfare/projects/eupen',
        'lino_welfare/projects/chatelet'])

    # apidoc_exclude_pathnames:
    # - lino_welfare/projects
