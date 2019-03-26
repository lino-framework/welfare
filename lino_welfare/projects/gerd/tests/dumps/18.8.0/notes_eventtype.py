# -*- coding: UTF-8 -*-
logger.info("Loading 10 objects to table notes_eventtype...")
# fields: id, name, remark, body
loader.save(create_notes_eventtype(1,['Aktennotiz', '', ''],u'Alle Notizen/Ereignisse, die keine andere Form haben',['', '', '']))
loader.save(create_notes_eventtype(2,['Brief', '', ''],u'Brief an Kunde, Personen, Organisationen',['', '', '']))
loader.save(create_notes_eventtype(3,['E-Mail', '', ''],u'E-Mail an Kunde, Personen, Organisationen',['', '', '']))
loader.save(create_notes_eventtype(4,['Einschreiben', '', ''],u'Brief, der per Einschreiben an Kunde oder an externe Personen / Dienst verschickt wird',['', '', '']))
loader.save(create_notes_eventtype(5,['Gespr\xe4ch EXTERN', '', ''],u'Pers\xf6nliches Gespr\xe4ch au\xdferhalb des \xd6SHZ, wie z.B. Vorstellungsgespr\xe4ch im Betrieb, Auswertungsgespr\xe4ch, gemeinsamer Termin im Arbeitsamt, im Integrationsprojekt, .',['', '', '']))
loader.save(create_notes_eventtype(6,['Gespr\xe4ch INTERN', '', ''],u'Pers\xf6nliches Gespr\xe4ch im \xd6SHZ',['', '', '']))
loader.save(create_notes_eventtype(7,['Hausbesuch', '', ''],u'Hausbesuch beim Kunden',['', '', '']))
loader.save(create_notes_eventtype(8,['Kontakt \xd6SHZ intern', '', ''],u'Kontakte mit Kollegen oder Diensten im \xd6SHZ, z.B. Fallbesprechung mit Allgemeinem Sozialdienst, Energieberatung, Schuldnerberatung, Sekretariat, ...',['', '', '']))
loader.save(create_notes_eventtype(9,['Telefonat', '', ''],u'Telefonischer Kontakt mit dem Kunden, anderen Personen, Diensten oder Organisationen ....',['', '', '']))
loader.save(create_notes_eventtype(10,['System note', 'System note', 'System note'],u'',['', '', '']))

loader.flush_deferred_objects()
