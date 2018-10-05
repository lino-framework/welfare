# -*- coding: UTF-8 -*-
logger.info("Loading 8 objects to table ledger_paymentterm...")
# fields: id, ref, name, days, months, end_of_month, printed_text
loader.save(create_ledger_paymentterm(1,u'PIA',['Vorauszahlung', 'Vorauszahlung', 'Payment in advance'],0,0,False,['', '', '']))
loader.save(create_ledger_paymentterm(2,u'07',['Zahlung sieben Tage Rechnungsdatum', 'Zahlung sieben Tage Rechnungsdatum', 'Payment seven days after invoice date'],7,0,False,['', '', '']))
loader.save(create_ledger_paymentterm(3,u'10',['Zahlung zehn Tage Rechnungsdatum', 'Zahlung zehn Tage Rechnungsdatum', 'Payment ten days after invoice date'],10,0,False,['', '', '']))
loader.save(create_ledger_paymentterm(4,u'30',['Zahlung 30 Tage Rechnungsdatum', 'Zahlung 30 Tage Rechnungsdatum', 'Payment 30 days after invoice date'],30,0,False,['', '', '']))
loader.save(create_ledger_paymentterm(5,u'60',['Zahlung 60 Tage Rechnungsdatum', 'Zahlung 60 Tage Rechnungsdatum', 'Payment 60 days after invoice date'],60,0,False,['', '', '']))
loader.save(create_ledger_paymentterm(6,u'90',['Zahlung 90 Tage Rechnungsdatum', 'Zahlung 90 Tage Rechnungsdatum', 'Payment 90 days after invoice date'],90,0,False,['', '', '']))
loader.save(create_ledger_paymentterm(7,u'EOM',['Zahlung Monatsende', 'Zahlung Monatsende', 'Payment end of month'],0,0,True,['', '', '']))
loader.save(create_ledger_paymentterm(8,u'P30',['Anzahlung 30%', 'Anzahlung 30%', 'Prepayment 30%'],30,0,False,['Prepayment <b>30%</b> \n    ({{(obj.total_incl*30)/100}} {{obj.currency}})\n    due on <b>{{fds(obj.due_date)}}</b>, remaining \n    {{obj.total_incl - (obj.total_incl*30)/100}} {{obj.currency}}\n    due 10 days before delivery.\n    ', '', '']))

loader.flush_deferred_objects()
