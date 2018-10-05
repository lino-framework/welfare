# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table pcsw_exclusiontype...")
# fields: id, name
loader.save(create_pcsw_exclusiontype(1,u'Termin nicht eingehalten'))
loader.save(create_pcsw_exclusiontype(2,u'ONEM-Auflagen nicht erf\xfcllt'))

loader.flush_deferred_objects()
