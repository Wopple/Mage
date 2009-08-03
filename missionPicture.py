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

import textrect

NOT_EXIST_TEXT = None
NOT_EXIST_RECT = None
SLATE = None

class MissionPicture(object):
    def __init__(self, topRange, bottomRange, inPath):

        posX = (SCREEN_SIZE[0] / 2) - (MISSION_PICTURE_SIZE[0] / 2)
        posY = ((bottomRange - topRange) / 2) - (MISSION_PICTURE_SIZE[1] / 2) + topRange
        self.rect = pygame.Rect( (posX, posY), MISSION_PICTURE_SIZE)

        self.imageExists = False

        pathName = os.path.join(inPath, MISSION_PICTURE)
        if os.path.exists(pathName):
            image = pygame.image.load(pathName).convert_alpha()
            self.image = pygame.Surface( (self.rect.width, self.rect.height) )
            self.image.blit(image, (0, 0))
            self.imageExists = True


        global NOT_EXIST_TEXT
        global NOT_EXIST_RECT
        global SLATE
        if NOT_EXIST_TEXT is None:
            
            font = pygame.font.Font(FONTS[0], MISSION_PICTURE_NEM_SIZE)
            posY = (self.rect.height / 2) - (MISSION_PICTURE_NEM_SIZE / 2) + self.rect.top
            NOT_EXIST_RECT = pygame.Rect( (self.rect.left, posY), (self.rect.width, (MISSION_PICTURE_NEM_SIZE + 4)) )
            NOT_EXIST_TEXT = textrect.render_textrect("No Picture Available", font, NOT_EXIST_RECT, MISSION_PICTURE_NEM_COLOR, MISSION_PICTURE_COLOR, 1)

            SLATE = pygame.Surface( (self.rect.width, self.rect.height) )
            SLATE.fill (MISSION_PICTURE_COLOR, (0, 0, self.rect.width, self.rect.height))

    def draw(self, screen):
        screen.blit(SLATE, self.rect.topleft)

        if self.imageExists:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(NOT_EXIST_TEXT, NOT_EXIST_RECT.topleft)
