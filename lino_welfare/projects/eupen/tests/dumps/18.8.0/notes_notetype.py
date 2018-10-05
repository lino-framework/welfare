# -*- coding: UTF-8 -*-
logger.info("Loading 13 objects to table notes_notetype...")
# fields: id, name, build_method, template, attach_to_email, email_template, important, remark, special_type
loader.save(create_notes_notetype(1,['Beschluss', '', ''],None,u'',False,u'Default.eml.html',False,u'',None))
loader.save(create_notes_notetype(2,['Konvention', '', ''],None,u'',False,u'Default.eml.html',False,u'Einmaliges Dokument in Verbindung mit Arbeitsvertrag',None))
loader.save(create_notes_notetype(3,['Notiz', '', ''],None,u'',False,u'Default.eml.html',False,u'Kontaktversuch, Gespr\xe4chsbericht, Telefonnotiz',None))
loader.save(create_notes_notetype(4,['Vorladung', '', ''],None,u'',False,u'Default.eml.html',False,u'Einladung zu einem pers\xf6nlichen Gespr\xe4ch',None))
loader.save(create_notes_notetype(5,['\xdcbergabeblatt', '', ''],None,u'',False,u'Default.eml.html',False,u'\xdcbergabeblatt vom allgemeinen Sozialdienst',None))
loader.save(create_notes_notetype(6,['Neuantrag', '', ''],None,u'',False,u'Default.eml.html',False,u'',None))
loader.save(create_notes_notetype(7,['Antragsformular', '', ''],None,u'',False,u'Default.eml.html',False,u'',None))
loader.save(create_notes_notetype(8,['Auswertungsbogen allgemein', '', ''],u'rtf',u'Auswertungsbogen_allgemein.rtf',False,u'Default.eml.html',False,u'',None))
loader.save(create_notes_notetype(9,['Erstgespr\xe4ch', 'Erstgespr\xe4ch', 'First meeting'],None,u'',False,u'Default.eml.html',False,u'','100'))
loader.save(create_notes_notetype(10,['Brief oder Einschreiben', 'Lettre', 'Letter'],u'appyrtf',u'Letter.odt',False,u'Default.eml.html',False,u'',None))
loader.save(create_notes_notetype(11,['Standardwert', 'Standardwert', 'Default'],None,u'',False,u'',False,u'',None))
loader.save(create_notes_notetype(12,['phone report', '', ''],None,u'',False,u'',False,u'',None))
loader.save(create_notes_notetype(13,['todo', '', ''],None,u'',False,u'',False,u'',None))

loader.flush_deferred_objects()
