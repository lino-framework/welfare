# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.


#~ from lino.utils import i2d, rstgen
from lino.utils import i2d
from lino.utils import babel

RELEASES = []

def released(version,date,lino_version='',changeset=''):
    RELEASES.insert(0,[version,i2d(date),lino_version,changeset])

released('1.0.2',20121120,None,'a44bff391952')
released('1.0.3',20121121)
released('1.0.4',20121130)
released('1.0.5',20121201,'1.5.2','a7cb6e85afe7')
released('1.0.6',20121210,'1.5.3')
released('1.0.7',20121211,'dev')



def as_index_rst(language=None):
    if language is not None:
        babel.set_language(language)
        
    #~ t = rstgen.SimpleTable('version released lino_version changeset'.split())
    #~ print t.to_rst([r[:4] for r in RELEASES])
    for version,date,lino_version,changeset in RELEASES:
        version = ":doc:`/releases/%s`" % version
        s = "- %s released %s" % (version,babel.dtosl(date))
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
    
        
        

if __name__ == "__main__":
    main()

