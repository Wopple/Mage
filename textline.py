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

import sys
import pygame
from pygame.locals import *
import textrect

class TextLine(object):
    def __init__(self, screenSizeX, screenSizeY, posY, text, fontSize, align=0, colorBG=(30, 30, 30)):

        self.text = text

        self.font = pygame.font.Font("fontdata.ttf", fontSize)

        self.colorBG = colorBG
        self.textColor = (250, 250, 250)

        
        self.rect = pygame.Rect( (0, posY), (screenSizeX, (fontSize + 4)) )
        self.textRect = pygame.Rect( (0, posY), (screenSizeX, (fontSize + 8)) )
        self.textSurface = textrect.render_textrect(self.text, self.font, self.textRect, self.textColor, self.colorBG, align)


        self.slate = pygame.Surface( (self.rect.width, self.rect.height) )
        self.slate.fill (self.colorBG, (0, 0, self.rect.width, self.rect.height))

    def draw(self, screen):
        screen.blit(self.slate, self.rect.topleft)
        screen.blit(self.textSurface, self.textRect)
