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
import os
import pygame

from constants import *

class Model(object):
    def __init__(self, model=None, view=None):
        self.view = view
        self.undefUpdate = False

    def setView(self, view):
        self.view = view

    def update(self):
        self.undefUpdate = True

    def checkError(self):
        if self.undefUpdate:
            return True
        else:
            return False

    def advance(self):
        return False

    def back(self):
        return False

    def either(self):
        return (self.advance() or self.back())

    def cancel(self):
        pass

    def pressCheat(self, inCheat):
        if DEBUG_MODE:
            self.goCheat(inCheat)

    def goCheat(self, inCheat):
        pass
