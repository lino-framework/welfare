# -*- coding: UTF-8 -*-
logger.info("Loading 11 objects to table cv_studytype...")
# fields: id, name, is_study, is_training, education_level
loader.save(create_cv_studytype(1,['Schule', '\xc9cole', 'School'],True,False,None))
loader.save(create_cv_studytype(2,['Sonderschule', '\xc9cole sp\xe9ciale', 'Special school'],True,False,None))
loader.save(create_cv_studytype(3,['Ausbildung', 'Formation', 'Training'],True,False,None))
loader.save(create_cv_studytype(4,['Lehre', 'Apprentissage', 'Apprenticeship'],True,False,None))
loader.save(create_cv_studytype(5,['Hochschule', '\xc9cole sup\xe9rieure', 'Highschool'],True,False,None))
loader.save(create_cv_studytype(6,['Universit\xe4t', 'Universit\xe9', 'University'],True,False,None))
loader.save(create_cv_studytype(7,['Teilzeitunterricht', 'Cours \xe0 temps partiel', 'Part-time study'],True,False,None))
loader.save(create_cv_studytype(8,['Fernkurs', 'Cours \xe0 distance', 'Remote study'],True,False,None))
loader.save(create_cv_studytype(9,['Prequalifying', 'Pr\xe9qualification', 'Prequalifying'],False,True,None))
loader.save(create_cv_studytype(10,['Qualifying', 'Qualification', 'Qualifying'],False,True,None))
loader.save(create_cv_studytype(11,['Alpha', 'Alpha', 'Alpha'],False,True,None))

loader.flush_deferred_objects()
