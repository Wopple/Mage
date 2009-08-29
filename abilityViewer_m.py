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
import cardCollection

from constants import *

class Model(model.Model):
    def __init__(self, inAbilities, inBG):
        super(Model, self).__init__()

        self.goBack = False
        self.goForward = False

        self.background = pygame.Surface(SCREEN_SIZE)
        self.background.blit(inBG, (0, 0))
        tempVeil = pygame.Surface(SCREEN_SIZE)
        tempVeil.fill(BLACK)
        tempVeil.set_alpha(CARD_VIEWER_VEIL)
        self.background.blit(tempVeil, (0, 0))

        
        self.cardCollection = cardCollection.CardCollection(inAbilities)

    def update(self):
        self.cardCollection.update()

    def decMenu(self):
        self.cardCollection.dec()

    def incMenu(self):
        self.cardCollection.inc()

    def confirm(self):
        self.goForward = True

    def advance(self):
        return self.goForward

    def cancel(self):
        self.goBack = True

    def back(self):
        return self.goBack

    def getSel(self):
        return self.cardCollection.selection.value

