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
import random

import model

from constants import *

import background
import incint
import cursor
import tileAura
import minimenu
import charStation
import soundSystem
import pieceTicker
import player
import cornerInfo
import ai

class Model(model.Model):
    def __init__(self, tiles, theChapter, activeChars):
        super(Model, self).__init__()
        self.background = background.Background(pygame.Rect((0, 0), SCREEN_SIZE), STARFIELD_PATTERN, STARFIELD_PATTERN_SIZE)
        self.idleTicker = pieceTicker.PieceTicker(IDLE_ANIM_SPEED)
        self.activeTicker = pieceTicker.PieceTicker(ACTIVE_ANIM_SPEED)
        self.tiles = tiles
        self.auras = []
        self.chapter = theChapter
        self.characters = activeChars
        self.xpGained = 300
        self.goForward = False
        self.createMap()
        self.cursor = cursor.Cursor(pygame.Rect( (0, 0), TILE_SIZE ) )
        self.cursorPos = [ incint.IncInt(0, 0, len(self.chapter.map[0])-1), incint.IncInt(0, 0, len(self.chapter.map)-1) ]
        self.scrollMap()
        self.setCursorPos(self.chapter.startingPos[0][0], self.chapter.startingPos[0][1])
        self.scrollMap()
        self.phase = 0
        self.menuOpen = False
        self.stationOpen = False
        self.movementOpen = False
        self.buildCharStation()
        self.buildMenu()
        self.buildCornerInfo()

        self.currentTarget = None
        self.movementArea = None

        self.refreshMovement(False, False)
        self.startingRefill()

        # Set the ai for the battle.
        self.enemy_ai = ai.null.NullAI(self)

    def goCheat(self, inCheat):
        if inCheat == 1:
            self.goForward = True
        elif inCheat == 2:
            if self.phase == 2:
                self.nextPhase()

    def advance(self):
        return self.goForward

    def update(self):
        self.idleTicker.update()
        self.activeTicker.update()
        self.cursor.update(self.genCursorPos(), TILE_SIZE )
        self.scrollMap()
        self.updateAuras()
        if self.stationOpen:
            self.charStation.update(self.idleTicker, self.activeTicker)
        self.updateActors()
        if self.phase == 2:
            self.enemy_ai.run()

    def updateActors(self):
        for y in range(len(self.field)):

            #Error checking for unbalanced grid
            if len(self.field[y]) != len(self.field[0]):
                fatalError()
            
            for x in range(len(self.field[0])):

                #Update Actor in square
                if len(self.field[y][x]) > 0:
                    self.field[y][x][0].piece.update(SPRITE_SHEET_IDLE, self.idleTicker.value())
                    self.field[y][x][0].piece.location = self.setPieceDrawLocation(x, y)

    def cursorMoveUp(self):
        if not self.stationOpen:
            if not(self.cursorPos[1].isMin()):
                newPos = self.cursorTuple()
                newPos = (newPos[0], newPos[1] - 1)
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[1].dec()
                    self.cursorMoveSuccess()

    def cursorMoveDown(self):
        if not self.stationOpen:
            if not(self.cursorPos[1].isMax()):
                newPos = self.cursorTuple()
                newPos = (newPos[0], newPos[1] + 1)
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[1].inc()
                    self.cursorMoveSuccess()

    def cursorMoveLeft(self):
        if not self.stationOpen:
            if not(self.cursorPos[0].isMin()):
                newPos = self.cursorTuple()
                newPos = (newPos[0] - 1, newPos[1])
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[0].dec()
                    self.cursorMoveSuccess()
        else:
            self.charStation.moveLeft()
            self.cursorMoveSuccess()

    def cursorMoveRight(self):
        if not self.stationOpen:
            if not(self.cursorPos[0].isMax()):
                newPos = self.cursorTuple()
                newPos = (newPos[0] + 1, newPos[1])
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[0].inc()
                    self.cursorMoveSuccess()
        else:
            self.charStation.moveRight()
            self.cursorMoveSuccess()

    def cursorMoveSuccess(self, playSound=True):
        self.updateCornerInfo()
        if playSound:
            self.cursor.playSound()

    def createMap(self):
        numY = len(self.chapter.map)
        numX = len(self.chapter.map[0])
        tempSizeY = (numY * TILE_SIZE[1]) + ((numY - 1) * MAP_OUTLINE_SIZE)
        tempSizeX = (numX * TILE_SIZE[0]) + ((numX - 1) * MAP_OUTLINE_SIZE)

        self.mapRect = pygame.Rect( (0, 0), (tempSizeX, tempSizeY))
        self.map = pygame.Surface((tempSizeX, tempSizeY))
        self.map.fill(MAP_OUTLINE_COLOR)
        self.field = []

        for y in range(numY):
            self.field.append([])
            for x in range (numX):
                self.field[y].append([])
                currTile = int(self.chapter.map[y][x])
                if (currTile < 0) or (currTile >= TILES_TOTAL):
                    currTile = 0
                tempTile = self.tiles[currTile]
                tempPos = self.findTilePos(x, y)
                self.map.blit(tempTile, tempPos)

        self.centerMap()

    def centerMap(self):
        if self.mapRect.width < SCREEN_SIZE[0]:
            self.mapRect.left = (SCREEN_SIZE[0] / 2) - (self.mapRect.width / 2)

        if self.mapRect.height < SCREEN_SIZE[1]:
            self.mapRect.top = (SCREEN_SIZE[1] / 2) - (self.mapRect.height / 2)

    def findTilePos(self, x, y):
        tempPosX = x * (TILE_SIZE[0] + MAP_OUTLINE_SIZE)
        tempPosY = y * (TILE_SIZE[1] + MAP_OUTLINE_SIZE)
        return (tempPosX, tempPosY)

    def updateAuras(self):
        for aura in self.auras:
            aura.update()

    def phaseAnimComplete(self):
        if self.phase == 0:
            self.auras.append(tileAura.TileAura(AURA_COLORS["yellow"], self.chapter.startingPos))

    def setCursorPos(self, inX, inY):
        self.cursorPos[0].value = inX
        self.cursorPos[1].value = inY

    def genCursorPos(self):
        tempPos = self.findTilePos(self.cursorPos[0].value, self.cursorPos[1].value)
        return (tempPos[0] + self.mapRect.left, tempPos[1] + self.mapRect.top)

    def scrollMap(self):
        while self.cursor.rect.right > SCREEN_SIZE[0]:
            self.mapRect.left -= 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )
        while self.cursor.rect.left < 0:
            self.mapRect.left += 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )
        while self.cursor.rect.bottom > SCREEN_SIZE[1]:
            self.mapRect.top -= 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )
        while self.cursor.rect.top < 0:
            self.mapRect.top += 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )

    def confirm(self):
        if self.stationOpen:
            self.charStation.selectChar()
            self.stationOpen = False
            self.menuOpen = False
            self.insertActor(self.characters[self.charStation.position.value - 1], self.cursorTuple())
            self.updateCornerInfo()
        elif self.menuOpen:
            if self.battleMenu.text() == "Place Character":
                self.stationOpen = True
                self.charStation.checkRight()
            elif self.battleMenu.text() == "Remove Character":
                self.returnCharToStation()
                self.removeActor(self.cursorTuple())
                self.menuOpen = False
            elif self.battleMenu.text() == "Begin Battle" or self.battleMenu.text() == "End Turn":
                self.menuOpen = False
                self.movementOpen = False
                if self.stationOpen:
                    fatalError()
                self.nextPhase()
            elif self.battleMenu.text() == "Spell":
                self.actionOutCharacter()
                self.menuOpen = False
            elif self.battleMenu.text() == "Weapon":
                self.actionOutCharacter()
                self.menuOpen = False
            elif self.battleMenu.text() == "Item":
                self.actionOutCharacter()
                self.menuOpen = False
        elif (self.movementOpen == False) and (self.overMovableCharacter()):
            self.movementOpen = True
            self.currentTarget = (self.cursorPos[0].value, self.cursorPos[1].value)
            self.movementArea = self.findMovementArea(self.currentTarget)
            self.auras.append(tileAura.TileAura(AURA_COLORS["blue"], self.movementArea))
        elif (self.movementOpen) and (not self.matchCursorLoc(self.currentTarget)):
            if self.validMoveSpot(self.cursorTuple()) and self.isInMovementArea(self.cursorTuple()):
                self.moveCharacter()
                self.closeMovement()
        else:
            self.buildMenu()
            if self.phase == 1:
                self.closeMovement()
            self.menuOpen = True
        soundSystem.playSound(1)

    def cancel(self):
        if self.stationOpen:
            self.stationOpen = False
        elif self.menuOpen:
            self.menuOpen = False
        elif self.movementOpen:
            self.movementOpen = False
            self.setCursorPos(self.currentTarget[0], self.currentTarget[1])
            self.currentTarget = None
            self.movementArea = None
            self.auras = []
        else:
            return
        soundSystem.playSound(2)

    def incMenu(self):
        self.battleMenu.inc()

    def decMenu(self):
        self.battleMenu.dec()

    def buildMenu(self):
        options = []
        
        if self.phase == 0:
            if self.overEmptySetupPoint() and not(self.charStation.noneRemaining()):
                options.append("Place Character")
            elif isinstance(self.getActorAtCursor(), player.Player):
                options.append("Remove Character")
                
            if self.charStation.noneRemaining():
                options.append("Begin Battle")

        if self.phase == 1:
            if isinstance(self.getActorAtCursor(), player.Player):
                if self.getActorAtCursor().piece.hasAction:
                    options.append("Spell")
                    options.append("Weapon")
                    options.append("Item")

        options.append("Options")
        options.append("Save and Quit")

        if self.phase != 0:
            options.append("End Turn")

        self.battleMenu = minimenu.MiniMenu(pygame.Rect((0, 0), BATTLE_MENU_ELEMENT_SIZE), options, BATTLE_MENU_FONT_SIZE,
                                            BATTLE_MENU_COLOR_ON, BATTLE_MENU_COLOR_OFF, BATTLE_MENU_COLOR_BG)

        self.battleMenu.rect.bottomleft = self.cursor.rect.topright
        if self.battleMenu.rect.top < 0:
            self.battleMenu.rect.top = self.cursor.rect.top
        if self.battleMenu.rect.right > SCREEN_SIZE[0]:
            self.battleMenu.rect.right = self.cursor.rect.left

    def overEmptySetupPoint(self):
        for point in self.chapter.startingPos:
            if self.cursorTuple() == point:
                if self.getActor(point) == False:
                    return True
                else:
                    return False
        return False

    def cursorTuple(self):
        return (self.cursorPos[0].value, self.cursorPos[1].value)

    def buildCharStation(self):
        self.charStation = charStation.CharStation(self.characters)
        self.charStation.box.center(ENTIRE_SCREEN, True, False)
        self.charStation.box.rect.bottom = SCREEN_SIZE[1]

    def nextPhase(self):
        if self.phase == 1:
            self.phase = 2
            self.refreshMovement(False, True)
        else:
            self.phase = 1
            self.refreshMovement(True, False)

        self.auras = []

    def insertActor(self, actor, pos):
        x = pos[0]
        y = pos[1]

        self.field[y][x] = []
        self.field[y][x].append(actor)

        for y2 in range(len(self.field)):
            for x2 in range(len(self.field[y2])):
                if (x2, y2) != (x, y):
                    if self.getActor((x2, y2)) == actor:
                        fatalError()

    def removeActor(self, pos):
        x = pos[0]
        y = pos[1]
        
        self.field[y][x] = []

    def getActor(self, pos):
        x = pos[0]
        y = pos[1]

        if len(self.field[y][x]) > 0:
            return self.field[y][x][0]
        else:
            return False

    def getActorAtCursor(self):
        return self.getActor(self.cursorTuple())

    def setPieceDrawLocation(self, x, y):
        tileLoc = self.findTilePos(x, y)

        finalX = tileLoc[0] + self.mapRect.left
        finalY = tileLoc[1] + TILE_SIZE[1] - PIECE_SIZE[1] + self.mapRect.top

        return (finalX, finalY)

    def returnCharToStation(self):
        tempChar = self.getActorAtCursor()
        success = False
        for x in range(len(self.characters)):
            if tempChar == self.characters[x]:
                self.charStation.relightChar(x)
                success = True
                break
        if not success:
            fatalError()

    def overMovableCharacter(self):
        x = self.cursorPos[0].value
        y = self.cursorPos[1].value
        if len(self.field[y][x]) > 0:
            if self.field[y][x][0].piece.canMove():
                return True
        else:
            return False

    def matchCursorLoc(self, inLoc):
        x = self.cursorPos[0].value
        y = self.cursorPos[1].value
        if (x, y) == inLoc:
            return True
        else:
            return False

    def matchMover(self, inLoc):
        if self.currentTarget is None:
            fatalError()

        x = self.currentTarget[0]
        y = self.currentTarget[1]
        
        if (x, y) == inLoc:
            return True
        else:
            return False
        

    def refreshMovement(self, pMove, eMove):
        for x in self.characters:
            x.piece.hasMove = pMove
            x.piece.hasAction = pMove

    def findMovementArea(self, moverLoc):
        area = []
        moveRemain = self.field[moverLoc[1]][moverLoc[0]][0].mov
        if moveRemain < 0:
            moveRemain = 0

        self.recurseMovement(area, moverLoc, moveRemain, '0')

        return area

    def recurseMovement(self, area, loc, moveRemain, prevDir):
        if moveRemain == 0:
            return

        if (loc[0] < 0) or (loc[1] < 0) or (loc[0] >= len(self.field[0])) or (loc[1] >= len(self.field)):
            return
        
        addUnique(area, loc)

        if prevDir != 'l':
            newLoc = (loc[0] - 1, loc[1])
            self.recurseMovement(area, newLoc, (moveRemain - 1), 'r')
        if prevDir != 'r':
            newLoc = (loc[0] + 1, loc[1])
            self.recurseMovement(area, newLoc, (moveRemain - 1), 'l')
        if prevDir != 'u':
            newLoc = (loc[0], loc[1] - 1)
            self.recurseMovement(area, newLoc, (moveRemain - 1), 'd')
        if prevDir != 'd':
            newLoc = (loc[0], loc[1] + 1)
            self.recurseMovement(area, newLoc, (moveRemain - 1), 'u')

    def isInMovementArea(self, inLoc):
        if not (self.movementArea is None):
            for x in self.movementArea:
                if x == inLoc:
                    return True
        return False

    def validMoveSpot(self, inLoc):
        x = inLoc[0]
        y = inLoc[1]

        if len(self.field[y][x]) != 0:
            return False

        return True

    def closeMovement(self):
        self.movementOpen = False
        self.currentTarget = None
        self.movementArea = None
        self.auras = []

    def moveCharacter(self):
        ox = self.currentTarget[0]
        oy = self.currentTarget[1]

        if len(self.field[oy][ox]) != 1:
            fatalError()

        tx = self.cursorPos[0].value
        ty = self.cursorPos[1].value

        if len(self.field[ty][tx]) != 0:
            fatalError()

        self.field[ty][tx].append(self.field[oy][ox][0])
        self.field[oy][ox] = []

        self.getActor((tx, ty)).piece.hasMove = False

    def actionOutCharacter(self):
        charLoc = self.cursorTuple()
        x = charLoc[0]
        y = charLoc[1]

        if len(self.field[y][x]) != 1:
            fatalError()

        self.field[y][x][0].piece.hasAction = False

    def startingRefill(self):
        for x in self.characters:
            x.piece.hpCurr = x.hp
            for m in range(3):
                x.piece.mpCurr[m] = int(x.mana[m] * STARTING_MANA_MULTIPLIER)

    def buildCornerInfo(self):
        self.cornerInfo = cornerInfo.CornerInfo()

    def updateCornerInfo(self):
        if (self.cursor.rect.left + (self.cursor.rect.width / 2)) < (SCREEN_SIZE[0] / 2):
            side = False
        else:
            side = True
        tempActor = self.getActorAtCursor()
        if tempActor == False:
            portrait = None
        else:
            portrait = tempActor.portrait
        
        self.cornerInfo.update(side, portrait)
