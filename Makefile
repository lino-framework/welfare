DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
ROOTDIR := /cygdrive/t/hgwork/welfare
#~ ROOTDIR = `pwd`
ROOTDIR := `cygpath -m $(ROOTDIR)`
#~ ROOTDIR := `cygpath -m \`pwd\``
MODULES = pcsw courses cbss debts cv isip jobs newcomers belstat
TESTS_OPTIONS = --verbosity=2 --traceback
MMOPTS := -s -a --settings lino_welfare.modlib.pcsw.settings
CMOPTS := --settings lino_welfare.modlib.pcsw.settings

#LANGUAGES = de fr nl et
#INPUT_FILES = lino\\actions.py lino\\ui\\extjs\\ext_ui.py lino\\modlib\\fields.py lino\\modlib\\system\\models.py

.PHONY: mm cm makedocs tests sdist

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm     run django-admin makemessages on modlib"
	@echo "  cm     run django-admin compilemessages on modlib"
	@echo "  tests  run Lino test suite"
  

ss:
	phantomjs --config=screenshots-config.json screenshots.js
  
mm:
	pwd
	for MOD in $(MODULES); do \
	  cd $(ROOTDIR)/lino_welfare/modlib/$$MOD && pwd && $(DJANGO_ADMIN) makemessages $(MMOPTS); \
	done
  

cm:  
	@for MOD in $(MODULES); \
	do \
	  cd $(ROOTDIR)/lino_welfare/modlib/$$MOD && $(DJANGO_ADMIN) compilemessages $(CMOPTS); \
	done
  
tests:  
	$(DJANGO_ADMIN) test --settings=lino_welfare.modlib.pcsw.settings $(TESTS_OPTIONS)

sdist:
	python setup.py sdist --formats=gztar,zip --dist-dir=../lino/docs/dl 
	#~ python setup.py register sdist --formats=gztar,zip upload 
	#~ python setup.py sdist --formats=gztar,zip --dist-dir=docs/dist
  
upload:
	python setup.py sdist --formats=gztar,zip --dist-dir=../lino/docs/dl upload 
  
  
