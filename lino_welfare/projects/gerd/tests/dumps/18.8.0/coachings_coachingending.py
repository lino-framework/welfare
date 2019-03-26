# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table coachings_coachingending...")
# fields: id, seqno, name, type
loader.save(create_coachings_coachingending(1,1,['\xdcbergabe an Kollege', 'Transfert vers coll\xe8gue', 'Transfer to colleague'],None))
loader.save(create_coachings_coachingending(2,2,['Einstellung des Anrechts auf SH', "Arret du droit \xe0 l'aide sociale", 'End of right on social aid'],None))
loader.save(create_coachings_coachingending(3,3,['Umzug in andere Gemeinde', 'D\xe9m\xe9nagement vers autre commune', 'Moved to another town'],None))
loader.save(create_coachings_coachingending(4,4,['Hat selber Arbeit gefunden', 'A trouv\xe9 du travail', 'Found a job'],None))

loader.flush_deferred_objects()
