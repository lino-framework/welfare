# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table cbss_manageaccessrequest...")
# fields: id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, birth_date, sis_card_no, id_card_no, first_name, last_name, sector, purpose, start_date, end_date, action, query_register
loader.save(create_cbss_manageaccessrequest(1,5,None,116,None,None,u'',u'',u'',u'',u'',u'',u'680601 053-29',u'1968-06-01',u'',u'',u'',u'',45,90,date(2014,5,22),date(2014,6,6),'1','3'))

loader.flush_deferred_objects()
