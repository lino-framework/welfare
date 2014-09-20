=============================================
ISIP (Individual Social Integration Projects)
=============================================

.. module:: welfare.isip

The :mod:`lino_welfare.modlib.isip` package provides data definitions
for managing ISIPs (Individual Social Integration Projects)


Mixins
======

.. class:: ContractBase

  Common base class for both :class:`welfare.isip.Contract` and 
  :class:`welfare.jobs.Contract` 

  .. attribute:: client

    Pointer to the :class:`welfare.pcsw.Client` with whom this
    contract is signed.

  .. attribute:: exam_policy

    Pointer to the :class:`ExamPolicy`

  .. attribute:: language

  .. attribute:: applies_from
  .. attribute:: applies_until
  .. attribute:: date_issued


Models
======

.. class:: Contract

  Inherits from :class:`ContractBase`.

  .. attribute:: study_type

    Pointer to the :class:`StudyType`

.. class:: ContractPartner

  Every contract can optionally be associated to one or several
  external partners. These are organisations

  .. attribute:: company

      Pointer to the :class:`contacts.Company`

  .. attribute:: contact_person

      Pointer to the :class:`contacts.Person` who represents this company.

  .. attribute:: contact_role

      Pointer to the role (:class:`contacts.RoleType`) of
      :attr:`contact_person` within :attr:`company`.

  .. attribute:: duties_company

      Text fragment inserted into the printable document.

.. class:: ContractPartners

.. class:: PartnersByContract



.. class:: ContractType

  The contract type determines the print template to be used. 

  .. attribute:: ref

      Print templates may use this field to conditionally hide or show
      certain parts.

  .. attribute:: exam_policy

      The default :class:`ExamPolicy` for new contracts of this type.

.. class:: ExamPolicy
.. class:: ExamPolicies

    The examination policy of a contract expresses how often the
    social agent meets with the client in order to analyze the
    evolution of the project.  This is a :class:`ml.cal.RecurrenceSet`
    and thus decides about automatic calendar events to be created.

    The demo database has the following examination policies:

    .. django2rst::

        rt.show('isip.ExamPolicies')


.. class:: ContractEnding
.. class:: ContractEndings

    Expresses how a contract was ended.

    The demo database has the following contract endings:

    .. django2rst::

        rt.show('isip.ContractEndings')


.. class:: EducationLevel
.. class:: EducationLevels

    The demo database has the following education levels:

    .. django2rst::

        rt.show('isip.EducationLevels')



.. class:: StudyType

    Used in :attr:`Contract.study_type` and by :attr:`jobs.Study.type`.

    .. attribute:: education_level

        Pointer to the :class:`EducationLevel`.

    .. attribute:: study_regime

        One choice from :class:`StudyRegimes`.



.. class:: StudyTypes

    The demo database has the following study types:

    .. django2rst::

        rt.show('isip.StudyTypes')



Choicelists
===========

.. class:: StudyRegimes

    The demo database has the following study regimes:

    .. django2rst::

        rt.show('isip.StudyRegimes')


.. class:: ContractEvents

    The demo database has the following contract events:

    .. django2rst::

        rt.show('isip.ContractEvents')

