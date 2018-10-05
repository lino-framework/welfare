# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table newcomers_faculty...")
# fields: id, name, weight
loader.save(create_newcomers_faculty(1,['Eingliederungseinkommen (EiEi)', "Revenu d'int\xe9gration sociale (RIS)", 'EiEi'],10))
loader.save(create_newcomers_faculty(2,['DSBE', "Service d'insertion socio-professionnelle", 'DSBE'],5))
loader.save(create_newcomers_faculty(3,['Ausl\xe4nderbeihilfe', 'Aide sociale \xe9quivalente (pour \xe9trangers)', 'Ausl\xe4nderbeihilfe'],4))
loader.save(create_newcomers_faculty(4,['Finanzielle Begleitung', 'Accompagnement budg\xe9taire', 'Finanzielle Begleitung'],6))
loader.save(create_newcomers_faculty(5,['Laufende Beihilfe', 'Aide compl\xe9menataire', 'Laufende Beihilfe'],2))

loader.flush_deferred_objects()
