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
import math

from constants import *

import incint

class TileAura(object):
    def __init__(self, inColor, tiles, auraID=0):

        self.alphaUp = True
        self.alpha = incint.IncInt(AURA_ALPHA_MIN,  AURA_ALPHA_MIN, AURA_ALPHA_MAX)
        self.color = inColor
        self.tiles = tiles

        self.aura = pygame.Surface(TILE_SIZE)
        self.red = inColor[0]
        self.green = inColor[1]
        self.blue = inColor[2]

        self.auraID = auraID

        self.fillColor()

    def update(self):
        if self.alpha.isMin():
            self.alphaUp = True
        if self.alpha.isMax():
            self.alphaUp = False


        count = AURA_ALPHA_SPEED
        while ((count > 0) and (not self.alpha.isBound())) or (count == AURA_ALPHA_SPEED):
            if self.alphaUp:
                self.alpha.inc()
            else:
                self.alpha.dec()
            count -= 1

        self.fillColor()
        self.aura.set_alpha(self.alpha.value)

    def fillColor(self):
        num = self.alpha.value - self.alpha.minimum
        tempRed = self.checkMax(self.red + num)
        tempGreen = self.checkMax(self.green + num)
        tempBlue = self.checkMax(self.blue + num)
        tempColor = (tempRed, tempGreen, tempBlue)
        self.aura.fill(tempColor)

    def checkMax(self, inVal):
        if inVal > 255:
            return 255
        else:
            return inVal
