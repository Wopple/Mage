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
import math

import box
import background
import incint
import cursor
import piece

from constants import *

class CharStation(object):
    def __init__(self, characters):

        sizeX = (CHAR_STATION_BORDER_SIZE * 2) + (PIECE_SIZE[0] * MAX_CHAR_ACTIVE) + (CHAR_STATION_PADDING * (MAX_CHAR_ACTIVE + 1))
        sizeY = (CHAR_STATION_BORDER_SIZE * 2) + (PIECE_SIZE[1]) + (CHAR_STATION_PADDING * 2)
        tempRect = pygame.Rect((0, 0), (sizeX, sizeY))
        self.box = box.Box(tempRect, CHAR_STATION_PATTERN, CHAR_STATION_PATTERN_SIZE,
                           CHAR_STATION_BORDER, CHAR_STATION_BORDER_SIZE)

        self.position = incint.IncInt(1, 1, MAX_CHAR_ACTIVE)
        self.cursor = cursor.Cursor(pygame.Rect((0, 0), PIECE_SIZE))

        self.pieces = []
        for x in range(len(characters)):
            self.pieces.append(piece.Piece(characters[x].piece.spriteSheet))

    def update(self, idleTicker, activeTicker):
        self.cursor.update(self.cursorPos(), PIECE_SIZE)

        for x in range(len(self.pieces)):
            self.pieces[x].location = self.miniPos(x)
            self.pieces[x].update(SPRITE_SHEET_IDLE, idleTicker.value())

    def draw(self, screen):
        self.box.draw(screen)
        self.cursor.draw(screen)
        for x in self.pieces:
            x.draw(screen)

    def moveLeft(self):
        self.position.dec()
        self.checkLeft()

    def moveRight(self):
        self.position.inc()
        self.checkRight()

    def checkLeft(self):
        if self.noneRemaining():
            fatalError()
        while self.noPiece():
            self.position.dec()

    def checkRight(self):
        if self.noneRemaining():
            fatalError()
        while self.noPiece():
            self.position.inc()

    def noPiece(self):
        if self.position.value > len(self.pieces):
            return True
        if not self.pieces[self.position.value - 1].visible:
            return True
        return False

    def cursorPos(self):
        return self.miniPos(self.position.value - 1)
        
    def miniPos(self, num):
        tempX = CHAR_STATION_BORDER_SIZE + CHAR_STATION_PADDING + ((PIECE_SIZE[0] + CHAR_STATION_PADDING) * num)
        tempY = CHAR_STATION_BORDER_SIZE + CHAR_STATION_PADDING

        tempX += self.box.rect.left
        tempY += self.box.rect.top

        return (tempX, tempY)

    def selectChar(self):
        self.pieces[self.position.value - 1].visible = False

    def noneRemaining(self):
        val = True
        for x in self.pieces:
            if x.visible:
                val = False
        return val

    def relightChar(self, num):
        self.pieces[num].visible = True
