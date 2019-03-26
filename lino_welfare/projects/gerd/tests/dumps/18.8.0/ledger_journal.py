# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table ledger_journal...")
# fields: id, ref, seqno, name, build_method, template, trade_type, voucher_type, journal_group, auto_check_clearings, auto_fill_suggestions, force_sequence, account, partner, printed_name, dc, yearly_numbering, must_declare, sepa_account
loader.save(create_ledger_journal(1,u'REG',1,['Rechnungseing\xe4nge', "Factures \xe0 l'entr\xe9e", 'Incoming invoices'],None,u'',u'P','vatless.ProjectInvoicesByJournal',u'20',True,True,False,None,None,['', '', ''],False,True,True,None))
loader.save(create_ledger_journal(2,u'SREG',2,['Sammelrechnungen', 'Sammelrechnungen', 'Collective purchase invoices'],None,u'',u'P','vatless.InvoicesByJournal',u'20',True,True,False,None,None,['', '', ''],False,True,True,None))
loader.save(create_ledger_journal(3,u'AAW',3,['Ausgabeanweisungen', 'Ausgabeanweisungen', 'Disbursement orders'],None,u'',u'P','finan.DisbursementOrdersByJournal',u'40',True,True,False,21,None,['', '', ''],False,True,True,None))
loader.save(create_ledger_journal(4,u'ZKBC',4,['KBC Zahlungsauftr\xe4ge', 'KBC Zahlungsauftr\xe4ge', 'KBC Payment Orders'],None,u'',None,'finan.PaymentOrdersByJournal',u'50',True,True,False,3,None,['', '', ''],False,True,True,None))

loader.flush_deferred_objects()
