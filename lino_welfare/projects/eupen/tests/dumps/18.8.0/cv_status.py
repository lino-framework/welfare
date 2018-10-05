# -*- coding: UTF-8 -*-
logger.info("Loading 7 objects to table cv_status...")
# fields: id, name
loader.save(create_cv_status(1,['Arbeiter', 'Ouvrier', 'Worker']))
loader.save(create_cv_status(2,['Angestellter', 'Employ\xe9', 'Employee']))
loader.save(create_cv_status(3,['Selbstst\xe4ndiger', 'Ind\xe9pendant', 'Freelancer']))
loader.save(create_cv_status(4,['Ehrenamtlicher', 'B\xe9n\xe9vole', 'Voluntary']))
loader.save(create_cv_status(5,['Student', '\xc9tudiant', 'Student']))
loader.save(create_cv_status(6,['Laboratory', 'Stage', 'Laboratory']))
loader.save(create_cv_status(7,['Interim', 'Int\xe9rim', 'Interim']))

loader.flush_deferred_objects()
