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

from constants import *

import card
import incint

class CardCollection(object):
    def __init__(self, inAbilities):

        self.zoomCard = None
        self.cards = []
        for x in inAbilities:
            self.cards.append(card.Card(x))
        self.selection = incint.IncInt(0, 0, (len(self.cards)-1))

        self.update()

    def update(self):
        self.zoomCard = pygame.Surface(CARD_SIZE)
        self.zoomCard.blit(self.cards[self.selection.value].image, (0,0))

    def inc(self):
        self.selection.inc()
        self.update()

    def dec(self):
        self.selection.dec()
        self.update()

    def draw(self, screen):
        self.drawStack(screen)
        self.drawZoom(screen)

    def drawStack(self, screen):
        pass

    def drawZoom(self, screen):
        tempX = ((SCREEN_SIZE[0] / 4) * 3) - (CARD_SIZE[0] / 2)
        tempY = (SCREEN_SIZE[1] / 2) - (CARD_SIZE[1] / 2)
        screen.blit(self.zoomCard, (tempX, tempY))
