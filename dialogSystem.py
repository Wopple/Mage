#!/usr/bin/env python

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

import box
import incint
import textrect

from constants import *

class DialogSystem(object):
    def __init__(self, inText, inSpeed):

        self.makeDialogBox()
        self.text = inText
        self.tick = incint.IncInt(0, 0, inSpeed - 1)
        tempNum = int( (self.dialogBox.rect.width - (DIALOG_BOX_BORDER_SIZE * 2) - (DIALOG_BOX_PADDING * 2)) / DIALOG_BOX_ELEMENT_SIZE[0] )
        self.letter = incint.IncInt(0, 0, tempNum)
        self.line = incint.IncInt(0, 0, DIALOG_BOX_NUM_OF_LINES - 1)
        self.nextLetter = pygame.Surface(DIALOG_BOX_ELEMENT_SIZE)
        self.nextPos = (0, 0)
        self.fonts = [pygame.font.Font(DIALOG_BOX_FONT_NORMAL, DIALOG_BOX_FONT_NORMAL_SIZE)]
        self.createOverlay()


    def makeDialogBox(self):
        tempX = DIALOG_BOX_SPACING
        sizeX = SCREEN_SIZE[0] - (DIALOG_BOX_SPACING * 2)
        sizeY = (DIALOG_BOX_ELEMENT_SIZE[1] * DIALOG_BOX_NUM_OF_LINES) + (DIALOG_BOX_PADDING * (DIALOG_BOX_NUM_OF_LINES + 1))
        r = pygame.Rect( (tempX, 0), (sizeX, sizeY) )
        r.bottom = SCREEN_SIZE[1] - DIALOG_BOX_SPACING
        self.dialogBox = box.Box(r, DIALOG_BOX_BG_IMAGE, DIALOG_BOX_BG_SIZE, DIALOG_BOX_BORDER, DIALOG_BOX_BORDER_SIZE)

    def update(self):
        if len(self.text) > 0:
            if len(self.text[0]) > 0:
                self.tick.inc()
                if self.tick.isMin():
                    self.nextLetter = textrect.render_textrect(self.text[0][0], self.fonts[0],
                                                    pygame.Rect((0, 0),DIALOG_BOX_ELEMENT_SIZE),
                                                    DIALOG_BOX_FONT_COLOR, (0, 0, 0), 1, True)
                    self.text[0] = self.text[0][1:]
                    tempX = DIALOG_BOX_BORDER_SIZE + DIALOG_BOX_PADDING + (DIALOG_BOX_ELEMENT_SIZE[0] * self.letter.value)
                    tempY = DIALOG_BOX_BORDER_SIZE + (DIALOG_BOX_PADDING * (self.line.value + 1))
                    self.nextPos = (tempX, tempY)
                    self.incrementCounter()

    def draw(self, screen):
        self.dialogBox.draw(screen)
        self.overlay.blit(self.nextLetter, self.nextPos)
        screen.blit(self.overlay, self.dialogBox.rect.topleft)

    def incrementCounter(self):
        self.letter.inc()
        if self.letter.isMin():
            self.line.inc()

    def createOverlay(self):
        self.overlay = pygame.Surface((self.dialogBox.rect.width, self.dialogBox.rect.height))
