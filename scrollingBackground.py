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

import background

from constants import *

class ScrollingBackground(background.Background):
    def __init__ (self, inRect, inImage, imageSize, inDirec, inSpeed):
        super(ScrollingBackground, self).__init__(inRect, inImage, imageSize)

        self.scrollPane = pygame.Surface.copy(self.subPane)
        #self.scrollPane.blit(self.subPane, (0, 0))
        
        #Directions: 0 = Up, 1 = Down, 2 = Left, 3 = Right.  Default to Right
        self.movement = [0, 0]
        self.scrollOrigin = [0, 0]
        if inDirec == 0:
            self.movement[1] = inSpeed * -1
            self.scrollOrigin[1] += self.subRect.height
        elif inDirec == 1:
            self.movement[1] = inSpeed
            self.scrollOrigin[1] -= self.subRect.height
        elif inDirec == 2:
            self.movement[0] = inSpeed * -1
            self.scrollOrigin[0] += self.subRect.width
        else:
            self.movement[0] = inSpeed
            self.scrollOrigin[0] -= self.subRect.width
            
        self.scrollRect = pygame.Rect( self.scrollOrigin, (self.subRect.width, self.subRect.height) )
        self.adjust()


    def update(self):
        self.subRect.left += self.movement[0]
        self.subRect.top += self.movement[1]
        
        self.scrollRect.left += self.movement[0]
        self.scrollRect.top += self.movement[1]

        if abs(self.subRect.left) > self.subRect.width:
            self.adjust()
        if abs(self.subRect.top) > self.subRect.height:
            self.adjust()

        self.mainPane.blit(BLACK_SCREEN, (0, 0))
        self.mainPane.blit(self.subPane, self.subRect.topleft)
        self.mainPane.blit(self.scrollPane, self.scrollRect.topleft)

    def adjust(self):
        if self.subRect.left < 0:
            self.subRect.left += self.subRect.width
        elif self.subRect.left > 0:
            self.subRect.left -= self.subRect.width

        if self.subRect.top < 0:
            self.subRect.top += self.subRect.height
        elif self.subRect.top > 0:
            self.subRect.top -= self.subRect.height

        self.scrollRect.left = (self.scrollOrigin[0] + self.subRect.left)
        self.scrollRect.top = (self.scrollOrigin[1] + self.subRect.top)
