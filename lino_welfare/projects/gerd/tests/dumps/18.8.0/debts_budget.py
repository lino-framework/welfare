# -*- coding: UTF-8 -*-
logger.info("Loading 14 objects to table debts_budget...")
# fields: id, user, printed_by, date, partner, print_todos, print_empty_rows, include_yearly_incomes, intro, conclusion, dist_amount
loader.save(create_debts_budget(1,13,13,date(2014,5,22),232,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(2,11,None,date(2014,5,22),233,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(3,2,None,date(2014,5,22),234,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(4,1,None,date(2014,5,22),235,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(5,3,None,date(2014,5,22),236,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(6,13,None,date(2014,5,22),237,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(7,11,None,date(2014,5,22),254,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(8,2,None,date(2014,5,22),255,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(9,1,None,date(2014,5,22),256,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(10,3,None,date(2014,5,22),257,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(11,13,None,date(2014,5,22),270,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(12,11,None,date(2014,5,22),271,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(13,2,None,date(2014,5,22),272,False,False,False,u'',u'','120.00'))
loader.save(create_debts_budget(14,1,None,date(2014,5,22),273,False,False,False,u'',u'','120.00'))

loader.flush_deferred_objects()
