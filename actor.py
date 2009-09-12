# Copyright 2009 Christopher Czyzewski, Daniel Tashjian
# This file is part of Project Mage.
#
#    Project Mage is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Project Mage is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Project Mage.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import pygame
import random

from constants import *

class Actor(object):
    def __init__(self, inName, inStats):
        #STR, MAG, SKI, VIT, WIL, SPD, MOVE, HP
        self.name = inName
        self.stats = inStats[:6]
        self.mov = inStats[6]
        self.hp = inStats[7]

    def getStats(self):
        return self.stats

    def takeDamage(self, damage):
        self.piece.hpCurr -= damage
        if self.piece.hpCurr < 0:
            self.piece.hpCurr = 0

    def _maxMana(self):
        maxMana = []

        for i in self.mana:
            maxMana.append(i * MAX_MANA_MULTIPLIER)

        return maxMana

    maxMana = property(_maxMana)
