# Copyright 2009 Christopher Czyzewski, Daniel Tashjian
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

import textrect

from constants import *

TABS = None
ICONS = None

class Card(object):
    def __init__(self, ability):

        global TABS
        global ICONS
        if TABS is None:
            TABS = []
            ICONS = []
            for x in range(0, 4):
                TABS.append(pygame.image.load(os.path.join(GRAPHICS_PATH,CARD_TAB_FILE + str(x) + CARD_TAB_FILE_EXT)).convert_alpha())
            ICONS.append(pygame.image.load(CARD_POW_ICON_FILE).convert_alpha())
            ICONS.append(pygame.image.load(CARD_ACC_ICON_FILE).convert_alpha())
            ICONS.append(pygame.image.load(CARD_SINGLE_ICON_FILE).convert_alpha())
            ICONS.append(pygame.image.load(CARD_LINE_ICON_FILE).convert_alpha())
            ICONS.append(pygame.image.load(CARD_AREA_ICON_FILE).convert_alpha())

        self.image = pygame.Surface(CARD_SIZE)
        self.image.fill(CARD_BORDER_COLOR_DARK)

        tempX = CARD_SIZE[0] - (CARD_BORDER * 2)
        tempY = CARD_SIZE[1] - (CARD_BORDER * 2)
        tempFill = pygame.Surface((tempX, tempY))
        tempFill.fill(CARD_BORDER_COLOR_LIGHT)
        self.image.blit(tempFill, ((CARD_BORDER), (CARD_BORDER)))
        

        tempX = CARD_SIZE[0] - (CARD_BORDER * 4)
        tempY = CARD_SIZE[1] - (CARD_BORDER * 4)

        #Create backgrounds
        BGs = []
        for t in range(4):
            if t == 3:
                alphaR = 255
            elif self.totalCost(ability.manaCost) == 0:
                alphaR = 0
            else:
                alphaR = (float(ability.manaCost[t]) / float(self.totalCost(ability.manaCost))) * 255
            BGs.append(self.createBG(tempX, tempY, t, alphaR))

        
        self.image.blit(BGs[3], (CARD_BORDER, CARD_BORDER))
        for t in range(3):
            self.image.blit(BGs[t], (CARD_BORDER * 2, CARD_BORDER * 2))
        

        self.rect = pygame.Rect((5, 5), CARD_SIZE)

        fontBig = pygame.font.Font(CARD_FONT, CARD_FONT_SIZE_BIG)
        fontSmall = pygame.font.Font(CARD_FONT, CARD_FONT_SIZE_SMALL)

        for t in range(4):
            tempX = (CARD_BORDER * 2) + CARD_OUTTER_PADDING + ((CARD_INNER_PADDING + CARD_TAB_SIZE[0]) * t)
            tempY = (CARD_BORDER * 2)
            self.image.blit(TABS[t], (tempX, tempY))
            tempArea = textrect.render_textrect(str(ability.manaCost[t]), fontBig,
                                            pygame.Rect((0, 0),CARD_TAB_SIZE),
                                            CARD_FONT_COLOR_2, CARD_INDENT_COLOR, 1, True)
            self.image.blit(tempArea, (tempX, tempY))

        tempArea = textrect.render_textrect(ability.name, fontBig,
                                            pygame.Rect((0, 0),CARD_NAME_SIZE),
                                            CARD_FONT_COLOR, CARD_INDENT_COLOR, 0)
        tempX = (CARD_BORDER * 2) + CARD_OUTTER_PADDING
        tempY = (CARD_BORDER * 2) + CARD_OUTTER_PADDING + CARD_TAB_SIZE[1] + CARD_INNER_PADDING
        self.image.blit(tempArea, (tempX, tempY))

        tempArea = textrect.render_textrect(ability.desc, fontBig,
                                            pygame.Rect((0, 0),CARD_DESC_SIZE),
                                            CARD_FONT_COLOR, CARD_INDENT_COLOR, 0)
        tempY += CARD_NAME_SIZE[1] + CARD_INNER_PADDING
        self.image.blit(tempArea, (tempX, tempY))

        tempY += CARD_DESC_SIZE[1] + CARD_INNER_PADDING
        for t in range(2):
            tempX = CARD_OUTTER_PADDING + ((CARD_SIZE[0] / 2) * t)
            if t == 0:
                currStat = ability.damage
                tempX += (CARD_BORDER * 2)
            else:
                currStat = ability.accuracy
            self.image.blit(ICONS[t], (tempX, tempY))

            tempY2 = tempY + (CARD_ICON_SIZE[1] / 2) - (CARD_BLOCK_SIZE[1] / 2)
            tempX += CARD_ICON_SIZE[0] + CARD_INNER_PADDING
            percentString = str(int(currStat * 100)) + "%"
            tempArea = textrect.render_textrect(percentString, fontBig,
                                                pygame.Rect((0, 0),CARD_SMALL_BLOCK_SIZE),
                                                CARD_FONT_COLOR, CARD_INDENT_COLOR, 1, False)
            self.image.blit(tempArea, (tempX, tempY2))

        rangeBoxSizeX = CARD_BLOCK_SIZE[0] + CARD_INNER_PADDING + CARD_ICON_SIZE[0]
        tempX = (CARD_SIZE[0] / 2) - (rangeBoxSizeX / 2)
        tempY += CARD_ICON_SIZE[1] + CARD_INNER_PADDING
        tempY2 = tempY + (CARD_ICON_SIZE[1] / 2) - (CARD_BLOCK_SIZE[1] / 2)
        tempText = str(ability.minRange) + " - " + str(ability.maxRange)
        tempArea = textrect.render_textrect(tempText, fontBig,
                                            pygame.Rect((0, 0),CARD_BLOCK_SIZE),
                                            CARD_FONT_COLOR, CARD_INDENT_COLOR, 1)
        self.image.blit(tempArea, (tempX, tempY2))

        tempX += CARD_BLOCK_SIZE[0] + CARD_INNER_PADDING
        if ability.AOE == 0:
            areaIcon = ICONS[2]
        elif ability.AOE >= 1 and ability.AOE <= 3:
            areaIcon = ICONS[3]
        else:
            areaIcon = ICONS[4]
        
        self.image.blit(areaIcon, (tempX, tempY))

        midPoint = CARD_SIZE[0] / 2
        tempY += CARD_ICON_SIZE[1] + CARD_INNER_PADDING

        tempX = midPoint - int(CARD_SMALL_BLOCK_SIZE[0] + (CARD_SMALLEST_BLOCK_SIZE[0] / 2))
        if ability.statOff == "P":
            tempText = "STR"
            tempColor = (128, 64, 0)
        elif ability.statOff == "M":
            tempText = "MAG"
            tempColor = (64, 128, 128)
        else:
            fatalError()
            
        tempArea = textrect.render_textrect(tempText, fontBig,
                                            pygame.Rect((0, 0),CARD_SMALL_BLOCK_SIZE),
                                            tempColor, CARD_INDENT_COLOR, 1)
        self.image.blit(tempArea, (tempX, tempY))

        tempX += CARD_SMALL_BLOCK_SIZE[0]
        tempArea = textrect.render_textrect("->", fontBig,
                                            pygame.Rect((0, 0),CARD_SMALLEST_BLOCK_SIZE),
                                            CARD_FONT_COLOR, CARD_INDENT_COLOR, 1)
        self.image.blit(tempArea, (tempX, tempY))

        if ability.statDef == "P":
            tempText = "VIT"
            tempColor = (128, 64, 0)
        elif ability.statDef == "M":
            tempText = "WIL"
            tempColor = (64, 128, 128)
        elif ability.statDef == "L":
            tempText = "LOW"
            tempColor = CARD_FONT_COLOR
        else:
            fatalError()

        tempX += CARD_SMALLEST_BLOCK_SIZE[0]
        tempArea = textrect.render_textrect(tempText, fontBig,
                                            pygame.Rect((0, 0),CARD_SMALL_BLOCK_SIZE),
                                            tempColor, CARD_INDENT_COLOR, 1)
        self.image.blit(tempArea, (tempX, tempY))
            
        
        

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def newIndent(self, inSize):
        newArea = pygame.Surface(inSize)
        newArea.fill(CARD_INDENT_COLOR)
        return newArea

    def setLoc(self, inX, inY):
        self.rect.left = inX
        self.rect.top = inY

    def createBG(self, sizeX, sizeY, t, alphaR):
        tempFill = pygame.Surface((sizeX, sizeY))
        tempFill.fill(CARD_BG_COLORS[t])
        tempFill.set_alpha(alphaR)
        return tempFill

    def totalCost(self, manaCost):
        total = 0
        for t in range(3):
            total += manaCost[t]
        return total
