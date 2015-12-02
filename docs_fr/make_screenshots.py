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
from selenium.webdriver.support import expected_conditions as EC

from lino.api.selenium import Album, runserver


def album1():

    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:8000/")
    app = Album(
        driver, 'tour', title="Le tour de Lino",
        ref="welfare.fr.tour", intro="""

        Un site de démonstraton en ligne se trouve sur
        http://welfare-demo.lino-framework.org

        Dort können Sie die folgenden Bildschirmansichten auch selber
        nachspielen.

        """)

    app.checktitle("Lino pour CPAS")

    app.screenshot('login1.png', "Avant l'identification", """

    Solange Sie sich nicht angemeldet haben, sind Sie ein anonymer
    Benutzer.  Da es sich um eine Demo-Datenbank handelt, stehen hier
    alle Benutzer sowie deren Passwörter gezeigt, damit Sie die
    Unterschiede ausprobieren können.  Beachten Sie, dass *Sprache*
    und *Benutzerprofil* variieren.  (Siehe
    :mod:`lino_welfare.modlib.welfare.roles`)

    """)

    elem = driver.find_element(By.XPATH, '//button[text()="Se connecter"]')
    elem.click()

    app.screenshot('login2.png', "S'identifier", """
    Nous nous connectons avec le nom de "romain" et mot de passe "1234".
    """)

    elem = driver.find_element(By.NAME, 'username')
    elem.send_keys("romain")
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys("1234")
    elem.send_keys(Keys.RETURN)

    app.stabilize()

    app.screenshot('welcome.png', "Après l'identification", """
    Nous voici dans l'écran d'accueil. Il consiste d'une série d'éléments:

    - Le menu principal
    - Les raccourcis ("quick links")
    - Les messages d'accueil
    - Un certain nombre de tables

    """)

    elem = driver.find_element(By.XPATH, '//button[text()="Contacts"]')
    elem.click()

    app.screenshot('menu_kontakte.png', "Le menu :menuselection:`Contacts`")

    # elem = driver.find_element(By.XPATH, '//button[text()="▶ Klienten"]')
    elem = driver.find_element(By.LINK_TEXT, "▶ Bénéficiaires")
    elem.click()

    app.stabilize()

    app.screenshot('contacts.Clients.grid.png', "La liste des bénéficiaires", """
    Wählen Sie :menuselection:`Kontakte --> Klienten`, um die Liste
    aller Klienten zu zeigen.
    """)

    # find the first row and doubleclick it:
    elem = driver.find_elements(By.CLASS_NAME, 'x-grid3-row')[0]
    app.doubleclick(elem)

    app.stabilize()

    app.screenshot('contacts.Clients.detail.png', "Le détail d'un bénéficiaire", """
    Doppelklick auf eine Zeile, um das Detail dieses Klienten zu zeigen.
    """)

    app.write_index()

    driver.quit()


if __name__ == '__main__':
    runserver('lino_welfare.projects.chatelet.settings.demo', album1)


