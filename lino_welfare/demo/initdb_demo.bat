@echo off
REM ~ python manage.py initdb std all_countries few_cities few_languages inscodes --traceback --noinput %*
REM ~ python manage.py initdb std props purposes all_countries be few_cities few_languages inscodes demo --traceback --noinput %*
python manage.py initdb std few_countries few_cities few_languages props cbss demo demo_events cpas_eupen --traceback --noinput %*
REM ~ python manage.py initdb std few_countries few_cities few_languages props cbss cpas_eupen demo_fr demo --traceback --noinput %*
REM ~ python manage.py initdb std all_countries be all_languages props demo --traceback %*
beep