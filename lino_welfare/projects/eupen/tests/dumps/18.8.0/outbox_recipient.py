# -*- coding: UTF-8 -*-
logger.info("Loading 0 objects to table outbox_recipient...")
# fields: id, mail, partner, type, address, name

loader.flush_deferred_objects()
