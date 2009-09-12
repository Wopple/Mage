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

import portrait
import meter
import textrect

from constants import *

class CornerInfo(object):
    def __init__(self):

        sizeX = CORNER_INFO_PORTRAIT_SIZE + (CORNER_INFO_PADDING * 2)
        sizeY = CORNER_INFO_PORTRAIT_SIZE + (CORNER_INFO_PADDING * 3) + (CORNER_INFO_BAR_SIZE[1] * 2)
        sizeX2 = sizeX
        sizeY2 = sizeY + (CORNER_INFO_PADDING * 4) + (CORNER_INFO_BAR_SIZE[1] * 6) + CORNER_INFO_DIVIDER_SIZE[1]
        self.sizes = [(sizeX, sizeY), (sizeX2, sizeY2)]
        self.rect = pygame.Rect((0, 0), self.sizes[0])
        self.portrait = None
        self.hp = 0
        self.hpMax = 0
        self.mana = 0
        self.manaMax = 0
        self.isMage = False
        self.font = font = pygame.font.Font(CORNER_INFO_FONT, CORNER_INFO_FONT_SIZE)

    def update(self, side, in_portrait, in_hp, in_hpMax, in_mana, in_manaMax, inMage):
        if not in_portrait is None:
            self.portrait = portrait.Portrait(in_portrait, (CORNER_INFO_PORTRAIT_SIZE, CORNER_INFO_PORTRAIT_SIZE), (0,0))
        else:
            self.portrait = None

        self.hp = in_hp
        self.hpMax = in_hpMax
        self.mana = in_mana
        self.manaMax = in_manaMax
        self.isMage = inMage

        if self.isMage:
            tempVal = 1
        else:
            tempVal = 0
        self.rect.width = self.sizes[tempVal][0]
        self.rect.height = self.sizes[tempVal][1]
        
        #left = True, right = False
        if side:
            self.rect.left = 0
        else:
            self.rect.right = SCREEN_SIZE[0]
        self.rect.top = 0

    def draw(self, screen):
        if not self.portrait is None:
            mainPane = pygame.Surface((self.rect.width, self.rect.height))
            mainPane.fill(CORNER_INFO_COLOR)
            mainPane.set_alpha(CORNER_INFO_ALPHA)
            self.portrait.rect.left = CORNER_INFO_PADDING
            self.portrait.rect.top = CORNER_INFO_PADDING
            self.portrait.draw(mainPane)

            tempX = CORNER_INFO_PADDING
            tempY = (CORNER_INFO_PADDING * 2) + CORNER_INFO_PORTRAIT_SIZE
            mainPane.blit(self.createBar(0), (tempX, tempY))
            tempY += CORNER_INFO_BAR_SIZE[1]
            mainPane.blit(self.createText(0), (tempX, tempY))
            if self.isMage:
                tempY += CORNER_INFO_PADDING + CORNER_INFO_BAR_SIZE[1]
                mainPane.blit(self.createDivider(), (tempX, tempY))
                tempY += CORNER_INFO_PADDING + CORNER_INFO_DIVIDER_SIZE[1]
                for i in range(1, 4):
                    mainPane.blit(self.createBar(i), (tempX, tempY))
                    tempY += CORNER_INFO_BAR_SIZE[1]
                    mainPane.blit(self.createText(i), (tempX, tempY))
                    tempY += CORNER_INFO_PADDING + CORNER_INFO_BAR_SIZE[1]
            
            screen.blit(mainPane, self.rect.topleft)

    def createBar(self, inVal):
        result = pygame.Surface(CORNER_INFO_BAR_SIZE)

        if inVal == 0:
            stat = self.hp
            statMax = self.hpMax
        else:
            stat = self.mana[inVal-1]
            statMax = self.manaMax[inVal-1]

        fullColor = CORNER_INFO_BAR_COLORS[inVal]
        emptyColor = []
        for c in fullColor:
            tempVal = c - CORNER_INFO_DARKER
            if tempVal < 0:
                tempVal = 0
            emptyColor.append(tempVal)

        amountToFill = int((float(stat) / float(statMax)) * CORNER_INFO_BAR_SIZE[0])

        result.fill(emptyColor)
        result.fill(fullColor, (0, 0, amountToFill, CORNER_INFO_BAR_SIZE[1]))

        return result

    def createText(self, inVal):
        if inVal == 0:
            stat = self.hp
            statMax = self.hpMax
        else:
            stat = self.mana[inVal-1]
            statMax = self.manaMax[inVal-1]

        tempText = str(stat) + "/" + str(statMax)
        tempRect = pygame.Rect((0, 0), CORNER_INFO_BAR_SIZE)
        tempColor = CORNER_INFO_BAR_COLORS[inVal]
        return textrect.render_textrect(tempText, self.font, tempRect,
                                        tempColor, BLACK, 2, True)
        

    def createDivider(self):
        result = pygame.Surface(CORNER_INFO_DIVIDER_SIZE)
        result.fill(CORNER_INFO_DIVIDER_COLOR)
        return result
