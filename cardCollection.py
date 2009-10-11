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
import random

ARROW = None

class CardCollection(object):
    def __init__(self, inAbilities):

        random.seed()

        global ARROW
        if ARROW is None:
            ARROW = pygame.image.load(CARD_ARROW_FILE).convert_alpha()
            
        self.arrowRect = pygame.Rect((0, 0), CARD_ARROW_SIZE)

        self.zoomCard = None
        self.cards = []
        for x in inAbilities:
            self.cards.append(card.Card(x))
        self.selection = incint.IncInt(0, 0, (len(self.cards)-1))
        self.bobber = incint.IncInt(0, 0, CARD_ARROW_BOB, True)

        if len(self.cards) <= 0:
            fatalError()

        for c in self.cards:
            dice = random.randint((CARD_RANDOM_SHIFT * -1), CARD_RANDOM_SHIFT)
            tempX = (SCREEN_SIZE[0] / 4) - (CARD_SIZE[0] / 2) + dice
            c.rect.left = tempX

        self.change()

    def update(self):
        self.bobber.bob()

    def change(self):
        self.zoomCard = pygame.Surface(CARD_SIZE)
        self.zoomCard.blit(self.cards[self.selection.value].image, (0,0))

        if len(self.cards) <= 0:
            fatalError()
            
        stackSize = SCREEN_SIZE[1] - CARD_STACK_FROM_BOTTOM - CARD_STACK_FROM_TOP
        areaPerCard = float(float(stackSize) / float(len(self.cards)))
        
        for c in range(len(self.cards)):
            tempY = CARD_STACK_FROM_TOP + (areaPerCard * c)
            if self.selection.value == c:
                tempY -= CARD_STICK_UP
                self.arrowRect.bottom = tempY - CARD_ARROW_GAP
                self.arrowRect.left = self.cards[c].rect.left + (self.cards[c].rect.width / 2) - (self.arrowRect.width / 2)
            self.cards[c].rect.top = tempY

    def inc(self):
        self.selection.inc()
        self.change()

    def dec(self):
        self.selection.dec()
        self.change()

    def draw(self, screen):
        self.drawStack(screen)
        self.drawZoom(screen)

    def drawZoom(self, screen):
        tempX = ((SCREEN_SIZE[0] / 4) * 3) - (CARD_SIZE[0] / 2)
        tempY = (SCREEN_SIZE[1] / 2) - (CARD_SIZE[1] / 2)
        screen.blit(self.zoomCard, (tempX, tempY))

    def drawStack(self, screen):
        for c in self.cards:
            c.draw(screen)
        tempArrowY = self.arrowRect.top - self.bobber.value
        screen.blit(ARROW, (self.arrowRect.left, tempArrowY))

    def currCardTempFlag(self):
        return self.cards[self.selection.value].tempFlag
        
