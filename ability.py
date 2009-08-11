import os
import sys
import pygame
import random

from constants import *

class Ability(object):
    def __init__(self, inName, inDesc, inMinRange, inMaxRange, inPower, inManaCost):

        self.name = inName
        self.desc = inDesc

        self.minRange = inMinRange
        self.maxRange = inMaxRange

        self.power = inPower

        self.manaCost = inManaCost
