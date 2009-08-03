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

import portrait

from constants import *

class CornerInfo(object):
    def __init__(self):

        sizeX = CORNER_INFO_PORTRAIT_SIZE + (CORNER_INFO_PADDING * 2)
        sizeY = CORNER_INFO_PORTRAIT_SIZE + (CORNER_INFO_PADDING * 2)
        self.rect = pygame.Rect((0, 0), (sizeX, sizeY))
        self.portrait = None

    def update(self, side, in_portrait):
        if not in_portrait is None:
            self.portrait = portrait.Portrait(in_portrait, (CORNER_INFO_PORTRAIT_SIZE, CORNER_INFO_PORTRAIT_SIZE), (0,0))
        else:
            self.portrait = None
        
        #left = True, right = False
        if side:
            self.rect.left = 0
        else:
            self.rect.right = SCREEN_SIZE[0]
        self.rect.top = 0

    def draw(self, screen):
        if not self.portrait is None:
            mainPane = pygame.Surface((self.rect.width, self.rect.height))
            mainPane.fill(CORNER_INFO_COLOR)
            mainPane.set_alpha(CORNER_INFO_ALPHA)
            self.portrait.rect.left = self.rect.left + CORNER_INFO_PADDING
            self.portrait.rect.top = self.rect.top + CORNER_INFO_PADDING
            screen.blit(mainPane, self.rect.topleft)
            self.portrait.draw(screen)
