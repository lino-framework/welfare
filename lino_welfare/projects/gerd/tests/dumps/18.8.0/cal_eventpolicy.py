# -*- coding: UTF-8 -*-
logger.info("Loading 6 objects to table cal_eventpolicy...")
# fields: id, start_date, start_time, end_date, end_time, name, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type
loader.save(create_cal_eventpolicy(1,date(2014,5,22),time(9,0,0),None,None,['Monatlich', 'Mensuel', 'Every month'],u'M',1,True,True,True,True,True,False,False,None,2))
loader.save(create_cal_eventpolicy(2,date(2014,5,22),time(9,0,0),None,None,['Alle 2 Monate', 'Bimensuel', 'Every 2 months'],u'M',2,True,True,True,True,True,False,False,None,2))
loader.save(create_cal_eventpolicy(3,date(2014,5,22),None,None,None,['Alle 3 Monate', 'Tous les 3 mois', 'Every 3 months'],u'M',3,True,True,True,True,True,False,False,None,2))
loader.save(create_cal_eventpolicy(4,date(2014,5,22),time(9,0,0),None,None,['Alle 2 Wochen', 'Tous les 14 jours', 'Every 2 weeks'],u'W',2,True,True,True,True,True,False,False,None,2))
loader.save(create_cal_eventpolicy(5,date(2014,5,22),time(9,0,0),None,None,['Einmal nach 10 Tagen', 'Une fois apr\xe8s 10 jours', 'Once after 10 days'],u'D',10,True,True,True,True,True,False,False,1,2))
loader.save(create_cal_eventpolicy(6,date(2014,5,22),None,None,None,['Sonstige', 'Autre', 'Other'],u'M',1,False,False,False,False,False,False,False,None,None))

loader.flush_deferred_objects()
