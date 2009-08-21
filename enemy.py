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
import ai

class Enemy(object):
    def __init__(self, inName, inStats, inGift, inMage, inAbilities):

        self.name = inName

        #STR, MAG, SKI, VIT, WIL, SPD, MOVE, HP
        self.stats = [inStats[0], inStats[1], inStats[2],
                      inStats[3], inStats[4], inStats[5]]
        self.mov = inStats[6]
        self.hp = inStats[7]

        self.gift = [inGift[0], inGift[1], inGift[2]]

        self.piece = piece.Piece()

        self.isMage = inMage
        if self.isMage:
            self.mana = [20, 20, 20]
        else:
            self.mana = [0, 0, 0]

        self.piece.mpCurr = self.mana

        self.abilities = inAbilities

    def getStats(self):
        return self.stats

    def getStatsOrig(self):
        return [self.stats[0], self.stats[1], self.stats[2], self.stats[3],
                self.stats[4], self.stats[5], self.mov, self.hp]

    # Returns a class which when called returns an AI object.
    def getAI(self):
        return ai.null.NullCharacterAI

    def canUseAbility(self, ability):
        return all(map(lambda a, b: a <= b, ability.manaCost, self.piece.mpCurr))

    def getUsableAbilities(self):
        returnList = []
        for ab in self.abilities:
            if self.canUseAbility(ab):
                returnList.append(ab)
        return returnList

    def getAbilityPower(self, ability):
        if ability.statOff == "P":
            offStat = self.stats[0]
        else:
            offStat = self.stats[1]
        return float(ability.damage) * float(offStat)
