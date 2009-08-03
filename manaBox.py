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

import box
import background
import scrollingBackground
import textrect
import incint

from constants import *

MANA_BOX_IMAGE = None
MANA_BOX_SIZE = None

MANA_TICKS = None

class ManaBox(object):
    def __init__(self):

        global MANA_BOX_IMAGE
        global MANA_BOX_SIZE
        if MANA_BOX_IMAGE is None:
            self.createImage()

        self.rect = pygame.Rect((0, 0), MANA_BOX_SIZE)

        self.updateBlank()

    def createImage(self):
        global MANA_BOX_IMAGE
        global MANA_BOX_SIZE
        global MANA_TICKS

        statText = ["RAGE", "SPIRIT", "FOCUS"]
        tempRect = pygame.Rect( (0, 0), MANA_BOX_ELEMENT_SIZE )
        tempFont = pygame.font.Font(MANA_BOX_FONT, MANA_BOX_FONT_SIZE)
        sizeX = (MANA_BOX_ELEMENT_SIZE[0]) + (MANA_BOX_BORDER_SIZE * 2) + (MANA_BOX_PADDING * 3) + (MANA_TICK_SPACING * (MANA_MAX - 1)) + (MANA_TICK_SIZE[0] * MANA_MAX)
        sizeY = (MANA_BOX_ELEMENT_SIZE[1] * 3) + (MANA_BOX_BORDER_SIZE * 2) + (MANA_BOX_PADDING * 2)

        tempRect = pygame.Rect((0, 0), (sizeX, sizeY))
        tempBox = box.Box(tempRect, MANA_BOX_PATTERN, MANA_BOX_PATTERN_SIZE,
                           MANA_BOX_BORDER, MANA_BOX_BORDER_SIZE)


        for x in range(3):
            textrect1 = textrect.render_textrect(statText[x], tempFont, tempRect,
                                                 BOX_FONT_COLOR, (0, 0, 0), 0, True)
            tempX = MANA_BOX_BORDER_SIZE + MANA_BOX_PADDING
            tempY = MANA_BOX_BORDER_SIZE + (MANA_BOX_PADDING * (x+1)) + (MANA_BOX_ELEMENT_SIZE[1] * x)
            MANA_BOX_SIZE = (sizeX, sizeY)
            tempRect = pygame.Rect((0, 0), (sizeX, sizeY))
            tempBox.mainPane.blit(textrect1, (tempX, tempY))

        MANA_BOX_IMAGE = tempBox.mainPane

        MANA_TICKS = []
        for m in range(4):
            tempSurface = pygame.Surface(MANA_TICK_SIZE)
            tempSurface.fill(MANA_TICK_COLORS[m])
            MANA_TICKS.append(tempSurface)
            

    def draw(self, screen):
        mainPane = pygame.Surface( (self.rect.width, self.rect.height) )
        mainPane.blit(MANA_BOX_IMAGE, (0, 0))
        mainPane.blit(self.tickPane, (0, 0))
        #mainPane.blit(self.numberPane, (0, 0))
        screen.blit(mainPane, self.rect.topleft)

    def center(self, baseRect, doHoriz, doVert):
        if doHoriz:
            self.rect.left = (baseRect.width / 2) - (self.rect.width / 2)
        if doVert:
            self.rect.top = (baseRect.height / 2) - (self.rect.height / 2)

    def update(self, mana):
        self.tickPane = pygame.Surface((self.rect.width, self.rect.height))
        self.tickPane.set_colorkey(BLACK)
        self.tickPane.fill(BLACK)
        
        for m in range(3):
            for t in range(MANA_MAX):
                if t < mana[m]:
                    color = m
                else:
                    color = 3

                tempX = MANA_BOX_BORDER_SIZE + (MANA_BOX_PADDING * 2) + MANA_BOX_ELEMENT_SIZE[0] + ((MANA_TICK_SIZE[0] + MANA_TICK_SPACING) * t)
                tempY = MANA_BOX_BORDER_SIZE + ((MANA_TICK_SIZE[1] + MANA_BOX_PADDING) * m)
                self.tickPane.blit(MANA_TICKS[color], (tempX, tempY))

    def updateBlank(self):
        self.update([0, 0, 0])

