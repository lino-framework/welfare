# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table languages_language...")
# fields: name, id, iso2
loader.save(create_languages_language(['Deutsch', 'Allemand', 'German'],u'ger',u''))
loader.save(create_languages_language(['Englisch', 'Anglais', 'English'],u'eng',u''))
loader.save(create_languages_language(['Estnisch', 'Estonien', 'Estonian'],u'est',u''))
loader.save(create_languages_language(['Franz\xf6sisch', 'Fran\xe7ais', 'French'],u'fre',u''))
loader.save(create_languages_language(['Niederl\xe4ndisch', 'Hollandais', 'Dutch'],u'dut',u''))

loader.flush_deferred_objects()
