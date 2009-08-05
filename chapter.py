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

class Chapter(object):
    def __init__(self, inName, inMap, inStartingPos, inObstacles):

        self.name = inName
        self.startingPos = inStartingPos

        self.createMapFromStrings(inMap)
        self.obstacles = inObstacles

    def createMapFromStrings(self, inMap):
        self.map = []

        for y in range(len(inMap)):
            self.map.append([])
            for x in range(len(inMap[y])):
                self.map[y].append(inMap[y][x])
