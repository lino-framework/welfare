# -*- coding: UTF-8 -*-
logger.info("Loading 9 objects to table uploads_uploadtype...")
# fields: id, name, upload_area, max_number, wanted, shortcut, warn_expiry_unit, warn_expiry_value
loader.save(create_uploads_uploadtype(1,['Aufenthaltserlaubnis', 'Permis de s\xe9jour', 'Residence permit'],'90',1,True,None,u'M',2))
loader.save(create_uploads_uploadtype(2,['Arbeitserlaubnis', 'Permis de travail', 'Work permit'],'90',1,True,None,u'M',2))
loader.save(create_uploads_uploadtype(3,['F\xfchrerschein', 'Permis de conduire', 'Driving licence'],'90',1,True,None,u'M',1))
loader.save(create_uploads_uploadtype(4,['Identifizierendes Dokument', 'Document identifiant', 'Identifying document'],'90',1,True,'pcsw.Client.id_document',u'M',1))
loader.save(create_uploads_uploadtype(5,['Vertrag', 'Contrat', 'Contract'],'90',-1,False,None,None,1))
loader.save(create_uploads_uploadtype(6,['\xc4rztliche Bescheinigung', 'Certificat m\xe9dical', 'Medical certificate'],'90',-1,False,None,None,1))
loader.save(create_uploads_uploadtype(7,['Behindertenausweis', "Certificat d'handicap", 'Handicap certificate'],'90',-1,False,None,None,1))
loader.save(create_uploads_uploadtype(8,['Diplom', 'Dipl\xf4me', 'Diploma'],'90',-1,True,None,None,1))
loader.save(create_uploads_uploadtype(9,['Personalausweis', "Carte d'identit\xe9", 'Identity card'],'90',-1,False,None,None,1))

loader.flush_deferred_objects()
