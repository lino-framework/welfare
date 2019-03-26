# -*- coding: UTF-8 -*-
logger.info("Loading 11 objects to table cal_eventtype...")
# fields: id, ref, seqno, name, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, force_guest_states, start_date, event_label, max_conflicting, max_days, transparent, planner_column, invite_client, esf_field
loader.save(create_cal_eventtype(1,None,1,['Feiertage', 'Jours f\xe9ri\xe9s', 'Holidays'],False,u'',u'',False,True,False,False,None,['', '', ''],1,1,False,u'10',False,None))
loader.save(create_cal_eventtype(2,None,2,['Versammlung', 'R\xe9union', 'Meeting'],False,u'',u'',True,False,False,False,None,['', '', ''],1,1,False,u'10',False,None))
loader.save(create_cal_eventtype(3,None,3,['Intern', 'Interne', 'Internal'],False,u'',u'',True,False,False,False,None,['', '', ''],1,1,True,u'20',False,None))
loader.save(create_cal_eventtype(4,None,4,['Internal meetings with client', 'Internal meetings with client', 'Internal meetings with client'],False,u'',u'',True,False,False,False,None,['Termin', 'Rendez-vous', 'Appointment'],4,1,False,None,True,u'10'))
loader.save(create_cal_eventtype(5,None,5,['Auswertung', '\xc9valuation', 'Evaluation'],False,u'',u'',True,False,False,False,None,['', '', ''],4,1,False,None,True,u'20'))
loader.save(create_cal_eventtype(6,None,6,['Beratungen mit Klient', 'Consultations avec le b\xe9n\xe9ficiaire', 'Consultations with client'],False,u'',u'',False,False,False,False,None,['Beratung', 'Consultation', 'Consultation'],1,1,False,None,False,None))
loader.save(create_cal_eventtype(7,None,7,['External meetings with client', 'R\xe9unions externes avec le b\xe9n\xe9ficiaire', 'External meetings with client'],False,u'',u'',True,False,False,False,None,['External meeting', 'R\xe9union externe', 'External meeting'],1,1,False,None,True,u'21'))
loader.save(create_cal_eventtype(8,None,8,['Informational meetings', 'Informational meetings', 'Informational meetings'],False,u'',u'',True,False,False,False,None,['Informational meeting', 'Informational meeting', 'Informational meeting'],1,1,False,None,True,u'30'))
loader.save(create_cal_eventtype(9,None,9,['Internal meetings', 'R\xe9unions interne', 'Internal meetings'],False,u'',u'',True,False,False,False,None,['Internal meeting', 'R\xe9union interne', 'Internal meeting'],1,1,False,None,False,None))
loader.save(create_cal_eventtype(10,None,10,['External meetings', 'R\xe9unions externe', 'External meetings'],False,u'',u'',True,False,False,False,None,['External meeting', 'R\xe9union externe', 'External meeting'],1,1,False,None,False,None))
loader.save(create_cal_eventtype(11,None,11,['Privat', 'Priv\xe9', 'Private'],False,u'',u'',True,False,False,False,None,['', '', ''],1,1,False,None,False,None))

loader.flush_deferred_objects()
