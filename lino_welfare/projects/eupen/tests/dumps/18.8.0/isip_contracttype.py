# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table isip_contracttype...")
# fields: id, name, full_name, exam_policy, overlap_group, template, ref, needs_study_type
loader.save(create_isip_contracttype(1,['VSE Ausbildung', 'VSE Ausbildung', 'VSE Ausbildung'],u'',1,None,u'',u'vsea',True))
loader.save(create_isip_contracttype(2,['VSE Arbeitssuche', 'VSE Arbeitssuche', 'VSE Arbeitssuche'],u'',1,None,u'',u'vseb',False))
loader.save(create_isip_contracttype(3,['VSE Lehre', 'VSE Lehre', 'VSE Lehre'],u'',1,None,u'',u'vsec',False))
loader.save(create_isip_contracttype(4,['VSE Vollzeitstudium', 'VSE Vollzeitstudium', 'VSE Vollzeitstudium'],u'',1,None,u'',u'vsed',True))
loader.save(create_isip_contracttype(5,['VSE Sprachkurs', 'VSE Sprachkurs', 'VSE Sprachkurs'],u'',1,None,u'',u'vsee',False))

loader.flush_deferred_objects()
