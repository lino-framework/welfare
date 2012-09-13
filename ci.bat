@echo off
set YEAR=2012
if not exist docs\en\blog\%YEAR%\%1.rst goto error
hg ci -m http://code.google.com/p/lino-welfare/source/browse/docs/en/blog/%YEAR%/%1.rst
goto :ende
:error
echo oops! blog file does not exist: docs\en\blog\%YEAR%\%1.rst 
:ende
