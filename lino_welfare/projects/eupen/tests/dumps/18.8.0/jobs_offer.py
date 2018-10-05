# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table jobs_offer...")
# fields: id, sector, function, name, provider, selection_from, selection_until, start_date, remark
loader.save(create_jobs_offer(1,1,1,u'\xdcbersetzer DE-FR (m/w)',191,date(2014,1,22),date(2014,5,2),date(2014,6,1),u'Wir sind auf der Suche nach einem Deutsch-Franz\xf6sich \xdcbersetzer \n(M/F) um einen Selbst\xe4ndigenr zu Gesch\xe4ftsessen und kommerziellen \nTermine zu begleiten. Sie \xfcbernehmen die \xdcbersetzung von Gespr\xe4che \nw\xe4hrend kommerziellen Kontakte mit deutschen Kunden.\nEs ist spontane und p\xfcnktliche Auftr\xe4ge, den ganzen Tag, in\nEupen und/oder Deutschland.\nRegelm\xe4\xdfigkeit: 1-2 Mal pro Monat, je nach Bedarf.\nFlexibilit\xe4t: die Termine sind je nach Kandidat anpassbar.'))

loader.flush_deferred_objects()
