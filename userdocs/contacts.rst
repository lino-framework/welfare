.. _welfare.contacts:

=========
Contacts
=========


.. actor:: contacts.Partner

    Toute personne physique ou morale est enregistrée 
    dans Lino en tant que :ddref:`contacts.Partner`.

    Lino différencie les types de Partenaires suivants:

    .. django2rst:: contacts.Partner.print_subclasses_graph()


.. actor:: contacts.Partner.is_obsolete

    Das Attribut "veraltet" bedeutet : 

    - die Daten dieses Partners werden nicht mehr gepflegt, 
    - alle Angaben verstehen sich als "so war es, bevor dieser Partner 
      aufhörte, uns zu interessieren".

    Veraltete Partner werden normalerweise in Listen ignoriert,
    als wären sie gelöscht.
    Um sie trotzdem zu sehen, 
    muss das Ankreuzfeld `Auch veraltete Klienten`
    (bzw. `Auch veraltete Partner`)
    im Parameter-Panel der Liste angekreuzt werden.



.. actor:: contacts.Person

.. actor:: contacts.Company

.. actor:: contacts.Role

.. actor:: contacts.RoleType

.. actor:: contacts.CompanyType

.. actor:: pcsw.Activity


.. actor:: households.Household

.. actor:: households.Type

