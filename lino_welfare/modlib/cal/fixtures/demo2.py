from lino.modlib.cal.fixtures.demo2 import objects as lino_objects
from lino import dd
from lino.utils import Cycler

def objects():
    Client = dd.resolve_model('pcsw.Client')
    CLIENTS = Cycler(Client.objects.all())
    for obj in lino_objects():
        if obj.__class__.__name__ == 'Event':
            if obj.calendar.invite_client:
                obj.project = CLIENTS.pop()
        yield obj
