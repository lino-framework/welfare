DJANGO_ADMIN = python l:\\snapshots\\django\\django\\bin\\django-admin.py
LINO_ROOT := /cygdrive/t/hgwork/welfare
LINO_ROOT := `cygpath -m $(LINO_ROOT)`
APPS = pcsw
MODULES = courses cbss debts households cv isip jobs newcomers 
TESTS_OPTIONS = --verbosity=2 --traceback
MMOPTS := -s -a --settings lino_welfare.settings
CMOPTS := --settings lino_welfare.settings

#LANGUAGES = de fr nl et
#INPUT_FILES = lino\\actions.py lino\\ui\\extjs\\ext_ui.py lino\\modlib\\fields.py lino\\modlib\\system\\models.py

.PHONY: mm cm makedocs tests sdist

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm     run django-admin makemessages on modlib"
	@echo "  cm     run django-admin compilemessages on modlib"
	@echo "  tests  run Lino test suite"
  

mm:
	#~ $(DJANGO_ADMIN) dtl2py --settings lino.apps.pcsw.settings
	#~ $(DJANGO_ADMIN) dtl2py --settings lino.apps.igen.settings
	#~ export DJANGO_SETTINGS_MODULE=lino.apps.pcsw.settings
	pwd
	for MOD in $(MODULES); do \
	  cd $(LINO_ROOT)/lino_welfare/modlib/$$MOD && pwd && $(DJANGO_ADMIN) makemessages $(MMOPTS); \
	done
	for i in $(APPS); do \
    cd $(LINO_ROOT)/lino/apps/$$i && pwd && $(DJANGO_ADMIN) makemessages $(MMOPTS); \
	done
  

cm:  
	#~ export DJANGO_SETTINGS_MODULE=lino.apps.pcsw.settings
	cd $(LINO_ROOT)/lino && $(DJANGO_ADMIN) compilemessages $(CMOPTS)
	@for MOD in $(MODULES); \
	do \
	  cd $(LINO_ROOT)/lino/modlib/$$MOD && $(DJANGO_ADMIN) compilemessages $(CMOPTS); \
	done
	for i in $(APPS); do \
	  cd $(LINO_ROOT)/lino/apps/$$i && $(DJANGO_ADMIN) compilemessages $(CMOPTS); \
	done
  
tests:  
	$(DJANGO_ADMIN) test --settings=lino_welfare.settings $(TESTS_OPTIONS)


sdist:
	python setup.py register sdist --formats=gztar,zip --dist-dir=docs/dist upload 
	#~ python setup.py sdist --formats=gztar,zip --dist-dir=docs/dist
  
html:
	cd docs ; export DJANGO_SETTINGS_MODULE=lino_welfare.settings ; make html

upload:
	cd docs ; make upload
	