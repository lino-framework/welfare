.. _welfare.jobs:

========
Art60*7
========

.. _welfare.jobs.Job:

Stelle
------

Eine Stelle ist ein Arbeitsplatz bei einem Stellenabieter, 
für den das ÖSHZ sich um die Besetzung kümmert.

(:class:`Job <lino_welfare.modlib.jobs.models.Job>`) 


.. _welfare.jobs.Candidature:

Kandidatur 
----------

Eine Kandidatur ist "wenn ein :ref:`welfare.pcsw.Client` sich für 
eine :ref:`welfare.jobs.Job`
bewirbt".
Das beinhaltet u.a. auch die Information, dass der verantwortliche 
Begleiter die Person als für diese Stelle geeignet einstuft.

(:class:`Candidature <lino_welfare.modlib.jobs.models.Candidature>`) 


.. _welfare.jobs.NewJobsOverview:

Overview of current jobs
------------------------

This list helps you to make decisions like:

- which jobs are soon going to be free, and which candidate(s) should we
  suggest?
- bla bla

Example (using fictive demo data):

.. py2rst:: 

    settings.SITE.login('rolf').show(jobs.NewJobsOverview)
    