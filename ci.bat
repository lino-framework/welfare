@echo off
set YEAR=2012
if not exist docs\en\blog\%YEAR%\%1.rst goto error
hg ci -m http://code.google.com/p/lino-welfare/source/browse/docs/blog/%YEAR%/%1.rst
goto :ende
:error
echo oops! file does not exist: docs\blog\%YEAR%\%1.rst 
:ende
