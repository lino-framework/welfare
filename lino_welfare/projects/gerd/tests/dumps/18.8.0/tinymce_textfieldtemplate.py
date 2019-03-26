# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table tinymce_textfieldtemplate...")
# fields: id, user, name, description, text
loader.save(create_tinymce_textfieldtemplate(1,None,u'hello',u"Inserts 'Hello, world!'",u'<div>Hello, world!</div>'))
loader.save(create_tinymce_textfieldtemplate(2,None,u'mfg',None,u'<p>Mit freundlichen Gr&uuml;&szlig;en<br><p>{{request.subst_user or request.user}}</p>'))

loader.flush_deferred_objects()
