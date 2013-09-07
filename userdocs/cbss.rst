.. _welfare.cbss:

=================
Banque-carrefour
=================

Ce module supporte pour l'instant la gestion des requêtes suivantes:

.. actors_overview:: 
    cbss.IdentifyPersonRequests
    cbss.ManageAccessRequests
    cbss.RetrieveTIGroupsRequests
    
    
TIs connus
----------

Liste incomplète (conversion en cours) des TIs que Lino connait:

.. django2rst::

    from lino_welfare.modlib.cbss.tx25 import HANDLERS
    from atelier import rstgen
    rows = []
    for k,v in HANDLERS.items():
        rows.append([k, unicode(v[0]),v[2]])
    print rstgen.table(['Name',"Text","IT"],rows)
    



Référence
=========

.. actor:: cbss.Sector
.. actor:: cbss.Purpose
.. actor:: cbss.IdentifyPersonRequest
.. actor:: cbss.ManageAccessRequest
.. actor:: cbss.RetrieveTIGroupsRequest

