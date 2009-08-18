# Copyright 2009 Christopher Czyzewski, Daniel Tashjian
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

import textrect

from constants import *

TABS = None

class Card(object):
    def __init__(self, ability):

        global TABS
        if TABS is None:
            TABS = []
            for x in range(0, 4):
                TABS.append(pygame.image.load(os.path.join(GRAPHICS_PATH,CARD_TAB_FILE + str(x) + CARD_TAB_FILE_EXT)).convert_alpha())


        self.image = pygame.Surface(CARD_SIZE)
        self.image.fill(CARD_BORDER_COLOR_DARK)

        tempX = CARD_SIZE[0] - (CARD_BORDER * 2)
        tempY = CARD_SIZE[1] - (CARD_BORDER * 2)
        tempFill = pygame.Surface((tempX, tempY))
        tempFill.fill(CARD_BORDER_COLOR_LIGHT)
        self.image.blit(tempFill, (CARD_BORDER, CARD_BORDER))

        tempX = CARD_SIZE[0] - (CARD_BORDER * 4)
        tempY = CARD_SIZE[1] - (CARD_BORDER * 4)
        tempFill = pygame.Surface((tempX, tempY))
        tempFill.fill(CARD_NEUTRAL_COLOR)
        self.image.blit(tempFill, ((CARD_BORDER * 2), (CARD_BORDER * 2)))


        
        self.rect = pygame.Rect((5, 5), CARD_SIZE)

        fontBig = pygame.font.Font(CARD_FONT, CARD_FONT_SIZE_BIG)

        for t in range(0, 4):
            tempX = (CARD_BORDER * 2) + CARD_OUTTER_PADDING + ((CARD_INNER_PADDING + CARD_TAB_SIZE[0]) * t)
            tempY = (CARD_BORDER * 2)
            self.image.blit(TABS[t], (tempX, tempY))

        tempArea = textrect.render_textrect(ability.name, fontBig,
                                            pygame.Rect((0, 0),CARD_NAME_SIZE),
                                            CARD_FONT_COLOR, CARD_INDENT_COLOR, 0)
        tempX = (CARD_BORDER * 2) + CARD_OUTTER_PADDING
        tempY = (CARD_BORDER * 2) + CARD_OUTTER_PADDING + CARD_TAB_SIZE[1] + CARD_INNER_PADDING
        self.image.blit(tempArea, (tempX, tempY))

        tempArea = textrect.render_textrect(ability.desc, fontBig,
                                            pygame.Rect((0, 0),CARD_DESC_SIZE),
                                            CARD_FONT_COLOR, CARD_INDENT_COLOR, 0)
        tempY += CARD_NAME_SIZE[1] + CARD_INNER_PADDING
        self.image.blit(tempArea, (tempX, tempY))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def newIndent(self, inSize):
        newArea = pygame.Surface(inSize)
        newArea.fill(CARD_INDENT_COLOR)
        return newArea

    def setLoc(self, inX, inY):
        self.rect.left = inX
        self.rect.top = inY
