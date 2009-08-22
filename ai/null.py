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

from model import Model

""" The NullAI class tells the battle to end the enemy phase. """
class NullAI(object):
    def __init__(self, battle):
        self.battle = battle

    def run(self):
        self.battle.nextPhase()

""" The NullTurnAI constructs the turn order arbitrarily. """
class NullTurnAI(threading.Thread):
    def __init__(self, battle, order):
        super(NullTurnAI, self).__init__()
        self.battle = battle
        self.order = order

    def run(self):
        for enemy in self.battle.enemies:
            self.order.append(enemy)

""" The NullCharacterAI has the character do nothing. """
class NullCharacterAI(threading.Thread):
    def __init__(self, character, battle, plan):
        super(NullCharacterAI, self).__init__()

    def run(self):
        pass
