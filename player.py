# Copyright 2009 Christopher Czyzewski
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

import piece

import actor

class Player(actor.Actor):
    def __init__(self, inName, inClass, inStats, inStatGrowths, inMana, inPortrait, inAttack, inSpells):
        super(Player, self).__init__(inName, inStats)
        
        self.className = inClass

        self.isMage = True
        
        self.statGrowths = inStatGrowths

        self.mana = [inMana[0], inMana[1], inMana[2]]

        self.piece = piece.Piece()
        self.level = 1
        self.portrait = inPortrait

        self.abilities = inSpells
        self.attackAbility = inAttack

    def getMana(self):
        return self.mana

    def getInfo(self):
        return [self.name, self.className, self.level, self.hp, self.hp, self.mov, "No Status"]

    def xpToNextLevel(self):
        return (int(XP_FORMULA_A + (XP_FORMULA_B ** ((XP_FORMULA_C * self.level) + XP_FORMULA_D))))

    def levelUp(self):
        if self.level < MAX_LEVEL:
            self.level += 1

