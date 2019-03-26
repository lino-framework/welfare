# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table jobs_contracttype...")
# fields: id, ref, name, full_name, exam_policy, overlap_group, template
loader.save(create_jobs_contracttype(1,u'art60-7a',['Sozial\xf6konomie', '\xe9conomie sociale', 'social economy'],u'',3,None,u''))
loader.save(create_jobs_contracttype(2,u'art60-7b',['Sozial\xf6konomie - major\xe9', '\xe9conomie sociale - major\xe9', 'social economy - increased'],u'',3,None,u''))
loader.save(create_jobs_contracttype(5,u'art60-7e',['Stadt Eupen', "ville d'Eupen", 'town'],u'',3,None,u''))
loader.save(create_jobs_contracttype(3,u'art60-7c',['mit R\xfcckerstattung', 'avec remboursement', 'social economy with refund'],u'',3,None,u''))
loader.save(create_jobs_contracttype(4,u'art60-7d',['mit R\xfcckerstattung Schule', 'avec remboursement \xe9cole', 'social economy school'],u'',3,None,u''))

loader.flush_deferred_objects()
