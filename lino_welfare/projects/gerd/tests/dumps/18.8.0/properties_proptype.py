# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table properties_proptype...")
# fields: id, name, choicelist, default_value, limit_to_choices, multiple_choices
loader.save(create_properties_proptype(1,['Vorhanden oder nicht', 'Pr\xe9sent ou pas', 'Present or not'],u'',u'',False,False))
loader.save(create_properties_proptype(2,['Bewertung', 'Appr\xe9ciation(?)', 'Rating'],u'properties.HowWell',u'2',False,False))
loader.save(create_properties_proptype(3,['Abteilung', 'Division', 'Division'],u'',u'',False,False))

loader.flush_deferred_objects()
