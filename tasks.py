# from atelier.invlib import add_demo_project
from atelier.tasks import ns
ns.setup_from_tasks(
    globals(), "lino_welfare",
    languages=['en', 'de', 'fr'],
    tolerate_sphinx_warnings= False,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_welfare/modlib/welfare/locale',
    cleanable_files=['docs/api/lino_welfare.*'],
    demo_projects=[
        'lino_welfare.projects.std.settings.demo',
        'lino_welfare.projects.eupen.settings.demo',
        'lino_welfare.projects.chatelet.settings.demo'])

    # apidoc_exclude_pathnames:
    # - lino_welfare/projects
