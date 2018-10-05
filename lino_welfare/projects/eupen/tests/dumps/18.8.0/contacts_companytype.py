# -*- coding: UTF-8 -*-
logger.info("Loading 14 objects to table contacts_companytype...")
# fields: id, name, abbr
loader.save(create_contacts_companytype(1,['Aktiengesellschaft', 'Soci\xe9t\xe9 Anonyme', 'Public Limited Company'],['AG', 'SA', '']))
loader.save(create_contacts_companytype(2,['Private Gesellschaft mit beschr\xe4nkter Haft', 'Soci\xe9t\xe9 Priv\xe9e \xe0 Responsabilit\xe9 Limit\xe9e', 'Limited Liability Company'],['PGmbH', 'SPRL', '']))
loader.save(create_contacts_companytype(3,['Einpersonengesellschaft mit beschr\xe4nkter Haft', "Soci\xe9t\xe9 d'Une Personne \xe0 Responsabilit\xe9 Limit\xe9e", 'One-person Private Limited Company'],['EGmbH', 'SPRLU', '']))
loader.save(create_contacts_companytype(4,['Kooperative mit beschr\xe4nkter Haft', 'Soci\xe9t\xe9 Coop\xe9rative \xe0 Responsabilit\xe9 Limit\xe9e', 'Cooperative Company with Limited Liability'],['', 'SCRL', '']))
loader.save(create_contacts_companytype(5,['Kooperative mit unbeschr\xe4nkter Haft', 'Soci\xe9t\xe9 Coop\xe9rative \xe0 Responsabilit\xe9 Illimit\xe9e', 'Cooperative Company with Unlimited Liability'],['', 'SCRI', '']))
loader.save(create_contacts_companytype(6,['Gesellschaft \xf6ffentlichen Rechts', 'Soci\xe9t\xe9 de Droit Commun', 'Non-stock Corporation'],['', '', '']))
loader.save(create_contacts_companytype(7,['Vereinigung ohne Gewinnabsicht', 'Association sans But Lucratif', 'Charity/Company established for social purposes'],['V.o.G.', 'ASBL', '']))
loader.save(create_contacts_companytype(8,['Genossenschaft', 'Soci\xe9t\xe9 Coop\xe9rative', 'Cooperative Company'],['', 'SC', '']))
loader.save(create_contacts_companytype(9,['Firma', 'Soci\xe9t\xe9', 'Company'],['', '', '']))
loader.save(create_contacts_companytype(10,['\xd6ffentlicher Dienst', 'Service Public', 'Public service'],['', '', '']))
loader.save(create_contacts_companytype(11,['Ministerium', 'Minist\xe8re', 'Ministry'],['', '', '']))
loader.save(create_contacts_companytype(12,['Schule', '\xe9cole', 'School'],['', '', '']))
loader.save(create_contacts_companytype(13,['Freier Mitarbeiter', 'Travailleur libre', 'Freelancer'],['', '', '']))
loader.save(create_contacts_companytype(14,['Einzelunternehmen', 'Entreprise individuelle', 'Sole proprietorship'],['', '', '']))

loader.flush_deferred_objects()
