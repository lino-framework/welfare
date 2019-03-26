# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table cv_educationlevel...")
# fields: id, seqno, name, is_study, is_training
loader.save(create_cv_educationlevel(1,1,['Prim\xe4r', 'Primaire', 'Primary'],True,False))
loader.save(create_cv_educationlevel(2,2,['Sekund\xe4r', 'Secondaire', 'Secondary'],True,False))
loader.save(create_cv_educationlevel(3,3,['Hochschule', 'Sup\xe9rieur', 'Higher'],True,False))
loader.save(create_cv_educationlevel(4,4,['Bachelor', 'Bachelor', 'Bachelor'],True,False))
loader.save(create_cv_educationlevel(5,5,['Master', 'Master', 'Master'],True,False))

loader.flush_deferred_objects()
