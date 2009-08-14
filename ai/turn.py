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
        super(TurnAI, self).__init__()
        self.battle = battle
        self.order = order

    def run(self):
        playerCenter = self.getCenter(self.battle.characters)
        enemyCenter = self.getCenter(self.battle.characters)

        for enemy in self.battle.enemies:
            self.order.append(enemy)

    # Finds the center of the given list of objects.
    # return: tuple of floats (x,y)
    def getCenter(self, objects):
        totalX = 0
        totalY = 0
        num = len(objects)

        for x in range(len(self.battle.field)):
            for y in range(len(self.battle.field[x])):
                fieldLocation = self.battle.field[x][y]
                if len(fieldLocation) > 0:
                    if fieldLocation[0] in objects:
                        totalX += x
                        totalY += y

        return (float(totalX) / num, float(totalY) / num)
