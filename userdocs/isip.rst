.. _welfare.isip:

====
ISIP
====

Ce module gère le travail avec les :term:`PIIS`.
Il est techniquement similaire au module :ref:`welfare.jobs`.

.. glossary::

  ISIP
    A convention or contract between the PCSW and a young client
    that leads to an individual coaching of the person, mostly 
    concerning her scholar education.
    
  PIIS
    Project d'Insertion Sociale Personnalisé.
    Une convention 
    entre le CPAS et un jeune client qui engendra un accompagnement 
    individuel de la personne surtout au niveau enseignement.

.. contents:: 
   :local:
   :depth: 2



.. actor:: isip.Contract

    The contract defining this :term:`ISIP`.
    A printable document to be signed.
    
    
    
.. actor:: isip.StudyType

    The list of choices for the *Study type* field of 
    an :ddref:`isip.Contract` or an :ddref:`jobs.Contract`.

    .. django2rst::
        
        settings.SITE.login('robin').show(isip.StudyTypes)

.. actor:: isip.ContractType
.. actor:: isip.ExamPolicy
.. actor:: isip.ContractEnding
