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

import incint
import soundSystem

from constants import *

IMAGE = None

class Cursor(object):
    def __init__(self, inRect):

        global IMAGE
        if IMAGE is None:
            IMAGE = pygame.image.load(os.path.join(GRAPHICS_PATH, CURSOR_IMAGE)).convert_alpha()
        
        self.rect = inRect

        sizeX = self.rect.width + (CURSOR_STEPS * 2)
        sizeY = self.rect.height + (CURSOR_STEPS * 2)
        self.rect = pygame.Rect( self.rect.topleft, (sizeX, sizeY) )

        self.ticker = incint.IncInt(1, 1, CURSOR_STEPS)
        self.braker = incint.IncInt(1, 1, CURSOR_ANIM_SPEED)
        
        self.update(self.rect.topleft, (self.rect.width, self.rect.height))

    def update(self, inPos, inSize):
        self.braker.increment()
        if self.braker.value == self.braker.minimum:
            self.ticker.decrement()

        sizeX = inSize[0] + (CURSOR_STEPS * 2)
        sizeY = inSize[1] + (CURSOR_STEPS * 2)
        self.rect = pygame.Rect( self.rect.topleft, (sizeX, sizeY) )
        
        self.rect.topleft = inPos
        self.rect.left -= CURSOR_STEPS
        self.rect.top -= CURSOR_STEPS

        self.pane = pygame.Surface((self.rect.width, self.rect.height))
        self.pane.set_colorkey(BLACK)
        self.pane.fill(BLACK)

        sizeX = CURSOR_SIZE[0] + CURSOR_STEPS
        sizeY = CURSOR_SIZE[1] + CURSOR_STEPS

        cornerPane = pygame.Surface( (sizeX, sizeY) )
        cornerPane.blit(IMAGE, (self.ticker.value, self.ticker.value))
        self.pane.blit(cornerPane, (0,0))

        tempCornerX = self.rect.width - sizeX
        tempCornerY = self.rect.height - sizeY
        tempPane = pygame.Surface.copy(cornerPane)
        tempPane = pygame.transform.flip(tempPane, True, False)
        self.pane.blit(tempPane, (tempCornerX,0))
        tempPane = pygame.transform.flip(tempPane, False, True)
        self.pane.blit(tempPane, (tempCornerX, tempCornerY))
        tempPane = pygame.transform.flip(tempPane, True, False)
        self.pane.blit(tempPane, (0, tempCornerY))


    def draw(self, screen):
        screen.blit(self.pane, self.rect.topleft)

    def playSound(self):
        soundSystem.playSound(0)
