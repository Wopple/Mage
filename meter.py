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

import sys
import pygame
from pygame.locals import *
from math import sqrt
import random

class Meter:

    def __init__ (self, loc, sizeX, sizeY, valMax, colorFull, colorEmpty, colorFlash=(255, 255, 255), colorSegment=(255, 255, 255)):
        self.loc = [loc[0], loc[1]]
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.valMax = valMax
        self.val = valMax
        self.colorFull = colorFull
        self.colorEmpty = colorEmpty
        self.colorFlash = colorFlash
        self.colorSegment = colorSegment
        self.flash = False
        self.flashCount = 0
        self.flashTick = 3
        self.segment = 0

        self.bar = pygame.Surface((self.sizeX, self.sizeY))

        if self.valMax == 0:
            print "Error: Illegal zero value - Meter"
            sys.exit()

    def update(self, val):
        if val > self.valMax:
            val = self.valMax
        self.val = val

        if self.segment < 0:
            self.segment = 0

    def draw(self, screen):
        mainPane = pygame.Surface((self.sizeX, self.sizeY))
        
        fillNum = int((float(self.val) / float(self.valMax)) * self.sizeX)
        
        if self.flash:
            self.flashCount += 1
            if self.flashCount > self.flashTick:
                self.flashCount = 0
                self.flash = False
            self.bar.fill (self.colorFlash)
        else:
            self.bar.fill (self.colorEmpty)
            self.bar.fill (self.colorFull, (0, 0, fillNum, self.sizeY))

        mainPane.blit(self.bar, (0, 0))

        if self.segment > 0:
            tempSize = int((float(self.segment) / float(self.valMax)) * self.sizeX)
            tempPane = pygame.Surface((tempSize, self.sizeY))
            tempPane.fill (self.colorSegment)
            mainPane.blit(tempPane, ((fillNum - tempSize), 0))

        screen.blit(mainPane, self.loc)

    def center(self, baseRect, doHoriz, doVert):
        if doHoriz:
            self.loc[0] = (baseRect.width / 2) - (self.sizeX / 2)
        if doVert:
            self.loc[1] = (baseRect.height / 2) - (self.sizeY / 2)
