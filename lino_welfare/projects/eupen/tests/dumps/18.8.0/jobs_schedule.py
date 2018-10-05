# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table jobs_schedule...")
# fields: id, name
loader.save(create_jobs_schedule(1,['5-Tage-Woche', '5 jours/semaine', '5 days/week']))
loader.save(create_jobs_schedule(2,['Individuell', 'individuel', 'Individual']))
loader.save(create_jobs_schedule(3,['Montag, Mittwoch, Freitag', 'lundi,mercredi,vendredi', 'Monday, Wednesday, Friday']))

loader.flush_deferred_objects()
