================
Curriculum Vitae
================

.. module:: welfare.cv

The :mod:`lino_welfare.modlib.cv` package provides data definitions
for managing information to figure in a CV.

.. contents:: 
   :local:
   :depth: 2



Models
======

.. class:: LanguageKnowledge

    .. attribute:: cef_level

    The CEF level.


Choicelists
===========

.. class:: CefLevel

    List of possible choices for the
    :attr:`LanguageKnowledge.cef_level` field.
    
    .. django2rst::
        
        rt.show(cv.CefLevel)

