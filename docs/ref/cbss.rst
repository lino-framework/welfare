=================
Banque-carrefour
=================

.. module:: welfare.cbss

Ce module supporte la gestion des requêtes suivantes:

.. contents:: 
   :local:
   :depth: 2
    

.. class:: IdentifyPersonRequest

.. class:: ManageAccessRequest

.. class:: cbss.RetrieveTIGroupsRequest

    Here is an incomplete list (conversion in progress) of the
    "information types" handled by Lino:

    .. lino2rst:: 

        from django.utils import translation
        from lino_welfare.modlib.cbss.tx25 import HANDLERS
        from atelier import rstgen
        rows = []
        for k,v in HANDLERS.items():
            en = str(v[0])
            with translation.override("de"):
                de = str(v[0])
            with translation.override("fr"):
                fr = str(v[0])
            rows.append([k, en, fr, de, v[2]])
        def c(a,b): return cmp(a[0], b[0])
        rows = sorted(rows)
        print(rstgen.table(['Name', "Text (en)", "Text (fr)", "Text (de)", "IT"],rows))
        
.. class:: Sector
.. class:: Purpose
