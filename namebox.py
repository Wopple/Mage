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

class NameBox(object):
    def __init__(self):

        sizeX = NAME_BOX_ELEMENT_SIZE[0] + (STAT_BOX_BORDER_SIZE * 2) + (NAME_BOX_PADDING * 2)
        sizeY = (NAME_BOX_ELEMENT_SIZE[1] * 5) + (STAT_BOX_BORDER_SIZE * 2) + (NAME_BOX_PADDING * 2)
        tempRect = pygame.Rect((0, 0), (sizeX, sizeY))
        self.box = box.Box(tempRect, STAT_BOX_PATTERN, STAT_BOX_PATTERN_SIZE,
                           STAT_BOX_BORDER, STAT_BOX_BORDER_SIZE)

        self.rect = pygame.Rect((0, 0), (self.box.rect.width, self.box.rect.height))
        self.update(["No Name", "No Class", 0, 0, 0, 0, "No Status"])
        self.blank = False


    def update(self, inVar):
        inName = inVar[0]
        inClass = inVar[1]
        inLevel = inVar[2]
        inHP = inVar[3]
        inHPMAX = inVar[4]
        inMov = inVar[5]
        inStatus = inVar[6]

        self.numberPane = pygame.Surface((self.rect.width, self.rect.height))
        self.numberPane.set_colorkey(BLACK)
        self.numberPane.fill(BLACK)
        
        text = [inName, "Lv." + str(inLevel) + " " + inClass,
                    str(inHP) + "/" + str(inHPMAX) + " HP", "Movement " + str(inMov),
                    inStatus]
        tempRect = pygame.Rect( (0, 0), NAME_BOX_ELEMENT_SIZE )
        tempFont = pygame.font.Font(STAT_BOX_FONT, NAME_BOX_FONT_SIZE)
        for x in range(len(text)):
            textrect1 = textrect.render_textrect(text[x], tempFont, tempRect,
                                                 BOX_FONT_COLOR, (0, 0, 0), 1, True)
            tempX = STAT_BOX_BORDER_SIZE + NAME_BOX_PADDING
            tempY = STAT_BOX_BORDER_SIZE + NAME_BOX_PADDING + (NAME_BOX_ELEMENT_SIZE[1] * x)
            self.numberPane.blit(textrect1, (tempX, tempY))

    def draw(self, screen):
        mainPane = pygame.Surface((self.box.rect.width, self.box.rect.height))
        self.box.draw(mainPane)
        if not self.blank:
            mainPane.blit(self.numberPane, (0, 0))
        screen.blit(mainPane, self.rect.topleft)

    def center(self, baseRect, doHoriz, doVert):
        if doHoriz:
            self.rect.left = (baseRect.width / 2) - (self.rect.width / 2)
        if doVert:
            self.rect.top = (baseRect.height / 2) - (self.rect.height / 2)




            
            
            
