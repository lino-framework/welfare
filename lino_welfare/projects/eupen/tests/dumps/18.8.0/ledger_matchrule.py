# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table ledger_matchrule...")
# fields: id, account, journal
loader.save(create_ledger_matchrule(1,4,3))
loader.save(create_ledger_matchrule(2,21,4))

loader.flush_deferred_objects()
