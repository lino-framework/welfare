# -*- coding: UTF-8 -*-
logger.info("Loading 8 objects to table debts_group...")
# fields: id, name, ref, account_type, entries_layout
loader.save(create_debts_group(1,['Monatliche Eink\xfcnfte', 'Revenus mensuels', 'Monthly incomes'],u'10',u'I',u'11'))
loader.save(create_debts_group(2,['J\xe4hrliche Eink\xfcnfte', 'Revenus annuels', 'Yearly incomes'],u'20',u'I',u'30'))
loader.save(create_debts_group(3,['Monatliche Ausgaben', 'D\xe9penses mensuelles', 'Monthly expenses'],u'11',u'E',u'10'))
loader.save(create_debts_group(4,['Steuern', 'Taxes', 'Taxes'],u'40',u'E',u'10'))
loader.save(create_debts_group(5,['Versicherungen', 'Assurances', 'Insurances'],u'50',u'E',u'10'))
loader.save(create_debts_group(6,['Aktiva, Verm\xf6gen, Kapital', 'Actifs', 'Assets'],u'60',u'A',u'30'))
loader.save(create_debts_group(7,['Schulden, Zahlungsr\xfcckst\xe4nde, Kredite', 'Dettes, paiements en retard et cr\xe9dits', 'Debts, outsanding payments and credits'],u'70',u'L',u'20'))
loader.save(create_debts_group(8,['Gerichtsvollzieher und Inkasso', "Huissiers et agents d'encaissement", 'Bailiffs and cash collectors'],u'71',u'L',u'40'))

loader.flush_deferred_objects()
