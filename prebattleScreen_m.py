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

import planningScreen
import background
import scrollingBackground
import incint
import soundSystem

from constants import *

class Model(model.Model):
    def __init__(self, characters):
        super(Model, self).__init__()

        self.goBack = False
        self.goForward = False
        
        self.planningScreen = planningScreen.PlanningScreen(True, characters)

    def update(self):
        self.planningScreen.update()

    def advance(self):
        return self.goForward

    def back(self):
        return self.goBack

    def cursorMoveUp(self):
        self.planningScreen.cursorMoveUp()

    def cursorMoveDown(self):
        self.planningScreen.cursorMoveDown()

    def cursorMoveLeft(self):
        self.planningScreen.cursorMoveLeft()

    def cursorMoveRight(self):
        self.planningScreen.cursorMoveRight()

    def confirm(self):
        currChar = self.planningScreen.currActiveCharacter()
        self.planningScreen.pieceBox.tryLight(currChar)

        if self.planningScreen.cursorPos[1].isMax():
            tempNum = self.planningScreen.numActiveChars()
            if (tempNum >= 1) and (tempNum <= MAX_CHAR_ACTIVE):
                soundSystem.playSound(1)
                self.goForward = True
