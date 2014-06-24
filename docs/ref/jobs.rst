============
Article 60§7
============

.. module:: welfare.jobs

The :mod:`lino_welfare.modlib.jobs` package provides data definitions
for managing so-called article 60§7 projects.

    An article 60§7 project is when the PCSW arranges a job for a
    client, with the aim to bring this person back into the social
    security system and the employment process. In most cases, the
    PSWC acts as the legal employer.  It can employ the person in its
    own services (internal contracts) or put him/her at the disposal
    of a third party employer (external contracts).

    (Adapted from `mi-is.be
    <http://www.mi-is.be/en/public-social-welfare-centers/article-60-7>`_).

This module is technically similar to :mod:`ISIP <isip>` which it
extends.

.. contents:: 
   :local:
   :depth: 2



Models
======

.. class:: Contract

  Inherits from :class:`welfare.isip.ContractBase`.

.. class:: Job

.. class:: JobProvider

  Inherits from :class:`ml.contacts.Company`.
  


.. class:: JobType

  Inherits from :class:`dd.Sequenced`.

.. class:: JobTypes

    The demo database comes with these job types:

    .. django2rst:: 

        dd.show('jobs.JobTypes')
        
.. class:: ContractType

  Inherits from :class:`dd.BabelNamed` and :class:`dd.PrintableType`.

.. class:: ContractTypes

    The demo database comes with these contract types:

    .. django2rst:: 

        dd.show('jobs.ContractTypes')


Tables
======        

.. class:: JobsOverView

    This list helps integration agents to make decisions like:

    - which jobs are soon going to be free, and which candidate(s) should we
      suggest?

    Example (using fictive demo data and only on one job type):

    .. django2rst:: 

       jt = jobs.JobType.objects.get(id=1)
       dd.show('jobs.JobsOverview', param_values=dict(job_type=jt))
        

