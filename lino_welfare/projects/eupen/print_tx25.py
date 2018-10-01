"""
Print a stored Tx25 response.

How to invoke::

  python manage.py run print_tx25.py ID

"""
from __future__ import print_function

import sys
from django.conf import settings
from lino.api.shell import rt
# from lino.modlib.printing.mixins import Printable


def main():

    # rt.startup()

    # settings.SITE.use_davlink = False

    Tx25 = rt.models.cbss.RetrieveTIGroupsRequests
    # ExcerptType = rt.models.excerpts.ExcerptType
    # Tx25 = rt.models.jobs.JobsOverview

    # et = ExcerptType.get_for_model(Tx25.model)
    # if not et.primary:
    #     raise Exception("Oops, %s is not primary" % et)

    if len(sys.argv) < 2:
        print("Must specify Lino number of Tx25. One of:")
        print(Tx25.model.objects
              .order_by('id').values_list('id', flat=True))
        sys.exit(-1)

    pk = int(sys.argv[1])

    ses = rt.login('hubert')
    obj = Tx25.model.objects.get(pk=pk)
    # if isinstance(obj, Printable):
    #     raise Exception("Oops, %s is a Printable" % obj)

    # print(ai)
    # print(rv['open_url'])
    # ses.run(ai)
    if obj.printed_by:
        # obj.printed_by.delete()
        obj.clear_cache()

    obj.do_print.run_from_ui(ses)

    rv = ses.response
    fn = rv['open_url']
    print(rv)
    print(settings.SITE.cache_dir + fn)


if __name__ == '__main__':
    main()
