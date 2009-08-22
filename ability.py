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
