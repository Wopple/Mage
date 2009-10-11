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

        self.cardGreyer = pygame.Surface(CARD_SIZE)
        self.cardGreyer.fill(CARD_GREYER_COLOR)
        self.cardGreyerNum = 0
        
        self.cardCollection = cardCollection.CardCollection(inAbilities)

        self.makeNEM()
        self.updateNEM()

    def update(self):
        self.cardCollection.update()
        self.updateGreyer()

    def decMenu(self):
        self.cardCollection.dec()
        self.updateNEM()
        self.cardGreyerNum = 0

    def incMenu(self):
        self.cardCollection.inc()
        self.updateNEM()
        self.cardGreyerNum = 0

    def confirm(self):
        if not self.notEnoughManaVisible:
            self.goForward = True

    def advance(self):
        return self.goForward

    def cancel(self):
        self.goBack = True

    def back(self):
        return self.goBack

    def getSel(self):
        return self.cardCollection.selection.value

    def makeNEM(self):
        self.notEnoughMana = pygame.image.load(NOT_ENOUGH_MANA_FILE).convert_alpha()
        zoomLoc = self.cardCollection.getZoomLoc()
        tempX = (CARD_SIZE[0] / 2) - (NOT_ENOUGH_MANA_IMAGE_SIZE[0] / 2) + zoomLoc[0]
        tempY = (CARD_SIZE[1] / 2) - (NOT_ENOUGH_MANA_IMAGE_SIZE[1] / 2) + zoomLoc[1]
        self.notEnoughManaRect = pygame.Rect( (tempX, tempY), (NOT_ENOUGH_MANA_IMAGE_SIZE) )
        self.notEnoughManaVisible = False

    def updateNEM(self):
        self.notEnoughManaVisible = not(self.cardCollection.currCardTempFlag())

    def updateGreyer(self):
        if self.notEnoughManaVisible:
            self.cardGreyerNum += CARD_GREYER_SPEED
            if self.cardGreyerNum > CARD_GREYER_MAX:
                self.cardGreyerNum = CARD_GREYER_MAX
        else:
            self.cardGreyerNum = 0
        self.cardGreyer.set_alpha(self.cardGreyerNum)
