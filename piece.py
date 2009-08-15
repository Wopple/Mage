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

from constants import *

class Piece(object):
    def __init__(self, spriteSheet=None):
        self.changeSpriteSheet(spriteSheet)
        self.location = (0, 0)
        
        self.group = 0
        self.frame = 0
        self.hasMove = False
        self.hasAction = False
        self.hasSpike = True
        self.visible = True

        self.hpCurr = 0
        self.mpCurr = [0, 0, 0]

    def changeSpriteSheet(self, spriteSheet):
        self.spriteSheet = spriteSheet
        if not(self.spriteSheet is None):
            self.spriteSheet

    def update(self, inGroup, inFrame):
        if inGroup != -1:
            self.group = inGroup
        self.frame = inFrame

    def draw(self, screen):
        if not(self.spriteSheet is None) and self.visible:
            surface = pygame.Surface(PIECE_SIZE)
            surface.set_colorkey(TRANSPARENT_COLOR)
            surface.fill(TRANSPARENT_COLOR)
            tempX = (PIECE_SIZE[0] * self.frame) * -1
            tempY = (PIECE_SIZE[1] * self.group) * -1
            surface.blit(self.spriteSheet, (tempX, tempY))
            screen.blit(surface, self.location)

    def canMove(self):
        return self.hasMove
