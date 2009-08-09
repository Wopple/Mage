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

import threading

class TurnAI(threading.Thread):
    def __init__(self, battle, order):
        self.battle = battle
        self.order = order

    def run(self):
        playerCenter = self.getCenter(self.battle.characters)
        enemyCenter = self.getCenter(self.battle.characters)

    # Finds the center of the given list of objects.
    # return: tuple of floats (x,y)
    def getCenter(self, objects):
        totalX = 0
        totalY = 0
        num = len(objects)

        for x in len(self.battle.field):
            for y in len(self.battle.field[x]):
                if self.battle.field[x][y][0] in objects:
                    centerX += x
                    centerY += y

        return (float(totalX) / num, float(totalY) / num)
