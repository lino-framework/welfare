# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre.
# License: BSD, see LICENSE for more details.

"""This is the :xfile:`make_screenshots.py` script for `docs_de`.

It generates the :ref:`welfare.de.tour` page.

"""
from __future__ import unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lino.api.selenium import Album, runserver


def album1(driver):

    app = Album(
        driver, 'tour', title="Lino-Tour",
        ref="welfare.de.tour", intro="""

        Eine Serie von Bildschirmansichten um zu zeigen, wie Lino
        Welfare aussieht.

        Sie können die hier beschriebenen Aktionen auch selber
        nachspielen in unserer `Online-Demo
        <http://welfare-demo.lino-framework.org>`_

        """)

    app.checktitle("Lino Welfare")
    # app.checktitle("Lino für ÖSHZ")

    app.screenshot('login1.png', "Vor der Anmeldung", """

    Solange Sie sich nicht angemeldet haben, sind Sie ein anonymer
    Benutzer.  Lino spricht deshalb im folgenden Bildschirm noch
    Englisch (oder genauer gesagt die Sprache, die Sie in Ihrem
    Browser als bevorzugt eingestellt haben).

    Da es sich um eine Demo-Datenbank handelt, stehen hier
    alle Benutzer sowie deren Passwörter gezeigt, damit Sie die
    Unterschiede ausprobieren können.  Beachten Sie, dass *Sprache*
    und *Benutzerprofil* variieren.

    """)

    # elem = driver.find_element(By.XPATH, '//button[text()="Anmelden"]')
    elem = driver.find_element(By.XPATH, '//button[text()="Log in"]')
    elem.click()

    elem = driver.find_element(By.NAME, 'username')
    elem.send_keys("rolf")
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys("1234")

    app.screenshot('login2.png', "Das Anmeldefenster", """
    Wir melden uns an mit Benutzernamen "rolf" und Passwort "1234".
    """)

    elem.send_keys(Keys.RETURN)

    # elem = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located(
    #         (By.NAME, 'integ.UsersWithClients.grid')))

    app.stabilize()

    app.screenshot('welcome.png', "Der Startbildschirm", """
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

    app.screenshot('pcsw.Clients.grid.png', "Liste der Klienten", """
    Wählen Sie :menuselection:`Kontakte --> Klienten`, um die Liste
    aller Klienten zu zeigen.
    """)

    if False:
        driver.get("http://127.0.0.1:8000/api/pcsw/Clients?sp=true")
        app.stabilize()

    elem = driver.find_element(
        By.CLASS_NAME, "x-tbar-database_gear")
    elem.click()
    app.stabilize()

    if False:
        elem.screenshot("tour/database_gear.png")
        # ValueError: No JSON object could be decoded
        # https://github.com/SeleniumHQ/selenium/issues/912

    app.screenshot('pcsw.Clients.grid.params.png', "Filterparameter", """
    """)

    # find the first row and doubleclick it:
    elem = driver.find_elements(By.CLASS_NAME, 'x-grid3-row')[0]
    app.doubleclick(elem)

    app.stabilize()

    app.screenshot('pcsw.Clients.detail.png', "Detail Klient", """
    Doppelklick auf eine Zeile, um das Detail dieses Klienten zu zeigen.
    """)

    app.write_index()


if __name__ == '__main__':
    runserver('lino_welfare.projects.eupen.settings.demo', album1)


