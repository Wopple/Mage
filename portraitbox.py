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

import box
import portrait

from constants import *

class PortraitBox(object):
    def __init__(self):

        sizeX = PORTRAIT_SIZE_PLANNING[0] + (PORTRAIT_BOX_BORDER_SIZE * 2) + (PORTRAIT_BOX_PADDING * 2)
        sizeY = PORTRAIT_SIZE_PLANNING[1] + (PORTRAIT_BOX_BORDER_SIZE * 2) + (PORTRAIT_BOX_PADDING * 2)
        tempRect = pygame.Rect( (0, 0), (sizeX, sizeY) )
        self.box = box.Box(tempRect, PORTRAIT_BOX_PATTERN, PORTRAIT_BOX_PATTERN_SIZE,
                           PORTRAIT_BOX_BORDER, PORTRAIT_BOX_BORDER_SIZE)
        self.portrait = None
        tempLoc = PORTRAIT_BOX_BORDER_SIZE + PORTRAIT_BOX_PADDING
        self.portLoc = (tempLoc, tempLoc)

    def draw(self, screen):
        self.box.draw(screen)

        if not(self.portrait is None):
            loc = (self.portLoc[0] + self.box.rect.left, self.portLoc[1] + self.box.rect.top)
            self.portrait.update(loc)
            self.portrait.draw(screen)

    def update(self, in_image):

        if in_image is None:
            self.portrait = None
        else:
            self.portrait = portrait.Portrait(in_image, PORTRAIT_SIZE_PLANNING, (0,0))
