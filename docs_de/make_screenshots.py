# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre.
# License: BSD, see LICENSE for more details.

"""This is the :xfile:`make_screenshots.py` script for `docs_de`.

It generates the :ref:`welfare.de.screenshots` page.

"""
from __future__ import unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lino.api.selenium import Album, runserver


def album1():

    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:8000/")
    app = Album(
        driver, 'screenshots', title="Bildertour",
        ref="welfare.de.screenshots", intro="""

        Die Online-Demo von Lino Welfare befindet sich unter
        http://welfare-demo.lino-framework.org

        Dort können Sie die folgenden Bildschirmansichten auch selber
        nachspielen.

        """)

    app.checktitle("Lino für ÖSHZ")

    app.screenshot('login1.png', "Vor der Anmeldung", """

    Solange Sie sich nicht angemeldet haben, sind Sie ein anonymer
    Benutzer.  Da es sich um eine Demo-Datenbank handelt, stehen hier
    alle Benutzer sowie deren Passwörter gezeigt, damit Sie die
    Unterschiede ausprobieren können.  Beachten Sie, dass *Sprache*
    und *Benutzerprofil* variieren.  (Siehe
    :mod:`lino_welfare.modlib.welfare.roles`)

    """)

    elem = driver.find_element(By.XPATH, '//button[text()="Anmelden"]')
    elem.click()

    app.screenshot('login2.png', "Das Anmeldefenster", """
    Wir melden uns an mit Benutzernamen "rolf" und Passwort "1234".
    """)

    elem = driver.find_element(By.NAME, 'username')
    elem.send_keys("rolf")
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys("1234")
    elem.send_keys(Keys.RETURN)

    # elem = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located(
    #         (By.NAME, 'integ.UsersWithClients.grid')))

    app.stabilize()

    app.screenshot('welcome.png', "Nach der Anmeldung", """
    Das ist der Startbildschirm. Hier haben wir eine Serie von Elementen:

    - Das Hauptmenü
    - Quicklinks
    - Begrüßungsmeldungen
    - Diverse Tabellen

    """)

    elem = driver.find_element(By.XPATH, '//button[text()="Kontakte"]')
    elem.click()

    app.screenshot('menu_kontakte.png', "Das Menü :menuselection:`Kontakte`")

    # elem = driver.find_element(By.XPATH, '//button[text()="▶ Klienten"]')
    elem = driver.find_element(By.LINK_TEXT, "▶ Klienten")
    elem.click()

    app.stabilize()

    app.screenshot('contacts.Clients.grid.png', "Liste der Klienten", """
    Wählen Sie :menuselection:`Kontakte --> Klienten`, um die Liste
    aller Klienten zu zeigen.
    """)

    # find the first row and doubleclick it:
    elem = driver.find_elements(By.CLASS_NAME, 'x-grid3-row')[0]
    app.doubleclick(elem)

    app.stabilize()

    app.screenshot('contacts.Clients.detail.png', "Detail Klient", """
    Doppelklick auf eine Zeile, um das Detail dieses Klienten zu zeigen.
    """)

    app.write_index()

    driver.quit()


if __name__ == '__main__':
    runserver('lino_welfare.projects.eupen.settings.demo', album1)


