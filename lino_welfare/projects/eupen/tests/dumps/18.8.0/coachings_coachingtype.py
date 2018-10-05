# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table coachings_coachingtype...")
# fields: id, name, does_integ, does_gss, eval_guestrole
loader.save(create_coachings_coachingtype(1,['ASD', 'SSG', 'General'],False,True,1))
loader.save(create_coachings_coachingtype(2,['DSBE', 'SI', 'Integ'],True,False,1))
loader.save(create_coachings_coachingtype(3,['Schuldnerberatung', 'M\xe9diation de dettes', 'Debts mediation'],False,False,None))

loader.flush_deferred_objects()
