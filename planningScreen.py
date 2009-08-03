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
import pieceBox
import background
import scrollingBackground
import cursor
import incint
import pieceTicker
import minimenu
import meter
import textrect
import statbox
import namebox
import manaBox
import portraitbox
import soundSystem

from constants import *

class PlanningScreen(object):
    def __init__(self, typePre, characters, xp=1):

        self.typePre = typePre
        self.xp = xp
        if self.xp < 1:
            self.xp = 1

        self.selectedXP = False

        #Background
        tempRect = pygame.Rect( (0, 0), SCREEN_SIZE)
        self.background = scrollingBackground.ScrollingBackground(tempRect, PLANNING_BG_IMAGE, PLANNING_BG_SIZE,
                                                                  PLANNING_BG_DIREC, PLANNING_BG_SPEED)

        #Top Box
        tempRect = pygame.Rect ((0, 0), PLANNING_BOX_SIZE1)
        if typePre:
            tempText = "Select Units for Chapter"
        else:
            tempText = "Distribute Experience"
        self.topBox = box.Box(tempRect, PLANNING_BOX_PATTERN, PLANNING_BOX_PATTERN_SIZE, PLANNING_BOX_BORDER, PLANNING_BOX_BORDER_SIZE,
                              tempText, PLANNING_BOX_FONT, PLANNING_BOX_FONT_SIZE)

        #Piece Box
        self.pieceBox = pieceBox.PieceBox(characters, typePre)
        self.pieceBox.box.center(ENTIRE_SCREEN, True, True)

        #Name Box
        self.namebox = namebox.NameBox()
        self.namebox.center(ENTIRE_SCREEN, False, True)
        self.namebox.rect.right = SCREEN_SIZE[0] - 5
        self.namebox.rect.top -= (self.namebox.rect.height / 2)

        #Stat Box
        self.statbox = statbox.StatBox()
        self.statbox.rect.right = SCREEN_SIZE[0] - 5
        self.statbox.rect.top = self.namebox.rect.bottom + 5

        #Cursor
        tempRect = pygame.Rect( (0, 0), (PIECE_SIZE) )
        self.cursor = cursor.Cursor(tempRect)
        self.cursorPos = [ incint.IncInt(1, 1, self.pieceBox.numOfColumns), incint.IncInt(1, 1, self.pieceBox.numOfRows + 1) ]

        #Count Box
        self.makeCountBox()

        #XP Box
        self.makeXPBox()
        self.updateXP()

        #Rearrange Top Box
        centerRect = pygame.Rect( (0, 0), (SCREEN_SIZE[0], (self.pieceBox.box.rect.top)) )
        self.topBox.center(centerRect, True, True)

        #Portrait Box
        self.portraitBox = portraitbox.PortraitBox()
        centerRect = pygame.Rect( (0,0), (self.pieceBox.box.rect.left, SCREEN_SIZE[1]) )
        self.portraitBox.box.center(centerRect, True, False)
        self.portraitBox.box.rect.top = self.topBox.rect.bottom + 5

        #Mana Box
        self.manaBox = manaBox.ManaBox()
        centerRect = pygame.Rect( (0,0), (self.pieceBox.box.rect.left, SCREEN_SIZE[1]) )
        self.manaBox.center(centerRect, True, False)
        self.manaBox.rect.top = self.portraitBox.box.rect.bottom + 5
        

        #Pieces
        self.pieceBox.placePieces()

        #Variables
        
        self.idleTicker = pieceTicker.PieceTicker(IDLE_ANIM_SPEED)
        self.activeTicker = pieceTicker.PieceTicker(ACTIVE_ANIM_SPEED)
        self.lastCount = self.numActiveChars()
        self.changeC = False
        self.menuOpen = False

        self.cursorMoveSuccess(True, False)
        

    def update(self):
        self.background.update()
        self.idleTicker.update()
        self.activeTicker.update()
        self.topBox.update()
        self.pieceBox.update(self.idleTicker.value(), self.activeTicker.value(), self.currActiveCharacter())
        self.cursor.update(self.findCursorPos(), self.findCursorSize())
        if self.lastCount != self.numActiveChars():
            self.lastCount = self.numActiveChars()
            self.makeCountBox()

    def updateXP(self):
        tempFont = pygame.font.Font(PLANNING_BOX_FONT, PLANNING_BOX_FONT_SIZE)
        
        self.surfaceReserve = textrect.render_textrect(str(self.xp), tempFont, self.rectReserve, BOX_FONT_COLOR, (0, 0, 0), 2, True)
        
        if self.validCharacter():
            tempText = str(self.currNextLevel())
        else:
            tempText = ""
        self.surfaceNext = textrect.render_textrect(tempText, tempFont, self.rectNext, BOX_FONT_COLOR, (0, 0, 0), 2, True)

    def drawXP(self, screen):
        screen.blit(self.surfaceReserve, (self.xpBox.rect.left + self.rectReserve.left, self.xpBox.rect.top + self.rectReserve.top))
        screen.blit(self.surfaceNext, (self.xpBox.rect.left + self.rectNext.left, self.xpBox.rect.top + self.rectNext.top))

    def draw(self, screen):
        self.background.draw(screen)
        self.topBox.draw(screen)
        self.pieceBox.draw(screen)
        self.statbox.draw(screen)
        self.namebox.draw(screen)
        self.portraitBox.draw(screen)
        self.manaBox.draw(screen)
        if self.typePre:
            self.countBox.draw(screen)
        else:
            self.xpBox.draw(screen)
            self.drawXP(screen)
            self.xpMeter.draw(screen)
        self.cursor.draw(screen)

    def findCursorPos(self):
        if self.overDoneButton():
            return self.pieceBox.donePos(True)
        elif self.selectedXP:
            return ((self.xpTextRect.left + self.xpBox.rect.left), (self.xpTextRect.top + self.xpBox.rect.top))
        else:
            return(  self.pieceBox.findCursorPos( ((self.cursorPos[0].value - 1), (self.cursorPos[1].value - 1)), True )  )

    def findCursorSize(self):
        if self.overDoneButton():
            return PLANNING_BOX_DONE_SIZE
        elif self.selectedXP:
            return (self.xpTextRect.width, self.xpTextRect.height)
        else:
            return PIECE_SIZE


    def cursorMoveUp(self):
        if not(self.selectedXP):
            self.cursorPos[1].decrement()
            self.cursorMoveSuccess()

    def cursorMoveDown(self):
        if not(self.selectedXP):
            self.cursorPos[1].increment()
            self.cursorMoveSuccess()

    def cursorMoveLeft(self):
        if not(self.overDoneButton()) and not(self.selectedXP):
            self.cursorPos[0].decrement()
            self.cursorMoveSuccess()

    def cursorMoveRight(self):
        if not(self.overDoneButton()) and not(self.selectedXP):
            self.cursorPos[0].increment()
            self.cursorMoveSuccess()

    def cursorMoveSuccess(self, resetTicker=True, playSound=True):
        self.activeTicker.reset()
        self.updateXP()
        if self.validCharacter():
            tempChar = self.pieceBox.characters[self.currActiveCharacter()]
            self.statbox.update(tempChar.getStats())
            self.manaBox.update(tempChar.getMana())
            self.namebox.update(tempChar.getInfo())
            self.namebox.blank = False
            self.portraitBox.update(tempChar.portrait)
        else:
            self.statbox.updateBlank()
            self.manaBox.updateBlank()
            self.namebox.blank = True
            self.portraitBox.update(None)
        if playSound:
            self.cursor.playSound()

    def overDoneButton(self):
        if self.cursorPos[1].value == self.cursorPos[1].maximum:
            return True
        else:
            return False

    def currActiveCharacter(self):
        return ( ((self.cursorPos[1].value - 1) * self.pieceBox.numOfColumns) + (self.cursorPos[0].value - 1) )

    def makeCountBox(self):
        tempRect = pygame.Rect ((0, 0), PLANNING_BOX_SIZE2)
        tempText = str(self.numActiveChars()) + " / " + str(MAX_CHAR_ACTIVE)
        self.countBox = box.Box(tempRect, PLANNING_BOX_PATTERN, PLANNING_BOX_PATTERN_SIZE, PLANNING_BOX_BORDER, PLANNING_BOX_BORDER_SIZE,
                                tempText, PLANNING_BOX_FONT, PLANNING_BOX_FONT_SIZE)
        self.countBox.rect.top = self.pieceBox.box.rect.bottom + 5
        self.countBox.center(ENTIRE_SCREEN, True, False)

    def makeXPBox(self):
        self.xpMeter = meter.Meter((0, 0), PLANNING_XP_BAR_SIZE[0], PLANNING_XP_BAR_SIZE[1], self.xp,
                                   PLANNING_XP_BAR_COLOR_FULL, PLANNING_XP_BAR_COLOR_EMPTY)
        tempHeight = PLANNING_XP_BAR_SIZE[1]
        if tempHeight < PLANNING_XP_TEXT_SIZE[1]:
            tempHeight = PLANNING_XP_TEXT_SIZE[1]
        tempRect = pygame.Rect( (0, 0),
                                (PLANNING_XP_BAR_SIZE[0] + (PLANNING_XP_BAR_PADDING * 3) + PLANNING_XP_TEXT_SIZE[0],
                                 tempHeight + (PLANNING_XP_BAR_PADDING * 4) + (PLANNING_XP_TEXT2_SIZE[1] * 2)) )
        self.xpBox = box.Box(tempRect, PLANNING_BOX_PATTERN, PLANNING_BOX_PATTERN_SIZE, PLANNING_BOX_BORDER, PLANNING_BOX_BORDER_SIZE)

        tempRect = pygame.Rect( (PLANNING_XP_BAR_PADDING, PLANNING_XP_BAR_PADDING), (PLANNING_XP_TEXT_SIZE[0], PLANNING_XP_TEXT_SIZE[1]) )
        tempFont = pygame.font.Font(PLANNING_BOX_FONT, PLANNING_BOX_FONT_SIZE)
        textSurface = textrect.render_textrect("EXP", tempFont, tempRect, BOX_FONT_COLOR, (0, 0, 0), 1, True)
        self.xpBox.mainPane.blit(textSurface, tempRect.topleft)
        self.xpTextRect = tempRect

        tempRect = pygame.Rect( (PLANNING_XP_BAR_PADDING, PLANNING_XP_BAR_PADDING + tempRect.height),
                                (PLANNING_XP_TEXT2_SIZE[0], PLANNING_XP_TEXT2_SIZE[1]) )
        textSurface = textrect.render_textrect("Reserve:", tempFont, tempRect, BOX_FONT_COLOR, (0, 0, 0), 0, True)
        self.xpBox.mainPane.blit(textSurface, tempRect.topleft)

        self.rectReserve = pygame.Rect(tempRect)
        self.rectReserve.right = self.xpBox.rect.width - PLANNING_XP_BAR_PADDING

        tempRect.top += tempRect.height + PLANNING_XP_BAR_PADDING
        textSurface = textrect.render_textrect("Next Lvl:", tempFont, tempRect, BOX_FONT_COLOR, (0, 0, 0), 0, True)
        self.xpBox.mainPane.blit(textSurface, tempRect.topleft)

        self.rectNext = pygame.Rect(tempRect)
        self.rectNext.right = self.xpBox.rect.width - PLANNING_XP_BAR_PADDING
        
        self.xpBox.rect.top = self.pieceBox.box.rect.bottom + 5
        self.xpBox.center(ENTIRE_SCREEN, True, False)
        self.xpMeter.center(self.xpBox.rect, True, False)
        self.xpMeter.loc[1] += PLANNING_XP_BAR_PADDING
        self.xpMeter.loc[0] += self.xpBox.rect.left + (PLANNING_XP_TEXT_SIZE[0] / 2)
        self.xpMeter.loc[1] += self.xpBox.rect.top

    def numActiveChars(self):
        tempCount = 0
        for sel in self.pieceBox.charSelections:
            if sel:
                tempCount += 1
        return tempCount

    def validCharacter(self):
        if self.currActiveCharacter() < len(self.pieceBox.characters):
            return True
        else:
            return False

    def goSelectXP(self):
        self.selectedXP = True
        self.cursorMoveSuccess()

    def currNextLevel(self):
        return self.pieceBox.characters[self.currActiveCharacter()].xpToNextLevel()

    def confirmXP(self):
        self.xp -= self.currNextLevel()
        self.pieceBox.characters[self.currActiveCharacter()].levelUp()
        self.selectedXP = False
        self.cursorMoveSuccess(False)
        self.xpMeter.update(self.xp)
        self.xpMeter.segment = 0
