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

import background
import textrect

from constants import *

class Box(object):
    def __init__(self, inRect, inBGImage, inBGSize, inBorderImage, inBorderSize, inText=None, inFont=None, inFontSize=None):

        self.rect = inRect
        self.mainPane = pygame.Surface( (self.rect.width, self.rect.height) )

        self.background = background.Background(pygame.Rect((0,0), (self.rect.width, self.rect.height)), inBGImage, inBGSize)
        self.background.draw(self.mainPane)
        self.drawBorder(inBorderImage, inBorderSize)
        if not(inText is None) and not(inFont is None) and not(inFontSize is None):
            self.drawText(inText, inFont, inFontSize)

    def drawBorder(self, inBorderImage, inBorderSize):
        border1 = pygame.image.load(os.path.join(GRAPHICS_PATH, inBorderImage)).convert_alpha()
        border2 = pygame.transform.rotate(border1, 90)
        border3 = pygame.transform.rotate(border1, 180)
        border4 = pygame.transform.rotate(border1, 270)

        #Create Border Sides
        sizeX = self.rect.width
        sizeY = self.rect.height
        for y in range (sizeY):
            self.mainPane.blit(border2, (0, y))
            tempX = sizeX - inBorderSize
            self.mainPane.blit(border4, (tempX, y))
        for x in range(sizeX):
            self.mainPane.blit(border1, (x, 0))
            tempY = sizeY - inBorderSize
            self.mainPane.blit(border3, (x, tempY))

    def drawText(self, inText, inFont, inFontSize):
        tempFont = pygame.font.Font(inFont, inFontSize)
        tempRect = pygame.Rect( (0, 0), (self.rect.width, (inFontSize+4)) )
        tempRect.top = (self.rect.height / 2) - (tempRect.height / 2)
        textrect1 = textrect.render_textrect(inText, tempFont, tempRect, BOX_FONT_COLOR, (0, 0, 0), 1, True)
        self.mainPane.blit(textrect1, tempRect.topleft)
        

    def draw(self, screen):
        screen.blit(self.mainPane, self.rect.topleft)

    def update(self):
        pass

    def center(self, baseRect, doHoriz, doVert):
        if doHoriz:
            self.rect.left = (baseRect.width / 2) - (self.rect.width / 2)
        if doVert:
            self.rect.top = (baseRect.height / 2) - (self.rect.height / 2)
