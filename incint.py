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

class IncInt:
    def __init__(self, in_value, in_min, in_max):
        self.value = in_value
        self.minimum = in_min
        self.maximum = in_max

        if self.minimum > self.maximum:
            print "Error in IncInt - Maximum value greater or equal to minimum value"
            print str(self.value) + " is not between " + str(self.minimum) + " and " + str(self.maximum)
            sys.exit()

        if (self.value < self.minimum) or (self.value > self.maximum):
            print "Error in IncInt - Value not in range"
            sys.exit()

    def increment(self):
        self.value += 1
        if self.value > self.maximum:
            self.value = self.minimum

    def decrement(self):
        self.value -= 1
        if self.value < self.minimum:
            self.value = self.maximum

    def isMin(self):
        if self.value == self.minimum:
            return True
        else:
            return False

    def isMax(self):
        if self.value == self.maximum:
            return True
        else:
            return False

    def isBound(self):
        return ( (self.isMin()) or (self.isMax()) )

    def inc(self):
        self.increment()

    def dec(self):
        self.decrement()
