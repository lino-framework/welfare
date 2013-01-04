@echo off
set YEAR=2013
if not exist ..\lino\docs\blog\%YEAR%\%1.rst goto error
hg ci -m http://code.google.com/p/lino/source/browse/docs/blog/%YEAR%/%1.rst
goto :ende
:error
echo oops! blog file does not exist: docs\en\blog\%YEAR%\%1.rst 
:ende
