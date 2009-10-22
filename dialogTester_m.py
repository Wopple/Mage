#!/usr/bin/env python

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
import os
import sys
import pygame

import model

import dialogSystem

from constants import *

class Model(model.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.goForward = False
        self.ds = dialogSystem.DialogSystem(self.loadTestString(), 3)

    def confirm(self):
        self.goForward = True

    def cancel(self):
        pass

    def advance(self):
        return self.goForward

    def back(self):
        return False

    def update(self):
        self.ds.update()

    def loadTestString(self):
        try:
            textFile = open("testconvo.dat")
            textArray = textFile.readlines()
            textFile.close()
        except:
            textArray = ["BlahdeBlahdeBlah.  I like to Great Aether people.  In the face!  Yoooooooo!  Making a really long piece of text here.  Look at meeee!!  Still talking here.  Ok I'm good now.",
                         "Yo momma is fat.  Blahhhhhhhh."]

        for x in range(len(textArray)):
            textArray[x] = textArray[x].strip()

        print textArray

        return textArray
