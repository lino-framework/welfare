# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""

from lino.utils import Cycler
from lino.api import rt


def objects():

    Obstacle = rt.modules.cv.Obstacle
    ObstacleType = rt.modules.cv.ObstacleType
    Client = rt.modules.pcsw.Client
    ClientStates = rt.modules.pcsw.ClientStates

    CLIENTS = Cycler(Client.objects.filter(
        client_state=ClientStates.coached)[10:15])

    TYPES = Cycler(ObstacleType.objects.all())

    for i in range(20):
        yield Obstacle(person=CLIENTS.pop(), type=TYPES.pop())
