..
  default userdocs for contacts module, used also by faggio, patrols,...

.. contents:: 
   :local:
   :depth: 2


.. actor:: contacts.Partner

    A Partner is any physical or moral person for which you want to 
    keep contact data (address, phone numbers, ...).

    Every :ddref:`contacts.Partner`
    can also be a
    :ddref:`contacts.Person`
    or a 
    :ddref:`contacts.Company`
    (or both).

    Lino differentiates the following subclasses of Partner:

    .. django2rst:: contacts.Partner.print_subclasses_graph()


.. actor:: contacts.Person

    A Person is a :ddref:`contacts.Partner` which corresponds to 
    a physical person or human being.

.. actor:: contacts.Company

    A Company is a :ddref:`contacts.Partner` which corresponds to 
    a company or any other type of organization.

.. actor:: contacts.Role

    A Role is when a given :ddref:`contacts.Person` plays a given
    :ddref:`contacts.RoleType` in a given :ddref:`contacts.Company`.

.. actor:: contacts.RoleType

    A :ddref:`contacts.RoleType` is 
    "what a given :ddref:`contacts.Person` can be for a given 
    :ddref:`contacts.Company`".

    The default database comes with the following list of 
    :ddref:`contacts.RoleTypes`:
    
    .. django2rst:: dd.show(contacts.RoleTypes)
    
.. actor:: contacts.CompanyType

    The default database comes with the following list of 
    organization types:
    
    .. django2rst:: dd.show(contacts.CompanyTypes)

