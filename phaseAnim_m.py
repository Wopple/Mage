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
import soundSystem

import model

from constants import *

class Model(model.Model):
    def __init__(self, inPhase):
        super(Model, self).__init__()

        self.slowCounter = 0
        self.didStop = False
        self.goForward = False

        tempPath = PHASE_IMAGE + str(inPhase) + PHASE_IMAGE_EXT
        tempPath = os.path.join(GRAPHICS_PATH, tempPath)
        tempImage = pygame.image.load(tempPath).convert_alpha()

        self.images = []
        self.rects = []

        for i in range(2):
            self.rects.append(pygame.Rect( (0,(300 * i + 20)), (PHASE_IMAGE_WIDTHS[inPhase], (PHASE_IMAGE_HEIGHT / 2)) ))
            tempSurface = pygame.Surface((self.rects[i].width, self.rects[i].height))
            tempSurface.set_colorkey(BLACK)
            tempSurface.fill(BLACK)
            tempSurface.blit(tempImage, (0,(self.rects[i].height * i * -1)))
            self.images.append(tempSurface)

        self.rects[0].topleft = (SCREEN_SIZE[0], ((SCREEN_SIZE[1] / 2) - self.rects[0].height))
        self.rects[1].topleft = ((0 - self.rects[1].width), (SCREEN_SIZE[1] / 2))

        self.shutter = pygame.Surface(SCREEN_SIZE)
        self.shutter.fill(BLACK)
        self.shutter.set_alpha(SHUTTER_ALPHA)

        self.shutterRects = []
        for i in range(2):
            self.shutterRects.append(pygame.Rect((0, 0), SCREEN_SIZE))

        self.shutterRects[0].bottom = 0
        self.shutterRects[1].top = SCREEN_SIZE[1]

    def update(self):
        speed = 0
        shutterDir = 0
        if self.slowCounter == 0:
            self.slowCounter = -1
            if self.didStop:
                soundSystem.playSound(4)
            else:
                soundSystem.playSound(3)
        if self.slowCounter <= 0:
            speed = PHASE_IMAGE_SPEED_FAST
            if self.didStop:
                shutterDir = -1
            else:
                shutterDir = 1
        else:
            speed = PHASE_IMAGE_SPEED_SLOW
            self.slowCounter -= 1
            shutterDir = 0
        self.rects[0].left -= speed
        self.rects[1].left += speed
        
        self.shutterRects[0].top += SHUTTER_SPEED * shutterDir
        self.shutterRects[1].top -= SHUTTER_SPEED * shutterDir
        

        if (self.rects[0].left <= self.rects[1].left) and (not self.didStop):
            self.didStop = True
            self.slowCounter = PHASE_IMAGE_SLOW_TIME

        if (self.rects[0].right < 0) and (self.rects[1].left > SCREEN_SIZE[0]):
            self.goForward = True

        

    def advance(self):
        return self.goForward
