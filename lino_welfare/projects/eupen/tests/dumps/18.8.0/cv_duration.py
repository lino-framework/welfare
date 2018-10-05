# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table cv_duration...")
# fields: id, name
loader.save(create_cv_duration(1,['Unbeschr\xe4nkte Dauer', 'Dur\xe9e ind\xe9termin\xe9e', 'Unlimited duration']))
loader.save(create_cv_duration(2,['Beschr\xe4nkte Dauer', 'Dur\xe9e d\xe9termin\xe9e', 'Limited duration']))
loader.save(create_cv_duration(3,['Clearly defined job', 'Travail nettement d\xe9fini', 'Clearly defined job']))
loader.save(create_cv_duration(4,['Ersatz', 'Contrat de remplacement', 'Replacement']))
loader.save(create_cv_duration(5,['Interim', 'Int\xe9rim', 'Interim']))

loader.flush_deferred_objects()
