@echo off
REM ~ set REMOTE_USER=user
REM ~ set REMOTE_USER=lsaffre
REM ~ set REMOTE_USER=melanie
REM ~ set REMOTE_USER=alicia
REM ~ set REMOTE_USER=gerd
set REMOTE_USER=root
REM ~ set REMOTE_USER=
REM ~ set REMOTE_USER=karl
REM ~ set REMOTE_USER=elmar
REM ~ set REMOTE_USER=caroline
REM ~ set REMOTE_USER=kerstin
REM ~ if exist w:\*.* subst w: /d
REM ~ subst w: media\webdav 
start python manage.py runserver 
