# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table contacts_roletype...")
# fields: id, name, use_in_contracts
loader.save(create_contacts_roletype(1,['Gesch\xe4ftsf\xfchrer', 'G\xe9rant', 'Manager'],True))
loader.save(create_contacts_roletype(2,['Direktor', 'Directeur', 'Director'],True))
loader.save(create_contacts_roletype(3,['Sekret\xe4r', 'Secr\xe9taire', 'Secretary'],True))
loader.save(create_contacts_roletype(4,['EDV-Manager', 'G\xe9rant informatique', 'IT Manager'],False))
loader.save(create_contacts_roletype(5,['Pr\xe4sident', 'Pr\xe9sident', 'President'],True))

loader.flush_deferred_objects()
