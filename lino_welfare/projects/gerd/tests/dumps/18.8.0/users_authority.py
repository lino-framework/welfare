# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table users_authority...")
# fields: id, user, authorized
loader.save(create_users_authority(1,5,7))
loader.save(create_users_authority(2,6,7))
loader.save(create_users_authority(3,4,7))

loader.flush_deferred_objects()
