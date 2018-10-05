# -*- coding: UTF-8 -*-
logger.info("Loading 14 objects to table clients_clientcontact...")
# fields: id, company, contact_person, contact_role, type, client, remark
loader.save(create_clients_clientcontact(1,200,None,None,1,139,u''))
loader.save(create_clients_clientcontact(2,None,215,None,7,139,u''))
loader.save(create_clients_clientcontact(3,None,216,None,8,139,u''))
loader.save(create_clients_clientcontact(4,None,217,None,9,139,u''))
loader.save(create_clients_clientcontact(5,201,None,None,1,141,u''))
loader.save(create_clients_clientcontact(6,None,219,None,10,141,u''))
loader.save(create_clients_clientcontact(7,None,215,None,7,141,u''))
loader.save(create_clients_clientcontact(8,None,216,None,8,141,u''))
loader.save(create_clients_clientcontact(9,None,218,None,9,142,u''))
loader.save(create_clients_clientcontact(10,None,219,None,10,142,u''))
loader.save(create_clients_clientcontact(11,None,215,None,7,142,u''))
loader.save(create_clients_clientcontact(12,None,216,None,8,144,u''))
loader.save(create_clients_clientcontact(13,None,217,None,9,144,u''))
loader.save(create_clients_clientcontact(14,None,219,None,10,144,u''))

loader.flush_deferred_objects()
