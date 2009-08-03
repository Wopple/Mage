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
import soundSystem

from constants import *

class PieceBox(object):
    def __init__(self, characters, typePre):
        self.characters = characters

        if typePre:
            perCol = PLANNING_BOX_CHARS_PER_COL
        else:
            perCol = MAX_CHAR_ACTIVE
        numOfRows = int(math.ceil(float(self.numOfCharacters()) / float(perCol)))
        numOfColumns = perCol
        sizeX = (PLANNING_BOX_BORDER_SIZE * 2) + (PIECE_SIZE[0] * numOfColumns) + (PLANNING_BOX_PADDING * (numOfColumns + 1))
        sizeY = (PLANNING_BOX_BORDER_SIZE * 2) + (PIECE_SIZE[1] * numOfRows) + (PLANNING_BOX_PADDING * (numOfRows + 2)) + PLANNING_BOX_DONE_SIZE[1]
        sizeXAlt = (PLANNING_BOX_BORDER_SIZE * 2) + (PLANNING_BOX_PADDING * 2) + PLANNING_BOX_DONE_SIZE[0]
        if sizeX < sizeXAlt:
            sizeX = sizeXAlt
        tempRect = pygame.Rect( (0, 0), (sizeX, sizeY) )
        self.box = box.Box(tempRect, PLANNING_BOX_PATTERN, PLANNING_BOX_PATTERN_SIZE, PLANNING_BOX_BORDER, PLANNING_BOX_BORDER_SIZE)

        self.numOfRows = numOfRows
        self.numOfColumns = numOfColumns

        self.createDoneButton()

        self.lightTicker = incint.IncInt(0, 0, PLANNING_BOX_LIGHT_RANGE)
        self.lightMasterSwitch = True

        #Create filled square areas for each character
        for x in range(numOfColumns):
            for y in range(numOfRows):
                tempPane = pygame.Surface (PIECE_SIZE)
                tempPane.fill(PLANNING_BOX_PIECE_FILL)
                tempPos = self.findCursorPos((x, y), False)
                self.box.mainPane.blit(tempPane, tempPos)

        self.charSelections = []
        for x in range(len(characters)):
            self.charSelections.append(False)

        self.lightBox = pygame.Surface (PIECE_SIZE)
        self.lightBox.fill(PLANNING_BOX_PIECE_FILL)
            
                
    def update(self, idleTick, activeTick, activeChar):
        for character in self.characters:
            character.piece.update(SPRITE_SHEET_IDLE, idleTick)

        if activeChar < self.numOfCharacters():
            self.characters[activeChar].piece.update(SPRITE_SHEET_ACTIVE, activeTick)

        if self.lightMasterSwitch:
            self.lightTicker.increment()
        else:
            self.lightTicker.decrement()
            
        if self.lightTicker.isBound():
            self.lightMasterSwitch = not(self.lightMasterSwitch)

        if self.numActiveChars() == 0:
            self.lightMasterSwitch = True
            self.lightTicker.value = self.lightTicker.minimum

        tempRed = self.checkMaxByte(PLANNING_BOX_PIECE_FILL[0] + (self.lightTicker.value * 3))
        tempGreen = self.checkMaxByte(PLANNING_BOX_PIECE_FILL[1] + (self.lightTicker.value * 3))
        tempBlue = self.checkMaxByte(PLANNING_BOX_PIECE_FILL[2] + (self.lightTicker.value * 3))

        self.lightBox.fill((tempRed, tempGreen, tempBlue))

        

    def draw(self, screen):
        self.box.draw(screen)
        self.drawLights(screen)
        self.drawPieces(screen)

    def numOfCharacters(self):
        return len(self.characters)

    def findCursorPos(self, pos, isAbsolute):
        tempX = PLANNING_BOX_BORDER_SIZE + PLANNING_BOX_PADDING + ((PLANNING_BOX_PADDING + PIECE_SIZE[0]) * pos[0])
        tempY = PLANNING_BOX_BORDER_SIZE + PLANNING_BOX_PADDING + ((PLANNING_BOX_PADDING + PIECE_SIZE[1]) * pos[1])

        if isAbsolute:
            tempX += self.box.rect.left
            tempY += self.box.rect.top
        return (tempX, tempY)

    def createDoneButton(self):
        tempPos = self.donePos(False)
        
        sizeX = self.box.rect.width
        sizeY = (PLANNING_BOX_PADDING * 2) + PLANNING_BOX_DONE_SIZE[1]
        
        centerRect = pygame.Rect( tempPos, (sizeX, sizeY) )

        doneRect = pygame.Rect( (0, 0), PLANNING_BOX_DONE_SIZE )
        tempFont = pygame.font.Font(PLANNING_BOX_FONT, PLANNING_BOX_FONT_SIZE)
        textrect1 = textrect.render_textrect("Done", tempFont, doneRect, BOX_FONT_COLOR, (0, 0, 0), 1, True)

        doneRect.left = (centerRect.width / 2) - (doneRect.width / 2) + centerRect.left
        doneRect.top = (centerRect.height / 2) - (doneRect.height / 2) + centerRect.top

        self.box.mainPane.blit(textrect1, doneRect.topleft)

        self.doneRect = doneRect

    def donePos(self, isAbsolute):
        tempX = 0
        tempY = self.box.rect.height - PLANNING_BOX_BORDER_SIZE - (PLANNING_BOX_PADDING * 2) - PLANNING_BOX_DONE_SIZE[1]

        if isAbsolute:
            tempX = self.box.rect.left + self.doneRect.left
            tempY = self.box.rect.top + self.doneRect.top
        return (tempX, tempY)

    def drawPieces(self, screen):
        for character in self.characters:
            character.piece.draw(screen)

    def placePieces(self):
        for currChar in range(len(self.characters)):
            tempPos = self.convertLinearToGrid(currChar)
            self.characters[currChar].piece.location = self.findCursorPos(tempPos, True)

    def tryLight(self, currChar):
        if currChar < len(self.characters):
            if not((self.charSelections[currChar] == False) and (self.numActiveChars() >= MAX_CHAR_ACTIVE)):
                self.lightCharacter(currChar)

    def lightCharacter(self, currChar):
        self.charSelections[currChar] = not(self.charSelections[currChar])
        if self.charSelections[currChar]:
            soundSystem.playSound(1)
        else:
            soundSystem.playSound(2)

    def convertLinearToGrid(self, currChar):
        x = currChar % self.numOfColumns
        y = int(currChar / self.numOfColumns)
        return (x, y)

    def drawLights(self, screen):
        for currLight in range(len(self.charSelections)):
            if self.charSelections[currLight]:
                screen.blit(self.lightBox, self.findCursorPos(self.convertLinearToGrid(currLight), True))

    def numActiveChars(self):
        tempCount = 0
        for sel in self.charSelections:
            if sel:
                tempCount += 1
        return tempCount

    def checkMaxByte(self, inVal):
        if inVal > 255:
            return 255
        else:
            return inVal
