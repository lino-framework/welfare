Releases
========

.. py2rst::

  from atelier.sphinxconf import version2rst
  import lino_welfare
  version2rst(self,lino_welfare)

Older releases
--------------

.. toctree::
   :maxdepth: 1
   :glob:

   1.0.?
   1.0.1?
   1.1.?



.. py2rst::

  #~ from lino.utils import i2d, rstgen
  from lino.utils import i2d
  from north import dbutils

  RELEASES = []

  def released(version,date,lino_version='',changeset=''):
      RELEASES.insert(0,[version,i2d(date),lino_version,changeset])

  released('1.0.2',20121120,None,'a44bff391952')
  released('1.0.3',20121121)
  released('1.0.4',20121130)
  released('1.0.5',20121201,'1.5.2','a7cb6e85afe7')
  released('1.0.6',20121210,'1.5.3')
  released('1.0.7',20121211,'dev')
  released('1.0.8',20131211,'dev')

  def as_index_rst(language=None):
      if language is not None:
          dbutils.set_language(language)
          
      #~ t = rstgen.SimpleTable('version released lino_version changeset'.split())
      #~ print t.to_rst([r[:4] for r in RELEASES])
      for version,date,lino_version,changeset in RELEASES:
          version = ":doc:`/releases/%s`" % version
          s = "- %s released %s" % (version,dbutils.dtosl(date))
          if lino_version:
              s += ", requires Lino `" + lino_version 
              s += " <http://lino-framework.org/releases/" + lino_version + ".html>`_"
          if changeset:
              s += ", :checkin:`%s`" % changeset
          print s
          
      print """
      
  .. toctree::
     :maxdepth: 1
     :hidden:

     coming"""
     
      for version,date,lino_version,changeset in RELEASES:
          print "   " + version

  # as_index_rst('de')
  
