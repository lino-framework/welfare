.. _welfare.cbss:

=================
Banque-carrefour
=================

Ce module supporte la gestion des requêtes suivantes:

.. contents:: 
   :local:
   :depth: 2
    

.. actor:: cbss.IdentifyPersonRequest
.. actor:: cbss.ManageAccessRequest

.. actor:: cbss.RetrieveTIGroupsRequest

    Incomplete list (conversion in progress) of the "information
    types" handled by Lino:

    .. django2rst::

        from lino_welfare.modlib.cbss.tx25 import HANDLERS
        from atelier import rstgen
        rows = []
        for k,v in HANDLERS.items():
            rows.append([k, unicode(v[0]),v[2]])
        def c(a,b): return cmp(a[0], b[0])
        rows = sorted(rows)
        print(rstgen.table(['Name',"Text","IT"],rows))
        
.. actor:: cbss.Sector
.. actor:: cbss.Purpose
