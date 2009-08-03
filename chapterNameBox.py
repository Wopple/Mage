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
import random

from constants import *

import textrect

class ChapterNameBox(object):
    def __init__(self, chapterNumber, chapterName):

        chapterNumber += 1
        
        pattern1 = pygame.image.load(os.path.join(GRAPHICS_PATH, CHAPTER_NAME_PATTERN)).convert_alpha()
        pattern2 = pygame.transform.flip(pattern1, True, False)
        border1 = pygame.image.load(os.path.join(GRAPHICS_PATH, CHAPTER_NAME_BORDER)).convert_alpha()
        border2 = pygame.transform.rotate(border1, 90)
        border3 = pygame.transform.rotate(border1, 180)
        border4 = pygame.transform.rotate(border1, 270)

        font1 = pygame.font.Font(FONTS[0], CHAPTER_NAME_FONTSIZE1)
        font2 = pygame.font.Font(FONTS[0], CHAPTER_NAME_FONTSIZE2)

        sizeX = (CHAPTER_NAME_PATTERN_SIZE * 2)
        sizeY = CHAPTER_NAME_BAR_HEIGHT
        posX = (SCREEN_SIZE[0] / 2) - (sizeX / 2)
        posY = (SCREEN_SIZE[1] / 2) - (sizeY / 2)
        self.rect = pygame.Rect( (posX, posY), (sizeX, sizeY))
        self.box = pygame.Surface( (sizeX, sizeY) )

        #Create Primary Bar
        for y in range (sizeY):
            self.box.blit(pattern1, (0, y))
            tempX = (int(sizeX / 2))
            self.box.blit(pattern2, (tempX, y))

        
        #Create Text
        tempRect = pygame.Rect( (0, (CHAPTER_NAME_BORDER_SIZE + 2)), (self.rect.width, (CHAPTER_NAME_FONTSIZE1 + 4)) )
        tempText = "Chapter " + str(chapterNumber)
        textrect1 = textrect.render_textrect(tempText, font1, tempRect, CHAPTER_NAME_COLOR, (0, 0, 0), 1, True)
        self.box.blit(textrect1, tempRect.topleft)

        tempRect = pygame.Rect( (0, 0), (self.rect.width, (CHAPTER_NAME_FONTSIZE2 + 4)) )
        tempRect.top = (self.rect.height / 2) - (tempRect.height / 2)
        textrect2 = textrect.render_textrect(chapterName, font2, tempRect, CHAPTER_NAME_COLOR, (0, 0, 0), 1, True)
        self.box.blit(textrect2, tempRect.topleft)

        #Create Border Sides
        for y in range (sizeY):
            self.box.blit(border2, (0, y))
            tempX = sizeX - CHAPTER_NAME_BORDER_SIZE
            self.box.blit(border4, (tempX, y))
        for x in range(sizeX):
            self.box.blit(border1, (x, 0))
            tempY = sizeY - CHAPTER_NAME_BORDER_SIZE
            self.box.blit(border3, (x, tempY))

        

    def draw(self, screen):
        screen.blit(self.box, self.rect.topleft)
