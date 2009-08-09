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

import null
import turn
import enemy

class AI(object):
    def __init__(self, battle):
        self.battle = battle
        self.reset()

    def reset(self):
        self.order = []
        self.turn = null.NullTurnAI(self.battle, self.order)
        self.state = 'turn'
        self.started = False
        self.enemies = []
        self.numEnemies = 0
        self.currentEnemy = 0

    def run(self):
        # Run the AI which determines the turn order.
        if self.state == 'turn':
            if self.started:
                if not self.turn.isAlive():
                    self.state = 'enemies'
                    self.started = False

                    # Create the list of AI's for the enemies.
                    for enemy in self.order:
                        self.enemies.append(enemy.getAI()(self.battle))
                        self.numEnemies = len(self.enemies)
            else:
                self.turn.start()
                self.started = True
        # Run each of the AI's for the enemies.
        elif self.state == 'enemies':
            if self.currentEnemy == self.numEnemies:
                self.state = 'done'
            else:
                if self.started:
                    if self.enemies[self.currentEnemy].isAlive():
                        self.started = False
                        self.currentEnemy += 1
                else:
                    self.enemies[self.currentEnemy].start()
                    self.started = True
        # Finish up.
        elif self.state == 'done':
            self.battle.nextPhase()
