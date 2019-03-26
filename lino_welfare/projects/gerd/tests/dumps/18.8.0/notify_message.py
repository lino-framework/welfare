# -*- coding: UTF-8 -*-
logger.info("Loading 13 objects to table notify_message...")
# fields: id, created, user, owner_type, owner_id, message_type, seen, sent, body, mail_mode, subject
loader.save(create_notify_message(1,dt(2014,5,22,5,48,0),6,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'La base de donn\xe9es a \xe9t\xe9 initialis\xe9e.'))
loader.save(create_notify_message(2,dt(2014,5,22,5,48,0),9,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(3,dt(2014,5,22,5,48,0),5,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(4,dt(2014,5,22,5,48,0),10,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(5,dt(2014,5,22,5,48,0),13,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(6,dt(2014,5,22,5,48,0),4,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'La base de donn\xe9es a \xe9t\xe9 initialis\xe9e.'))
loader.save(create_notify_message(7,dt(2014,5,22,5,48,0),8,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(8,dt(2014,5,22,5,48,0),11,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(9,dt(2014,5,22,5,48,0),3,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'The database has been initialized.'))
loader.save(create_notify_message(10,dt(2014,5,22,5,48,0),1,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(11,dt(2014,5,22,5,48,0),2,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'La base de donn\xe9es a \xe9t\xe9 initialis\xe9e.'))
loader.save(create_notify_message(12,dt(2014,5,22,5,48,0),7,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))
loader.save(create_notify_message(13,dt(2014,5,22,5,48,0),12,None,None,u'system',None,dt(2014,5,22,5,48,0),u'',u'often',u'Die Datenbank wurde initialisiert.'))

loader.flush_deferred_objects()
