# -*- coding: UTF-8 -*-
logger.info("Loading 10 objects to table clients_clientcontacttype...")
# fields: id, name, known_contact_type, is_bailiff, can_refund
loader.save(create_clients_clientcontacttype(1,['Apotheke', 'Pharmacie', 'Pharmacy'],None,False,False))
loader.save(create_clients_clientcontacttype(2,['Krankenkasse', "Caisse d'assurance maladie", 'Health insurance'],None,False,False))
loader.save(create_clients_clientcontacttype(3,['Rechtsanwalt', 'Avocat', 'Advocate'],None,False,False))
loader.save(create_clients_clientcontacttype(4,['Gerichtsvollzieher', 'Huissier', 'Bailiff'],None,True,False))
loader.save(create_clients_clientcontacttype(5,['Inkasso-Unternehmen', 'Inkasso-Unternehmen', 'Debt collecting company'],None,True,False))
loader.save(create_clients_clientcontacttype(6,['Arbeitsvermittler', 'Bureau de ch\xf4mage', 'Employment office'],None,False,False))
loader.save(create_clients_clientcontacttype(7,['Arzt', 'M\xe9decin', 'Physician'],None,False,True))
loader.save(create_clients_clientcontacttype(8,['Hausarzt', 'M\xe9decin traitant', 'Family doctor'],None,False,True))
loader.save(create_clients_clientcontacttype(9,['Zahnarzt', 'Dentiste', 'Dentist'],None,False,True))
loader.save(create_clients_clientcontacttype(10,['Kinderarzt', 'P\xe9diatre', 'Pediatrician'],None,False,True))

loader.flush_deferred_objects()
