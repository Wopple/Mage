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

class Portrait(object):
    def __init__(self, in_image, in_size, in_loc):

        tempSurface = pygame.Surface(PORTRAIT_SIZE_ORIG)
        tempSurface.set_colorkey(BLACK)
        tempSurface.fill(BLACK)
        tempSurface.blit(in_image, (0,0))

        if in_size != PORTRAIT_SIZE_ORIG:
            self.image = pygame.Surface(in_size)
            pygame.transform.scale(tempSurface, in_size, self.image)
            self.image.set_colorkey(BLACK)
        else:
            self.image = tempSurface

        self.rect = pygame.Rect(in_loc, in_size)

    def update(self, loc):
        self.rect.topleft = loc

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
