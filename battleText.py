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

from constants import *

import textrect

class BattleText(object):
    def __init__(self, inText, inColor, inLoc):

        self.rect = pygame.Rect(inLoc, BATTLE_TEXT_SIZE)
        font = pygame.font.Font(BATTLE_TEXT_FONT, BATTLE_TEXT_FONT_SIZE)
        self.image = textrect.render_textrect(inText, font, self.rect,
                                              inColor, BLACK, 1, True)
        self.count = 0
        self.remove = False

    def update(self):
        self.count += 1
        if self.count >= BATTLE_TEXT_REMOVAL_VALUE:
            self.remove = True

    def draw(self, screen):
        if self.count > 0:
            loc = (self.rect.left, self.rect.top - self.count)
            screen.blit(self.image, loc)
