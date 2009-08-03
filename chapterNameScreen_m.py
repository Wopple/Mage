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
import random

import model
import scrollingBackground

import chapterNameBox

from constants import *

class Model(model.Model):
    def __init__(self, inNum, inName):
        super(Model, self).__init__()

        
        self.state = "open"
        self.timer = int(CHAPTER_NAME_SECONDS * FRAME_RATE)
        self.nameBox = chapterNameBox.ChapterNameBox(inNum, inName)
        self.movementCounter = CHAPTER_NAME_MOVE_UP_DELAY
        self.veil = pygame.Surface(SCREEN_SIZE)
        self.veil.set_alpha(COLOR_MAX)
        tempRect = pygame.Rect( (0, 0), SCREEN_SIZE)
        self.background = scrollingBackground.ScrollingBackground(tempRect, CHAPTER_NAME_BG_PATTERN, CHAPTER_NAME_BG_PATTERN_SIZE,
                                                                  CHAPTER_NAME_BG_DIREC, CHAPTER_NAME_BG_SPEED)

    def update(self):
        if self.state == "open":
            self.openState()
        elif self.state == "close":
            self.closeState()
        else:
            self.holdState()
            
        self.glide()
        self.background.update()
        

    def glide(self):
        if self.movementCounter <= 0:
            self.nameBox.rect.top -= 1
            self.movementCounter = CHAPTER_NAME_MOVE_UP_DELAY
        self.movementCounter -= 1

    def holdState(self):
        if self.timer <= 0:
            self.state = "close"
        self.timer -= 1

    def openState(self):
        
        if self.changeAlpha(False):
            self.state = "hold"

    def closeState(self):
        if self.changeAlpha(True):
            self.state = "end"

    def changeAlpha(self, goUp):
        endFlag = False
        amount = FADE_IN
        if not goUp:
            amount *= -1

        currAlpha = self.veil.get_alpha()
        currAlpha += amount

        if currAlpha < COLOR_MIN:
            currAlpha = COLOR_MIN
            endFlag = True
        if currAlpha > COLOR_MAX:
            currAlpha = COLOR_MAX
            endFlag = True

        self.veil.set_alpha(currAlpha)
        return endFlag

    def advance(self):
        if self.state == "end":
            return True
        else:
            return False

    def back(self):
        return False
