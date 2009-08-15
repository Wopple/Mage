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

import model

import minimenu

from constants import *

class Model(model.Model):
    def __init__(self):
        super(Model, self).__init__()
        tempRect = pygame.Rect( (50, 50), (200, 0) )
        self.titleMenu = minimenu.MiniMenu(tempRect, ["Start New Game", "Load Game", "Quit"],
                                           MAIN_MENU_FONT_SIZE, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF, MAIN_MENU_COLOR_BG)
        self.titleMenu.center(ENTIRE_SCREEN, True, True)
        self.confirmed = False

    def incMenu(self):
        self.titleMenu.inc()

    def decMenu(self):
        self.titleMenu.dec()

    def confirm(self):
        self.confirmed = True

    def update(self):
        pass

    def advance(self):
        if (self.confirmed == True) and not (self.back()):
            return True
        else:
            return False

    def back(self):
        if (self.confirmed == True) and (self.titleMenu.value() == 4):
            return True
        else:
            return False
