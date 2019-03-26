# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table gfks_helptext...")
# fields: id, content_type, field, help_text
loader.save(create_gfks_helptext(1,contacts_Partner,u'language',u'Die Sprache, in der Dokumente ausgestellt werden sollen.'))
loader.save(create_gfks_helptext(2,gfks_HelpText,u'field',u'The name of the field.'))
loader.save(create_gfks_helptext(3,pcsw_Client,u'in_belgium_since',u'Since when this person in Belgium lives.\n<b>Important:</b> help_text can be formatted.'))
loader.save(create_gfks_helptext(4,pcsw_Client,u'noble_condition',u'The eventual noble condition of this person. Imported from TIM.'))
loader.save(create_gfks_helptext(5,contacts_Partner,u'language',u'Die Sprache, in der Dokumente ausgestellt werden sollen.'))

loader.flush_deferred_objects()
