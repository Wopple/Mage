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

import incint

class PieceTicker(object):
    def __init__(self, inSpeed):

        self.ticker = incint.IncInt(0, 0, (SPRITE_SHEET_NUM_X - 1))
        self.sub = [incint.IncInt(0, 0, inSpeed[0]),
                        incint.IncInt(0, 0, inSpeed[1])]
        self.goUp = True

    def update(self):
        if self.ticker.isBound():
            useTicker = 0
        else:
            useTicker = 1

        self.sub[useTicker].increment()

        if self.sub[useTicker].isMin():
            if self.goUp:
                self.ticker.increment()
            else:
                self.ticker.decrement()

            if self.ticker.isMin():
                self.goUp = True
            if self.ticker.isMax():
                self.goUp = False

    def value(self):
        return self.ticker.value

    def reset(self):
        self.ticker.value = 0
        self.sub[0].value = 0
        self.sub[1].value = 0
        self.goUp = True
