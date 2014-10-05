===============
Bescheinigungen
===============


Anwesenheitsbescheinigung
=========================

Um eine Anwesenheitsbescheinigung auszustellen, muss der Klient
"anwesend" gewesen sein.  Also es muss ein :term:`Termin` oder eine
:term:`Visite` existieren, für die dieser Klient als Gast eingetragen
ist. Diese Einträge sind es, die man sieht im Feld "Termine" des
Reiters "Person" im Detail des Klienten.


Hilfebestätigungen
==================

Siehe :doc:`aids`.


Beispiele
=========

Hier einige Beispiele von Ausdrucken aus der Demo-Datenbank.



.. django2rst::

    import os
    import shutil
    from atelier import rstgen
    ses = rt.login()
    def asli(obj):
        rv = ses.run(obj.do_print)
        if rv['success']:
            pass
            # print("\n\n%s\n\n" % rv['open_url'])
        else:
            raise Exception("Oops: %s" % rv['message'])
        if not 'open_url' in rv:
            raise Exception("Oops: %s" % rv['message'])
        tmppath = settings.SITE.project_dir + rv['open_url']
        head, tail = os.path.split(tmppath)
        # tail = 'tested/' + tail
        tail = 'dl/excerpts/' + tail
        kw = dict(tail=tail)
        kw.update(type=obj.excerpt_type)
        kw.update(owner=obj.owner)
        try:
            shutil.copyfile(tmppath, tail)
        except IOError as e:
            kw.update(error=str(e))
            msg = "%(type)s %(owner)s %(tail)s Oops: %(error)s" % kw
            # raise Exception(msg)
            return msg
        return "%(type)s `%(owner)s <../%(tail)s>`__" % kw
    
    print(rstgen.ul([asli(o) for o in excerpts.Excerpt.objects.all()]))
   

