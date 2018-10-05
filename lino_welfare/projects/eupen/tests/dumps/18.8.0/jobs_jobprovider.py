# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table jobs_jobprovider...")
# fields: company_ptr
loader.save(create_jobs_jobprovider(188))
loader.save(create_jobs_jobprovider(189))
loader.save(create_jobs_jobprovider(191))

loader.flush_deferred_objects()
