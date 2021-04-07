# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre.
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This is the :xfile:`make_screenshots.py` script for `docs_de`.

It generates the :ref:`welfare.de.screenshots` page.

"""
from __future__ import unicode_literals

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from lino.api.selenium import Album, runserver


def album1(driver):

    app = Album(
        driver, 'tour', title="Tour de Lino",
        ref="welfare.fr.tour", intro="""

        Voici un petit tour dans Lino Welfare.

        Vous pouvez également aller jouer vous-même sur notre `site de
        démonstraton en ligne <https://welfare-demo.lino-framework.org>`_

        """)

    app.checktitle("Lino Welfare")

    app.stabilize()
    app.screenshot('login1.png', "Avant l'identification", """

    Tant que vous êtes anonyme, Lino parlera la langue préférée configurée de
    votre navigateur.
    Choisissez un des noms d'utilisateur pour vous connecter.
    Notez que la langue et les droits d'accès dépendront de votre choix.
    Voir également :doc:`/users`.

    """)

    elem = driver.find_element(By.XPATH, '//button[text()="Log in"]')
    elem.click()

    elem = driver.find_element(By.NAME, 'username')
    elem.send_keys("romain")
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys("1234")

    app.screenshot('login2.png', "S'identifier", """

    Pour ce tour nous nous connectons avec le nom de "romain" et mot
    de passe "1234".

    """)

    elem.send_keys(Keys.RETURN)

    app.stabilize()

    app.screenshot('welcome.png', "L'écran d'accueil", """
    Nous voici dans l'écran d'accueil. Il contient une série d'éléments:

    - Le menu principal
    - Les raccourcis ("quick links")
    - Les messages d'accueil
    - Un certain nombre de tableaux avec des informations diverses

    """)

    elem = driver.find_element(By.XPATH, '//button[text()="Contacts"]')
    elem.click()

    app.screenshot('menu_contacts.png', "Le menu :menuselection:`Contacts`", """

    Dans Lino Welfare, les "contacts" sont toutes les personnes et
    organisations extérieures.

    """)

    # elem = driver.find_element(By.XPATH, '//button[text()="▶ Klienten"]')
    elem = driver.find_element(By.LINK_TEXT, "▶ Bénéficiaires")
    elem.click()
    app.stabilize()

    app.screenshot('pcsw.Clients.grid.png', "La liste des bénéficiaires", """

    Sélectionnez :menuselection:`Contacts --> Bénéficiaires` pour
    ouvrir la liste générale des bénéficiaires.

    """)

    elem = driver.find_element(
        By.CLASS_NAME, "x-tbar-database_gear")
    elem.click()
    app.stabilize()
    app.screenshot('pcsw.Clients.grid.params.png', "Le panneau à paramètres", """

    Le panneau à paramètres vous permet d'appliquer des conditions de
    filtre pour sélectionner les données voulues.

    """)

    # find the first row and doubleclick it:
    elem = driver.find_elements(By.CLASS_NAME, 'x-grid3-row')[0]
    app.doubleclick(elem)

    app.stabilize()

    app.screenshot('pcsw.Clients.detail.png', "Le détail d'un bénéficiaire", """

    Pour voir le détail d'un bénéficiaire, vous double-cliquez sur la
    ligne en question.

    """)

    up_buttons = driver.find_elements(By.CLASS_NAME, 'x-tool-up')
    print(len(up_buttons))
    elem = up_buttons[0]
    elem.click()

    app.stabilize()

    app.screenshot(
        'pcsw.Clients.AppointmentsByPartner.png',
        "Les rendez-vous d'un bénéficiaire", """

    Pour voir tous les rendez-vous d'un bénéficiaire, cliquez sur le
    symbole dans le coin supérieur droit pour ouvrir le panneau dans
    sa propre fenetre.

    """)

    elem.send_keys(Keys.ESCAPE)

    app.stabilize()

    tab1 = driver.find_element(By.LINK_TEXT, 'Personne')
    app.hover(tab1)
    # tab2 = driver.find_element(By.LINK_TEXT, 'Situation familiale')
    tabs = driver.find_elements(By.CLASS_NAME, 'x-tab-right')
    print(len(tabs), [e.text for e in tabs])
    tab2 = tabs[0]
    tab2.click()
    app.stabilize()

    app.screenshot(
        'pcsw.Clients.detail2.png',
        "Intervenants d'un bénéficiaire", """

    Le deuxième onglet du détail d'un bénéficiaire...

    """)

    app.write_index()


if __name__ == '__main__':
    runserver('lino_welfare.projects.chatelet.settings.demo', album1)


