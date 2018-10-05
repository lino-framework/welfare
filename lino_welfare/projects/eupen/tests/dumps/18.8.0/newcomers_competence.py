# -*- coding: UTF-8 -*-
logger.info("Loading 7 objects to table newcomers_competence...")
# fields: id, seqno, user, faculty, weight
loader.save(create_newcomers_competence(1,1,6,1,10))
loader.save(create_newcomers_competence(2,2,5,2,5))
loader.save(create_newcomers_competence(3,3,4,3,4))
loader.save(create_newcomers_competence(4,4,6,4,6))
loader.save(create_newcomers_competence(5,5,5,5,2))
loader.save(create_newcomers_competence(6,6,4,1,10))
loader.save(create_newcomers_competence(7,7,6,2,5))

loader.flush_deferred_objects()
