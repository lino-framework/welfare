# -*- coding: UTF-8 -*-
logger.info("Loading 0 objects to table outbox_mail...")
# fields: id, project, user, owner_type, owner_id, date, subject, body, sent

loader.flush_deferred_objects()
