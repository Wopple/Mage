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

from constants import *

class Background(object):
    def __init__(self, inRect, inImage, imageSize):

        self.mainRect = inRect
        self.mainPane = pygame.Surface((self.mainRect.width, self.mainRect.height))
        pattern = pygame.image.load(os.path.join(GRAPHICS_PATH, inImage)).convert_alpha()

        tempFloat = float(float(inRect.width) / float(imageSize[0]))
        repeatX = int(math.ceil(tempFloat))
        tempFloat = float(float(inRect.height) / float(imageSize[1]))
        repeatY = int(math.ceil(tempFloat))

        sizeX = repeatX * imageSize[0]
        sizeY = repeatY * imageSize[0]
        self.subRect = pygame.Rect( (0, 0), (sizeX, sizeY) )
        self.subPane = pygame.Surface((self.subRect.width, self.subRect.height))

        for x in range (repeatX):
            for y in range (repeatY):
                self.subPane.blit(pattern, ( (x*imageSize[0]), (y*imageSize[1]) ) )


        self.mainPane.blit(self.subPane, self.subRect.topleft)

    def draw(self, screen):
        screen.blit(self.mainPane, self.mainRect.topleft)

    def update(self):
        pass
