# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table pcsw_dispensereason...")
# fields: id, seqno, name
loader.save(create_pcsw_dispensereason(1,1,['Gesundheitlich', 'Sant\xe9', 'Health']))
loader.save(create_pcsw_dispensereason(2,2,['Studium/Ausbildung', 'Etude/Formation', 'Studies']))
loader.save(create_pcsw_dispensereason(3,3,['Famili\xe4r', 'Cause familiale', 'Familiar']))
loader.save(create_pcsw_dispensereason(4,4,['Sonstige', 'Autre', 'Other']))

loader.flush_deferred_objects()
