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
import random

import model

import background
import scrollingBackground
import incint
import soundSystem
import box
import textrect
import cursor
import meter

from constants import *

class Model(model.Model):
    def __init__(self, inBG, inCharMana, inCharManaMax, inManaCost):
        super(Model, self).__init__()

        self.goBack = False
        self.goForward = False

        self.origMana = []
        self.mana = []
        for i in range(3):
            self.origMana.append(inCharMana[i])
            self.mana.append(inCharMana[i])
        self.colorless = inManaCost[3]

        for i in range(3):
            self.mana[i] -= inManaCost[i]

        temp = self.getTextRect(0)
        self.cursor = cursor.Cursor(temp)

        self.background = pygame.Surface(SCREEN_SIZE)
        self.background.blit(inBG, (0, 0))
        tempVeil = pygame.Surface(SCREEN_SIZE)
        tempVeil.fill(BLACK)
        tempVeil.set_alpha(CARD_VIEWER_VEIL)
        self.background.blit(tempVeil, (0, 0))

        self.cursorPos = incint.IncInt(0, 0, 2)

        self.buildWindow()

        self.colorlessRect = self.getColorlessRect()
        self.makeColorlessText()

        self.bars = []
        for i in range(3):
            colorFull = ENERGY_SPENDER_BAR_COLORS[i]
            colorEmpty = []
            for c in colorFull:
                tempVal = c - ENERGY_SPENDER_DARKER
                if tempVal < 0:
                    tempVal = 0
                colorEmpty.append(tempVal)
            self.bars.append(meter.Meter(self.getMeterLoc(i), ENERGY_SPENDER_BAR_SIZE[0], ENERGY_SPENDER_BAR_SIZE[1],
                                         inCharManaMax[i], colorFull, colorEmpty))

        self.manaNums = []
        self.manaNumRects = []
        for i in range(3):
            temp = self.getManaNumRect(i)
            self.manaNumRects.append(temp)
            self.manaNums.append(self.makeManaNum(temp, i))

    def incMenu(self):
        self.cursorPos.inc()

    def decMenu(self):
        self.cursorPos.dec()

    def update(self):
        self.updateCursor()
        for i in range(3):
            self.bars[i].update(self.mana[i])

    def advance(self):
        return self.goForward

    def back(self):
        return self.goBack

    def cancel(self):
        pass

    def confirm(self):
        if self.mana[self.cursorPos.value] > 0:
            self.mana[self.cursorPos.value] -= 1
            self.colorless -= 1

        self.makeColorlessText()

        self.manaNums = []
        for i in range(3):
            self.manaNums.append(self.makeManaNum(self.manaNumRects[i], i))

        if self.colorless == 0:
            self.goForward = True

    def getColorlessRect(self):
        size = ENERGY_SPENDER_ELEMENT_SIZE
        tempX = (ENERGY_SPENDER_SIZE[0] / 2) - (size[0] / 2)
        tempY = ENERGY_SPENDER_BORDER_SIZE + ENERGY_SPENDER_PADDING
        tempX += self.box.rect.left
        tempY += self.box.rect.top
        return pygame.Rect( (tempX, tempY), size )

    def getManaNumRect(self, inNum):
        inNum += 1
        size = ENERGY_SPENDER_ELEMENT_SIZE
        tempX = ENERGY_SPENDER_BORDER_SIZE + (ENERGY_SPENDER_PADDING * 2) + ENERGY_SPENDER_ELEMENT_SIZE[0]
        tempY = ENERGY_SPENDER_PADDING + ((ENERGY_SPENDER_PADDING + ENERGY_SPENDER_ELEMENT_SIZE[1]) * inNum) + ENERGY_SPENDER_BORDER_SIZE
        tempX += self.box.rect.left
        tempY += self.box.rect.top
        return pygame.Rect( (tempX, tempY), size )

    def makeColorlessText(self):
        tempFont = pygame.font.Font(ENERGY_SPENDER_FONT, ENERGY_SPENDER_FONT_SIZE)
        temp = textrect.render_textrect(str(self.colorless), tempFont,
                                            self.colorlessRect, ENERGY_SPENDER_COLORLESS, (0, 0, 0), 1, True)
        self.colorlessText = temp

    def makeManaNum(self, inRect, inNum):
        tempFont = pygame.font.Font(ENERGY_SPENDER_FONT, ENERGY_SPENDER_FONT_SIZE)
        temp = textrect.render_textrect(str(self.mana[inNum]), tempFont,
                                            inRect, ENERGY_SPENDER_BAR_COLORS[inNum], (0, 0, 0), 1, True)
        return temp


    def buildWindow(self):
        self.box = box.Box(pygame.Rect((0, 0), (ENERGY_SPENDER_SIZE)),
                           ENERGY_SPENDER_BG_IMAGE, ENERGY_SPENDER_BG_SIZE,
                           ENERGY_SPENDER_BORDER_IMAGE, ENERGY_SPENDER_BORDER_SIZE)
        self.box.center(ENTIRE_SCREEN, True, True)

        tempFont = pygame.font.Font(ENERGY_SPENDER_FONT, ENERGY_SPENDER_FONT_SIZE)
        for i in range(3):
            loc = self.getTextRect(i)
            temp = textrect.render_textrect(str(MANA_NAMES[i]), tempFont,
                                            pygame.Rect((0, 0),ENERGY_SPENDER_ELEMENT_SIZE),
                                            ENERGY_SPENDER_FONT_COLOR, (0, 0, 0), 1, True)
            self.box.mainPane.blit(temp, loc)

    def getTextRect(self, inNum):
        if (inNum >= 0) or (inNum <= 2):
            inNum += 1
            tempX = ENERGY_SPENDER_PADDING + ENERGY_SPENDER_BORDER_SIZE
            tempY = ENERGY_SPENDER_PADDING + ((ENERGY_SPENDER_PADDING + ENERGY_SPENDER_ELEMENT_SIZE[1]) * inNum) + ENERGY_SPENDER_BORDER_SIZE
            return pygame.Rect( (tempX, tempY), ENERGY_SPENDER_ELEMENT_SIZE )

    def getMeterLoc(self, inNum):
        inNum += 1
        tempX = (ENERGY_SPENDER_PADDING * 3) + (ENERGY_SPENDER_ELEMENT_SIZE[0] * 2) + ENERGY_SPENDER_BORDER_SIZE
        tempY = ENERGY_SPENDER_PADDING + ((ENERGY_SPENDER_PADDING + ENERGY_SPENDER_ELEMENT_SIZE[1]) * inNum) + ENERGY_SPENDER_BORDER_SIZE
        tempX += self.box.rect.left
        tempY += self.box.rect.top
        return (tempX, tempY)

    def updateCursor(self):
        temp = self.getTextRect(self.cursorPos.value)
        temp.left += self.box.rect.left
        temp.top += self.box.rect.top
        self.cursor.update(temp.topleft, (temp.width, temp.height))

    def getTotalSpending(self):
        total = []
        for i in range(3):
            total.append(self.origMana[i] - self.mana[i])
        return total
