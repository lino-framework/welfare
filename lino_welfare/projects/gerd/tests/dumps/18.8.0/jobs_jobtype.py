# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table jobs_jobtype...")
# fields: id, seqno, name, remark, is_social
loader.save(create_jobs_jobtype(1,1,u'Sozialwirtschaft = "major\xe9s"',u'',False))
loader.save(create_jobs_jobtype(2,2,u'Intern',u'',False))
loader.save(create_jobs_jobtype(3,3,u'Extern (\xd6ffentl. VoE mit Kostenr\xfcckerstattung)',u'',False))
loader.save(create_jobs_jobtype(4,4,u'Extern (Privat Kostenr\xfcckerstattung)',u'',False))
loader.save(create_jobs_jobtype(5,5,u'Sonstige',u'',False))

loader.flush_deferred_objects()
