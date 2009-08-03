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
from math import sqrt
import random
import textrect
import incint


class Menu(object):
    def __init__(self, screenSizeX, screenSizeY, posY, title, options, fontSize, colorBG=(30, 30, 30)):

        self.title = title
        self.options = options
        
        self.selection = incint.IncInt(1, 1, len(options))

        self.font = pygame.font.Font("fontdata.ttf", fontSize)
        self.lineSize = (fontSize*2) + 4

        self.x1 = 0
        self.y1 = posY
        self.sizeX = screenSizeX
        self.sizeY = (self.lineSize * (len(self.options) + 2)) + 8

        self.colorBG = colorBG
        self.colorOn = (250, 250, 0)
        self.colorOff = (250, 250, 250)

        self.slate = pygame.Surface( (screenSizeX, self.sizeY) )
        self.slate.fill (self.colorBG, (0, 0, screenSizeX, self.sizeY))

        self.hasSound = False


    def incrementSelection(self):
        if self.hasSound:
            self.sound1.play()
        self.selection.increment()

    def decrementSelection(self):
        if self.hasSound:
            self.sound1.play()
        self.selection.decrement()

    def activate(self):
        if self.hasSound:
            self.sound2.play()

    def reset(self):
        self.selection.value = 1

    def setSounds(self, sound1, sound2):
        self.hasSound = True
        self.sound1 = sound1
        self.sound2 = sound2

    def update(self, options):
        self.options = options
        self.selection = incint.IncInt(self.selection.value, 1, len(options))
        
    def draw(self, screen):
        screen.blit(self.slate, (self.x1, self.y1))

        currY = self.y1 + 4
        textRect = pygame.rect.Rect((self.x1 + 4), currY, (self.sizeX-4), self.lineSize)
        textSurface = textrect.render_textrect(self.title, self.font, textRect, self.colorOff, self.colorBG, 1)
        screen.blit(textSurface, textRect)
        currY += self.lineSize
        
        counter = 0
        while counter < len(self.options):
            currY += self.lineSize
            textRect = pygame.rect.Rect((self.x1 + 4), currY, (self.sizeX-4), self.lineSize)
            if self.selection.value == (counter + 1):
                currColor = self.colorOn
            else:
                currColor = self.colorOff
            textSurface = textrect.render_textrect(self.options[counter], self.font, textRect, currColor, self.colorBG, 1)
            screen.blit(textSurface, textRect)
            counter += 1

    def value(self):
        return self.selection.value
