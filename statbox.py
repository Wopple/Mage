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

STAT_BOX_IMAGE = None
STAT_BOX_SIZE = None

class StatBox(object):
    def __init__(self):
        
        global STAT_BOX_IMAGE
        global STAT_BOX_SIZE
        if STAT_BOX_IMAGE is None:
            self.createImage()

        self.rect = pygame.Rect((0, 0), STAT_BOX_SIZE)

        self.update([0,0,0,0,0,0])

    def createImage(self):
        global STAT_BOX_IMAGE
        global STAT_BOX_SIZE

        statText = ["STR", "MAG", "SKI", "VIT", "WIL", "SPD"]
        elements = []
        tempRect = pygame.Rect( (0, 0), STAT_BOX_ELEMENT_SIZE )
        tempFont = pygame.font.Font(STAT_BOX_FONT, STAT_BOX_FONT_SIZE)
        for x in range(6):
            textrect1 = textrect.render_textrect(statText[x], tempFont, tempRect,
                                                 BOX_FONT_COLOR, (0, 0, 0), 0, True)
            elements.append(textrect1)

        sizeX = (STAT_BOX_ELEMENT_SIZE[0] * 2) + (STAT_BOX_BORDER_SIZE * 2) + (STAT_BOX_PADDING * 3)
        sizeY = (STAT_BOX_ELEMENT_SIZE[1] * 3) + (STAT_BOX_BORDER_SIZE * 2) + (STAT_BOX_PADDING * 2)
        STAT_BOX_SIZE = (sizeX, sizeY)
        tempRect = pygame.Rect((0, 0), (sizeX, sizeY))
        tempBox = box.Box(tempRect, STAT_BOX_PATTERN, STAT_BOX_PATTERN_SIZE,
                           STAT_BOX_BORDER, STAT_BOX_BORDER_SIZE)
        for col in range(2):
            for row in range(3):
                x, tempX, tempY = self.getXXY(col, row)
                tempBox.mainPane.blit(elements[x], (tempX, tempY))

        STAT_BOX_IMAGE = tempBox.mainPane

    def update(self, stats):
        elements = []
        tempRect = pygame.Rect( (0, 0), STAT_BOX_ELEMENT_SIZE )
        tempFont = pygame.font.Font(STAT_BOX_FONT, STAT_BOX_FONT_SIZE)
        for x in range(6):
            textrect1 = textrect.render_textrect(str(stats[x]), tempFont, tempRect,
                                                 BOX_FONT_COLOR, (0, 0, 0), 2, True)
            elements.append(textrect1)

        self.numberPane = pygame.Surface((self.rect.width, self.rect.height))
        self.numberPane.set_colorkey(BLACK)
        self.numberPane.fill(BLACK)
        for col in range(2):
            for row in range(3):
                x, tempX, tempY = self.getXXY(col, row)
                self.numberPane.blit(elements[x], (tempX, tempY))

    def getXXY(self, col, row):
        x = row + (3 * col)
        tempX = STAT_BOX_BORDER_SIZE + (STAT_BOX_PADDING * (col + 1)) + (STAT_BOX_ELEMENT_SIZE[0] * col)
        tempY = STAT_BOX_BORDER_SIZE + STAT_BOX_PADDING + (STAT_BOX_ELEMENT_SIZE[1] * row)
        return x, tempX, tempY

        
    def updateBlank(self):
        self.update(["", "", "", "", "", ""])

    def draw(self, screen):
        mainPane = pygame.Surface( (self.rect.width, self.rect.height) )
        mainPane.blit(STAT_BOX_IMAGE, (0, 0))
        mainPane.blit(self.numberPane, (0, 0))
        screen.blit(mainPane, self.rect.topleft)

    def center(self, baseRect, doHoriz, doVert):
        if doHoriz:
            self.rect.left = (baseRect.width / 2) - (self.rect.width / 2)
        if doVert:
            self.rect.top = (baseRect.height / 2) - (self.rect.height / 2)

