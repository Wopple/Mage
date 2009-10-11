import os
import sys
import pygame
import random

from constants import *

class Ability(object):
    def __init__(self, inName, inDesc, inMinRange, inMaxRange,
                 inAOE, inDamage, inAccuracy, inStun, inSpecial,
                 inManaCost, inStatOff, inStatDef):

        self.name = inName
        self.desc = inDesc

        self.minRange = inMinRange
        self.maxRange = inMaxRange

        self.AOE = inAOE

        self.damage = inDamage
        self.accuracy = inAccuracy

        self.stun = inStun

        self.special = inSpecial

        self.manaCost = inManaCost

        self.statOff = inStatOff
        self.statDef = inStatDef

        self.tempFlag = True

    def getAOEType(self):
        if self.AOE == 0:
            return 0
        elif self.AOE >= 1 and self.AOE <= 3:
            return 1
        else:
            return 2

    def getAOERange(self):
        if self.AOE == 0:
            rangeMin = 0
            rangeMax = 0
        elif self.AOE == 1:
            rangeMin = 1
            rangeMax = 2
        elif self.AOE == 2:
            rangeMin = 1
            rangeMax = 3
        elif self.AOE == 4:
            rangeMin = 1
            rangeMax = 1
        elif self.AOE == 5:
            rangeMin = 0
            rangeMax = 2
        elif self.AOE == 6:
            rangeMin = 0
            rangeMax = 3
        else:
            rangeMin = 0
            rangeMax = 0

        return (rangeMin, rangeMax)
