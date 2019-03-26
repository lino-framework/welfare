# -*- coding: UTF-8 -*-
logger.info("Loading 10 objects to table contacts_role...")
# fields: id, type, person, company
loader.save(create_contacts_role(1,1,114,188))
loader.save(create_contacts_role(2,1,113,189))
loader.save(create_contacts_role(3,2,169,189))
loader.save(create_contacts_role(4,4,119,189))
loader.save(create_contacts_role(5,4,119,191))
loader.save(create_contacts_role(6,1,115,191))
loader.save(create_contacts_role(7,4,212,187))
loader.save(create_contacts_role(8,None,148,187))
loader.save(create_contacts_role(9,None,163,187))
loader.save(create_contacts_role(10,1,170,214))

loader.flush_deferred_objects()
