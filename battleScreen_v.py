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

import view

import player
import enemy

from constants import *

SYMBOL_ON = None
SYMBOL_OFF = None


class View(view.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

        global SYMBOL_ON
        global SYMBOL_OFF
        if (SYMBOL_ON is None) or (SYMBOL_OFF is None):
            SYMBOL_ON = []
            SYMBOL_OFF = []

            for x in range(3):
                fileName = SYMBOL_FILE + str(x) + SYMBOL_FILE_ON + SYMBOL_FILE_EXT
                fileName = os.path.join(GRAPHICS_PATH, fileName)
                SYMBOL_ON.append(pygame.image.load(fileName).convert_alpha())
                fileName = SYMBOL_FILE + str(x) + SYMBOL_FILE_OFF + SYMBOL_FILE_EXT
                fileName = os.path.join(GRAPHICS_PATH, fileName)
                SYMBOL_OFF.append(pygame.image.load(fileName).convert_alpha())

    def update(self, tickClock=True):
        self.model.background.draw(self.screen)
        self.screen.blit(self.model.map, self.model.mapRect.topleft)
        self.drawAuras()
        self.drawActors()
        self.model.cursor.draw(self.screen)
        for i in self.model.battleText:
            i.draw(self.screen)
        if self.model.menuOpen:
            self.model.battleMenu.draw(self.screen)
        if self.model.stationOpen:
            self.model.charStation.draw(self.screen)
        self.model.cornerInfo.draw(self.screen)
        
        if tickClock:
            pygame.display.flip()

    def drawAuras(self):
        for aura in self.model.auras:
            for tile in aura.tiles:
                tempPos = self.model.findTilePos(tile[0], tile[1])
                self.screen.blit(aura.aura, (tempPos[0] + self.model.mapRect.left, tempPos[1] + self.model.mapRect.top) )

    def drawActors(self):
        for y in range(len(self.model.field)):
            for x in range(len(self.model.field[0])):
                if len(self.model.field[y][x]) > 0:
                    self.model.field[y][x][0].piece.draw(self.screen)
                    if self.model.phase != 0:
                        if self.model.phase == 1:
                            if self.model.movementOpen:
                                matchCurr = self.model.matchMover((x, y))
                            else:
                                matchCurr = self.model.matchCursorLoc((x, y))
                        else:
                            matchCurr = False

                        if isinstance(self.model.field[y][x][0], player.Player):
                            tempPiece = self.model.field[y][x][0].piece
                            self.drawSymbol(tempPiece.hasMove, tempPiece.hasAction, tempPiece.hasSpike, tempPiece.location, matchCurr, self.screen)

    def drawSymbol(self, inMove, inAction, inSpike, inLoc, isCurrChar, screen):
        global SYMBOL_ON
        global SYMBOL_OFF

        if isCurrChar and self.model.phaseAnimDone:
            symbolSize = (SYMBOL_SIZE_LARGE, SYMBOL_SIZE_LARGE)
        else:
            symbolSize = (SYMBOL_SIZE_SMALL, SYMBOL_SIZE_SMALL)
        symbolRect = pygame.Rect( (0,0), symbolSize )
        symbolRect.bottom = inLoc[1] + SYMBOL_ABOVE
        symbolRect.left = (PIECE_SIZE[0] / 2) - (symbolSize[0] / 2) + inLoc[0]

        truthTable = []
        truthTable = [inMove, inAction, inSpike]

        for i in range(len(truthTable)):
            if truthTable[i]:
                tempImage = SYMBOL_ON[i]
            else:
                tempImage = SYMBOL_OFF[i]

            
            tempSurface = pygame.Surface(symbolSize)
            tempSurface.fill(BLACK)
            pygame.transform.scale(tempImage, symbolSize, tempSurface)
            tempSurface.set_colorkey(BLACK)
            screen.blit(tempSurface, symbolRect.topleft)
