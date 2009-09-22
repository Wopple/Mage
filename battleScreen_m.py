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
import enemy
import battleText

class Model(model.Model):
    def __init__(self, tiles, theChapter, activeChars, enemyList):
        super(Model, self).__init__()

        random.seed()

        #Creates the background
        self.background = background.Background(pygame.Rect((0, 0), SCREEN_SIZE), STARFIELD_PATTERN, STARFIELD_PATTERN_SIZE)

        #Creates the tickers that control the piece sprite animations
        self.idleTicker = pieceTicker.PieceTicker(IDLE_ANIM_SPEED)
        self.activeTicker = pieceTicker.PieceTicker(ACTIVE_ANIM_SPEED)

        
        self.enemyList = enemyList
        self.tiles = tiles
        self.auras = []
        self.battleText = []
        self.chapter = theChapter
        self.characters = activeChars
        self.goForward = False

        #Sets the amount of xp gained during the battle to 300 - For debugging purposes only
        self.xpGained = 300

        #Creates the playfield
        self.createMap()

        #Places the chapter's starting enemies
        self.placeEnemies()

        #Creates the cursor object and cursor position variable
        self.cursor = cursor.Cursor(pygame.Rect( (0, 0), TILE_SIZE ) )
        self.cursorPos = [ incint.IncInt(0, 0, len(self.chapter.map[0])-1), incint.IncInt(0, 0, len(self.chapter.map)-1) ]

        #Sets the starting cursor position, and scrolls the map as necessary
        self.scrollMap()
        self.setCursorPos(self.chapter.startingPos[0][0], self.chapter.startingPos[0][1])
        self.scrollMap()

        self.phaseAnimDone = False
        self.phase = 0
        self.menuOpen = False
        self.stationOpen = False
        self.movementOpen = False
        self.cardsOpen = False
        self.targetOpen = False

        #Builds the sub-panels
        self.buildCharStation()
        self.buildMenu()
        self.buildCornerInfo()

        self.currentTarget = None
        self.movementArea = None

        #Removes the actions of player characters and enemies during the Setup Phase
        self.refreshPlayers(0, 0, 0)
        self.refreshEnemies(0, 0, 0)

        #Sets the starting HP and Mana of player characters
        self.startingRefill()

        # Set the ai for the battle.
        self.enemy_ai = ai.AI(self)

        # Plan to execute for the enemy.
        self.plan = None

    def goCheat(self, inCheat):
        if inCheat == 1:
            self.goForward = True

    def advance(self):
        return self.goForward

    def update(self):
        #Updates timers than keep track of piece animations
        #Seperate timers for Idle and Active animations
        self.idleTicker.update()
        self.activeTicker.update()

        #Updates cursor position
        self.cursor.update(self.genCursorPos(), TILE_SIZE )

        #Scrolls map if necessary, based on cursor position
        self.scrollMap()

        #Animates groups of blinking tiles
        self.updateAuras()

        #Updates "Character Station", which houses characters waiting to be
        #placed during the Setup Phase
        if self.stationOpen:
            self.charStation.update(self.idleTicker, self.activeTicker)

        #Updates all Actors on the Field
        self.updateActors()

        #Run AI
        if self.phase == 2 and self.phaseAnimDone:
            if self.plan is None:
                self.plan = self.enemy_ai.run()
            else:
                self.executePlan()
                self.plan = None  # Doing this hands control to the AI.

        #Update BattleText
        
        for BT in self.battleText:
            BT.update()
            if BT.count < BATTLE_TEXT_THRESHOLD:
                break
        tempList = []
        for BT in self.battleText:
            if not BT.remove:
                tempList.append(BT)
        self.battleText = tempList

    def updateActors(self):
        for y in range(len(self.field)):

            #Error checking for unbalanced grid
            if len(self.field[y]) != len(self.field[0]):
                fatalError("Grid was unbalanced")
            
            for x in range(len(self.field[0])):

                #Update Actor in square
                if len(self.field[y][x]) > 0:
                    if self.field[y][x][0].piece.group == 0:
                        tickerVal = self.idleTicker.value()
                    else:
                        tickerVal = self.activeTicker.value()
                    self.field[y][x][0].piece.update(-1, tickerVal)
                    self.field[y][x][0].piece.location = self.setPieceDrawLocation(x, y)

    def cursorMoveUp(self):
        #Cursor movement input handler
        if not self.stationOpen:
            if not(self.cursorPos[1].isMin()):
                newPos = self.cursorTuple()
                newPos = (newPos[0], newPos[1] - 1)
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[1].dec()
                    self.cursorMoveSuccess()

    def cursorMoveDown(self):
        #Cursor movement input handler
        if not self.stationOpen:
            if not(self.cursorPos[1].isMax()):
                newPos = self.cursorTuple()
                newPos = (newPos[0], newPos[1] + 1)
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[1].inc()
                    self.cursorMoveSuccess()

    def cursorMoveLeft(self):
        #Cursor movement input handler
        if not self.stationOpen:
            if not(self.cursorPos[0].isMin()):
                newPos = self.cursorTuple()
                newPos = (newPos[0] - 1, newPos[1])
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[0].dec()
                    self.cursorMoveSuccess()
        else:
            #If navigating the Character Station for Setup Phase piece selection
            self.charStation.moveLeft()
            self.cursorMoveSuccess()

    def cursorMoveRight(self):
        #Cursor movement input handler
        if not self.stationOpen:
            if not(self.cursorPos[0].isMax()):
                newPos = self.cursorTuple()
                newPos = (newPos[0] + 1, newPos[1])
                if (not self.movementOpen) or (self.movementOpen and self.isInMovementArea(newPos)):
                    self.cursorPos[0].inc()
                    self.cursorMoveSuccess()
        else:
            #If navigating the Character Station for Setup Phase piece selection
            self.charStation.moveRight()
            self.cursorMoveSuccess()

    def cursorMoveSuccess(self, playSound=True):
        #Called when a cursor's position changes
        self.updateCornerInfo()

        if not self.movementOpen:
            self.updateActiveAnimation()
        
        if playSound:
            self.cursor.playSound()

    def createMap(self):
        #Creates playfield on init
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
        #Centers map vertically and/or horizontally if a dimension is smaller than
        #the screen size
        if self.mapRect.width < SCREEN_SIZE[0]:
            self.mapRect.left = (SCREEN_SIZE[0] / 2) - (self.mapRect.width / 2)

        if self.mapRect.height < SCREEN_SIZE[1]:
            self.mapRect.top = (SCREEN_SIZE[1] / 2) - (self.mapRect.height / 2)

    def findTilePos(self, x, y):
        #Calculation for finding a tile's draw position
        tempPosX = x * (TILE_SIZE[0] + MAP_OUTLINE_SIZE)
        tempPosY = y * (TILE_SIZE[1] + MAP_OUTLINE_SIZE)
        return (tempPosX, tempPosY)

    def updateAuras(self):
        #Updates glowing tiles
        for aura in self.auras:
            aura.update()

    def phaseAnimComplete(self):
        #Called when the Phase Change Animation has finished
        if self.phase == 0:
            self.auras.append(tileAura.TileAura(AURA_COLORS["yellow"], self.chapter.startingPos))
        elif self.phase == 1:
            self.refreshPlayers(1, 1, 1)
        elif self.phase == 2:
            #Runs enemy AI
            self.refreshEnemies(1, 1, 1)

        self.phaseAnimDone = True
        self.updateActiveAnimation()
        self.updateCornerInfo()

    def setCursorPos(self, inX, inY):
        #Sets the cursor position to a given X and Y value
        self.cursorPos[0].value = inX
        self.cursorPos[1].value = inY

    def genCursorPos(self):
        #Returns drawing position of cursor
        tempPos = self.findTilePos(self.cursorPos[0].value, self.cursorPos[1].value)
        return (tempPos[0] + self.mapRect.left, tempPos[1] + self.mapRect.top)

    def scrollMap(self):
        #Scrolls the map relative to the screen in order to keep the cursor
        #on screen
        while self.cursor.rect.right > SCREEN_SIZE[0]:
            self.mapRect.left -= 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )
        while self.cursor.rect.left < 0:
            self.mapRect.left += 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )
        while self.cursor.rect.bottom > SCREEN_SIZE[1]:
            self.mapRect.top -= 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )
        while self.cursor.rect.top < (0 + PIECE_SIZE[0] + SYMBOL_SIZE_LARGE + SYMBOL_ABOVE):
            self.mapRect.top += 1
            self.cursor.update(self.genCursorPos(), TILE_SIZE )

    def confirm(self):
        #Occurs when the Enter button is pressed
        
        if self.stationOpen:
            #When Character Station is open
            self.charStation.selectChar()
            self.stationOpen = False
            self.menuOpen = False
            self.insertActor(self.characters[self.charStation.position.value - 1], self.cursorTuple())
            
        elif self.menuOpen:
            #When Menu is open
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
                    fatalError("Turn was ended while character station was open")
                self.nextPhase()
            elif self.battleMenu.text() == "Spell":
                self.cardsOpen = True
                self.menuOpen = False
            elif self.battleMenu.text() == "Weapon":
                self.performAction(-1)
                self.menuOpen = False
            elif self.battleMenu.text() == "Item":
                self.actionOutCharacter()
                self.menuOpen = False

        elif (self.targetOpen):
            if self.cursorTuple() in self.movementArea:
                self.targetOpen = False
                self.resolveAction()
                self.currentTarget = None
                self.currentAbility = None
                self.movementArea = None
                self.auras = []
                
        elif (self.movementOpen == False) and (self.overMovableCharacter()):
            #When over a selectable character
            self.movementOpen = True
            self.currentTarget = (self.cursorPos[0].value, self.cursorPos[1].value)
            self.movementArea = self.findMovementArea(self.currentTarget, "P")
            self.auras.append(tileAura.TileAura(AURA_COLORS["blue"], self.movementArea))
            
        elif (self.movementOpen) and (not self.matchCursorLoc(self.currentTarget)):
            #When directing movement and not over the moving character
            if self.validMoveSpot(self.cursorTuple()) and self.isInMovementArea(self.cursorTuple()):
                self.moveCharacter()
                self.closeMovement()    
        else:
            #Other circumstances - Build Menu
            self.buildMenu()
            if self.phase == 1:
                self.closeMovement()
            self.menuOpen = True
            
        soundSystem.playSound(1)
        if not self.movementOpen:
            self.updateActiveAnimation()
        self.updateCornerInfo()

    def cancel(self):
        #Occurs when the Cancel button is pressed
        
        if self.stationOpen:
            #When Character Station is open
            self.stationOpen = False

        elif self.menuOpen:
            #When Menu is open
            self.menuOpen = False

        elif self.targetOpen:
            #When choosing a target
            self.targetOpen = False
            self.setCursorPos(self.currentTarget[0], self.currentTarget[1])
            self.currentTarget = None
            self.movementArea = None
            self.auras = []
            
        elif self.movementOpen:
            #When directing movement
            self.movementOpen = False
            self.setCursorPos(self.currentTarget[0], self.currentTarget[1])
            self.currentTarget = None
            self.currentAbility = None
            self.movementArea = None
            self.auras = []
            
        else:
            #Other citsumtances
            return
        soundSystem.playSound(2)

    def incMenu(self):
        #Moves down on the menu
        self.battleMenu.inc()

    def decMenu(self):
        #Moves up on the menu
        self.battleMenu.dec()

    def buildMenu(self):
        #Builds the battle option menu
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
        #Returns whether or not the cursor is over an
        #empty setup spot
        for point in self.chapter.startingPos:
            if self.cursorTuple() == point:
                if self.getActor(point) == False:
                    return True
                else:
                    return False
        return False

    def cursorTuple(self):
        #Returns the cursor's numerical position as a tuple
        return (self.cursorPos[0].value, self.cursorPos[1].value)

    def buildCharStation(self):
        #Sets up the Character Station
        self.charStation = charStation.CharStation(self.characters)
        self.charStation.box.center(ENTIRE_SCREEN, True, False)
        self.charStation.box.rect.bottom = SCREEN_SIZE[1]

    def nextPhase(self):
        #Advances to the next phase
        if self.phase == 1:
            self.phase = 2
            self.refreshPlayers(0, 0, 2)
            self.enemy_ai.reset()
        else:
            self.phase = 1
            self.refreshEnemies(0, 0, 2)

        self.phaseAnimDone = False
        self.auras = []

    def insertActor(self, actor, pos):
        #Inserts an actor into a certain square.  Causes an error
        #If the space is not empty
        x = pos[0]
        y = pos[1]

        try:
            if len(self.field[y][x]) > 0:
                fatalError("Tried to insert actor into non-empty space")
        except:
            fatalError("Grid was improper during insert")

        self.field[y][x] = []
        self.field[y][x].append(actor)

        for y2 in range(len(self.field)):
            for x2 in range(len(self.field[y2])):
                if (x2, y2) != (x, y):
                    if self.getActor((x2, y2)) == actor:
                        fatalError("Multiple copies of same actor on grid")

    def removeActor(self, pos):
        #Deletes an actor at a certain square
        
        x = pos[0]
        y = pos[1]

        try:
            self.field[y][x] = []
        except:
            fatalError("Grid was improper during removal")

    def getActor(self, pos):
        #Returns an actor at a given square, or False if none is present
        
        x = pos[0]
        y = pos[1]

        if len(self.field[y][x]) > 0:
            return self.field[y][x][0]
        else:
            return False

    def getActorAtCursor(self):
        #Calls getActor on the square that the cursor is on
        
        return self.getActor(self.cursorTuple())

    def setPieceDrawLocation(self, x, y):
        #Calculates the drawing position of a piece
        
        tileLoc = self.findTilePos(x, y)

        finalX = tileLoc[0] + (TILE_SIZE[0] / 2) - (PIECE_SIZE[0] / 2) + self.mapRect.left
        finalY = tileLoc[1] + TILE_SIZE[1] - PIECE_SIZE[1] + self.mapRect.top

        return (finalX, finalY)

    def returnCharToStation(self):
        #Removes a character from the map and returns them to
        #the Character Station during the Setup Phase
        
        tempChar = self.getActorAtCursor()
        success = False
        for x in range(len(self.characters)):
            if tempChar == self.characters[x]:
                self.charStation.relightChar(x)
                success = True
                break
        if not success:
            fatalError("Character was not returned to station successfully")

    def overMovableCharacter(self):
        #Returns whether the cursor is over an actor that the player can move
        
        x = self.cursorPos[0].value
        y = self.cursorPos[1].value
        if len(self.field[y][x]) > 0:
            if self.field[y][x][0].piece.canMove():
                return True
        else:
            return False

    def matchCursorLoc(self, inLoc):
        #Returns whether the given location is the cursor's current location
        
        x = self.cursorPos[0].value
        y = self.cursorPos[1].value
        if (x, y) == inLoc:
            return True
        else:
            return False

    def matchMover(self, inLoc):
        #Returns whether the given location is the location of the current
        #moving character.  Causes an error if there is no moving character.
        
        if self.currentTarget is None:
            fatalError("Tried to check non-existant target")

        x = self.currentTarget[0]
        y = self.currentTarget[1]
        
        if (x, y) == inLoc:
            return True
        else:
            return False

    def refreshPlayers(self, move, action, spike):
        #0 = Turn off, 1 = Turn on, 2 = Ignore
        for x in self.characters:
            
            if move == 1:
                x.piece.hasMove = True
            elif move == 0:
                x.piece.hasMove = False

            if action == 1:
                x.piece.hasAction = True
            elif action == 0:
                x.piece.hasAction = False

            if spike == 1:
                x.piece.hasSpike = True
            elif spike == 0:
                x.piece.hasSpike = False

    def refreshEnemies(self, move, action, spike):
        #0 = Turn off, 1 = Turn on, 2 = Ignore
        for x in self.enemies:
            
            if move == 1:
                x.piece.hasMove = True
            elif move == 0:
                x.piece.hasMove = False

            if action == 1:
                x.piece.hasAction = True
            elif action == 0:
                x.piece.hasAction = False

            if spike == 1:
                x.piece.hasSpike = True
            elif spike == 0:
                x.piece.hasSpike = False

    def findMovementArea(self, moverLoc, moverType):
        if not (moverType == "P" or moverType == "E"):
            fatalError()
        moverType += "M"

        path = self.mapPathMaker(moverLoc[0], moverLoc[1], self.field[moverLoc[1]][moverLoc[0]][0].mov, moverType)

        if moverType[0] == "E":
            path2 = []
            for i in path:
                if self.validMoveSpot(i):
                    path2.append(i)
            return path2
        else:
            return path

    def isInMovementArea(self, inLoc):
        #Determines if the given location is within the current
        #piece movement area
        
        if not (self.movementArea is None):
            for x in self.movementArea:
                if x == inLoc:
                    return True
        return False

    def validMoveSpot(self, inLoc):
        #Determines if the given location is a valid position to
        #move to, excluding whether it is within the actual movement
        #area range (see isInMovementArea)

        if not self.isWithinMap(inLoc):
            return False
        
        x = inLoc[0]
        y = inLoc[1]

        if len(self.field[y][x]) != 0:
            return False

        return True

    def validMoveThrough(self, inLoc, moverType):
        #Determines if the given location is a valid position to
        #move through, or if it blocks movement.

        if not self.isWithinMap(inLoc):
            return False

        if moverType[0] == "P":
            typePlayer = True
        elif moverType[0] == "E":
            typePlayer = False
        else:
            fatalError("Incorrect mover type")

        if moverType[1] == "M":
            typeMovement = True
        elif moverType[1] == "A":
            typeMovement = False
        else:
            fatalError("Incorrect mover type")

        x = inLoc[0]
        y = inLoc[1]

        if len(self.field[y][x]) != 0:
            if isinstance(self.field[y][x][0], enemy.Enemy):
                if typePlayer and typeMovement:
                    return False
            if isinstance(self.field[y][x][0], player.Player):
                if not typePlayer and typeMovement:
                    return False

        return True

    def isWithinMap(self, inLoc):
        #Determines whether a square is within the bounds of the map

        x = inLoc[0]
        y = inLoc[1]

        if (x >= 0) and (x < len(self.field[0])) and (y >= 0) and (y < len(self.field)):
            return True
        else:
            return False

    def closeMovement(self):
        #Cancels movement selection
        
        self.movementOpen = False
        self.currentTarget = None
        self.movementArea = None
        self.auras = []

    def moveCharacter(self):
        #Moves the character found at the Current Target location to the
        #Cursor's current location.  Causes an error if the target character's
        #Square is empty, or if the destination square is not empty.
        
        ox = self.currentTarget[0]
        oy = self.currentTarget[1]

        if len(self.field[oy][ox]) != 1:
            fatalError("Movement origin was empty")

        tx = self.cursorPos[0].value
        ty = self.cursorPos[1].value

        if len(self.field[ty][tx]) != 0:
            fatalError("Movement destination was not empty")

        self.field[ty][tx].append(self.field[oy][ox][0])
        self.field[oy][ox] = []

        self.getActor((tx, ty)).piece.hasMove = False

    def actionOutCharacter(self, inLoc=None):
        #Removes the Primary Action from the character at a given position.
        #The default is the cursor's position.  Causes an error if there is
        #no character at this position

        if inLoc is None:
            charLoc=self.cursorTuple()
        else:
            charLoc=inLoc
        
        x = charLoc[0]
        y = charLoc[1]

        if len(self.field[y][x]) != 1:
            fatalError("Performed character actions on empty square")

        self.field[y][x][0].piece.hasAction = False

    def startingRefill(self):
        #Sets starting HP and Mana for all player characters
        
        for x in self.characters:
            x.piece.hpCurr = x.hp
            for m in range(3):
                x.piece.mpCurr[m] = int(x.mana[m] * STARTING_MANA_MULTIPLIER)

    def buildCornerInfo(self):
        #Builds the Corner Info panel
        
        self.cornerInfo = cornerInfo.CornerInfo()

    def updateCornerInfo(self):
        #Updates the Corner Info panel

        #Places the panel on the opposite horizontal side as the cursor
        if (self.cursor.rect.left + (self.cursor.rect.width / 2)) < (SCREEN_SIZE[0] / 2):
            side = False
        else:
            side = True

        tempActor = self.getActorAtCursor()
        
        if tempActor == False:
            portrait = None
            temp_hp = 0
            temp_hpMax = 0
            temp_mage = False
        else:
            portrait = tempActor.portrait
            temp_hp = tempActor.piece.hpCurr
            temp_hpMax = tempActor.hp
            temp_mage = tempActor.isMage

        if temp_mage:
            temp_mana = tempActor.piece.mpCurr
            temp_manaMax = tempActor.maxMana
        else:
            temp_mana = (0, 0, 0)
            temp_manaMax = (0, 0, 0)
        
        self.cornerInfo.update(side, portrait, temp_hp, temp_hpMax, temp_mana, temp_manaMax, temp_mage)

    def placeEnemies(self):
        #Places the starting enemies for the chapter
        
        for x in self.chapter.obstacles:
            if x[0] == "E":
                tempEnemy = self.enemyList[x[1]]
                newEnemy = enemy.Enemy(tempEnemy.name, tempEnemy.getStatsOrig(), tempEnemy.gift,
                                       tempEnemy.isMage, tempEnemy.abilities)
                newEnemy.piece.changeSpriteSheet(tempEnemy.piece.spriteSheet)
                self.insertActor(newEnemy, (x[2], x[3]))

    def updateActiveAnimation(self):

        for x in self.players:
            x.piece.group = 0

        if not self.currentTarget is None:
            temp = self.getActor(self.currentTarget)
        else:
            temp = self.getActorAtCursor()
        if temp != False and isinstance(temp, player.Player):
            if temp.piece.hasMove or temp.piece.hasAction:
                if temp.piece.group == 0:
                    temp.piece.group = 1
                    self.activeTicker.reset()

    def getAbilitiesFromCursorActor(self):
        temp = self.getActorAtCursor()
        if temp == False:
            fatalError("Attempted to get abilities of empty square")

        return temp.abilities

    # Performs the action from the current plan.
    def executePlan(self):
        for action in self.plan.actions:
            if action.type == ai.plan.MOVE:
                temp1 = self.currentTarget
                temp2 = self.cursorPos[0].value
                temp3 = self.cursorPos[1].value
                self.currentTarget = self.locationOf(self.plan.character)
                self.cursorPos[0].value = action.destination[0]
                self.cursorPos[1].value = action.destination[1]
                self.moveCharacter()
                self.currentTarget = temp1
                self.cursorPos[0].value = temp2
                self.cursorPos[1].value = temp3
            elif action.type == ai.plan.ATTACK:
                temp1 = self.cursorPos[0].value
                temp2 = self.cursorPos[1].value
                location = self.locationOf(self.plan.character)[0]
                self.cursorPos[0].value = location[0]
                self.cursorPos[1].value = location[1]
                self.actionOutCharacter()
                self.cursorPos[0].value = temp1
                self.cursorPos[1].value = temp2

    # Returns the location of the given character.
    # None is returned if the character is not in the field.
    def locationOf(self, character):
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if self.field[y][x] != []:
                    if self.field[y][x][0] is character:
                        return (x, y)
        return None

    def getAbilitiesFromCursorActor(self):
        temp = self.getActorAtCursor()
        if temp == False:
            fatalError()

        return temp.abilities

    #Causes the actor at the cursor to perform an ability.
    #Performs the first half, retrieving the ability and
    #opening the targetting system.
    #The ability performed is the index of the ability in their
    #Abilities variable, or -1 for the standard attack of players.
    #Causes errors if no actor is at the cursor, or if an
    #improper argument is given.
    def performAction(self, actionNum):

        charLoc = self.cursorTuple()
        x = charLoc[0]
        y = charLoc[1]

        if len(self.field[y][x]) != 1:
            fatalError("Performed character actions on empty square")

        currChar = self.field[y][x][0]

        if (actionNum >= len(currChar.abilities)) and (actionNum != -1):
            fatalError("Improper action argument")

        if (actionNum == -1) and not isinstance(currChar, player.Player):
            fatalError("Attempted to refer to standard attack of enemy")

        #Gets the correct ability
        if actionNum == -1:
            currAbility = currChar.attackAbility
        else:
            currAbility = currChar.abilities[actionNum]

        #Opens targetting system
        self.currentTarget = self.cursorTuple()
        self.currentAbility = currAbility
        self.targetOpen = True
        self.movementArea = self.findTargetArea(currAbility)
        self.auras.append(tileAura.TileAura(AURA_COLORS["red"], self.movementArea))



    #Performs the finalized action, with the user of
    #the ability being stored in the target, the selected
    #square for the ability to be performed at being at the
    #cursor position, and the selected ability being stored
    #in the currAbility variable.  Causes errors if these
    #conditions are not valid.
    def resolveAction(self):

        if self.currentAbility is None:
            fatalError()

        currAbility = self.currentAbility

        if self.currentTarget is None:
            fatalError()

        charOffense = self.getActor(self.currentTarget)

        if charOffense == False:
            fatalError()

        charDefense = self.getActorAtCursor()

        tempPos = self.genCursorPos()
        tempBTLoc = ( (tempPos[0] + (TILE_SIZE[0] / 2) - (BATTLE_TEXT_SIZE[0] / 2)),
                      tempPos[1] - BATTLE_TEXT_SIZE[1] - BATTLE_TEXT_ABOVE)
        if charDefense == False:
            print "Used " + currAbility.name + " on empty square " + str(self.cursorTuple())
            tempBT = battleText.BattleText("No Target", FONT_COLORS["black"], tempBTLoc)
        else:
            print "Used " + currAbility.name + " on " + charDefense.name + " at " + str(self.cursorTuple())
            hitChance = self.calculateHitChance(charOffense, charDefense, currAbility)
            print str(hitChance) + "% chance to hit"
            if self.rollForHit(hitChance):
                damage = self.calculateDamage(charOffense, charDefense, currAbility)
                print "Hit for " + str(damage) + " damage"
                tempBT = battleText.BattleText(str(damage), FONT_COLORS["red"], tempBTLoc)
                charDefense.takeDamage(damage)
            else:
                print "Miss"
                tempBT = battleText.BattleText("Miss", FONT_COLORS["black"], tempBTLoc)

        #Add BattleText
        self.battleText.append(tempBT)
        if charDefense.piece.hpCurr <= 0:
            self.battleText.append(battleText.BattleText("Defeated", FONT_COLORS["black"], tempBTLoc))
        
        #Uses up target's limited amount of actions
        self.actionOutCharacter(self.currentTarget)

        #Check Field for Defeated Pieces
        self.checkForDefeated()

        #Update CornerInfo
        self.updateCornerInfo()

    def findTargetArea(self, currAbility):
        areaMax = self.mapPathMaker(self.cursorPos[0].value, self.cursorPos[1].value, currAbility.maxRange, "PA")
        areaMin = self.mapPathMaker(self.cursorPos[0].value, self.cursorPos[1].value, currAbility.minRange - 1, "PA")

        for i in range(len(areaMax)):
            for j in range(len(areaMin)):
                if areaMax[i] == areaMin[j]:
                    areaMax[i] = "REMOVE"
                    
        finalArea = []
        for i in areaMax:
            if i != "REMOVE":
                finalArea.append(i)

        return finalArea

    def mapPathMaker(self, inX, inY, moveRemain, moverType):

        numY = len(self.chapter.map)
        numX = len(self.chapter.map[0])

        area = []

        for y in range(numY):
            area.append([])
            for x in range(numX):
                area[y].append(0)

        if moveRemain == -1:
            return area

        if moveRemain < 0:
            moveRemain = 0

        area[inY][inX] = 2
        
        while moveRemain >= 0:

            #Search for '1' squares
            for y in range(len(self.field)):
                for x in range(len(self.field[0])):
                    if area[y][x] == 1:
                        
                    #Check all '1's for validity.  Valid squares become a '2',
                    #Invalid squares become a '0'.
                        if self.validMoveThrough((x, y), moverType):
                            area[y][x] = 2

            #Search for '2' squares
            for y in range(len(self.field)):
                for x in range(len(self.field[0])):
                    if area[y][x] == 2:
                        
                    #All squares around each '2' becomes a '1' for checking,
                    #and the '2' then becomes a finalized '3'
                        area[y][x] = 3

                        for (tempX, tempY) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                            if self.isWithinMap((tempX, tempY)):
                                if area[tempY][tempX] == 0:
                                    area[tempY][tempX] = 1
                            
            moveRemain -= 1

        #Move all finalized '3' squares into a list
        finalList = []
        for y in range(len(self.field)):
            for x in range(len(self.field[0])):
                if area[y][x] == 3:
                    finalList.append((x, y))
                    
        return finalList

    def calculateDamage(self, attacker, defender, currAbility):
        if currAbility.statOff == "P":
            offense = attacker.stats[0]
        elif currAbility.statOff == "M":
            offense = attacker.stats[1]
        else:
            fatalError("Ability has improper offensive stat reference")

        if currAbility.statDef == "P":
            defense = defender.stats[3]
        elif currAbility.statDef == "M":
            defense = defender.stats[4]
        elif currAbility.statDef == "L":
            if defender.stats[3] < defender.stats[4]:
                defense = defender.stats[3]
            else:
                defense = defender.stats[4]
        else:
            fatalError("Ability has improper defensive stat reference")

        total = int((offense - defense + BASE_DAMAGE) * currAbility.damage)

        if total < 0:
            total = 0
        if total > DAMAGE_CAP:
            total = DAMAGE_CAP

        print "Damage Formula:  " + str(offense) + " offense - " + str(defense) + " defense + " + str(BASE_DAMAGE) + " BASE = " + str(total)

        return total

    def calculateHitChance(self, attacker, defender, currAbility):
        offense = attacker.stats[2]
        defense = defender.stats[5]

        total = int((((offense - defense) * HIT_CHANCE_INCREMENT) + BASE_HIT_CHANCE) * currAbility.accuracy)

        if total < 0:
            total = 0
        if total > 100:
            total = 100

        print "Accuracy Formula:  ((" + str(offense) + " offense - " + str(defense) + " defense) * " + str(HIT_CHANCE_INCREMENT) + ") + " + str(BASE_HIT_CHANCE) + " BASE = " + str(total)

        return total

    def rollForHit(self, hitChance):
        dice = random.randint(1, 100)
        return (dice <= hitChance)

    def checkForDefeated(self):
        print "Checking For Defeated Pieces"
        for y in range(len(self.field)):
            for x in range(len(self.field[y])):
                if len(self.field[y][x]) > 0:
                    if self.field[y][x][0].piece.hpCurr <= 0:
                        self.field[y][x] = []
        
    # Property for the list of players in the battle.
    def _players(self):
        players = []

        for i in self.field:
            for j in i:
                if len(j) > 0 and isinstance(j[0], player.Player):
                    players.append(j[0])

        return players

    # Property for the list of enemies in the battle.
    def _enemies(self):
        enemies = []

        for i in self.field:
            for j in i:
                if len(j) > 0:
                    if len(j) > 0 and isinstance(j[0], enemy.Enemy):
                        enemies.append(j[0])

        return enemies

    players = property(_players)
    enemies = property(_enemies)
