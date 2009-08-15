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
import random
import math

import model

import menu
import player
import chapter
import enemy
import ability

from constants import *

class Model(model.Model):
    def __init__(self, inPath):
        super(Model, self).__init__()

        self.success = True
        self.confirmed = False
        self.players = []
        self.enemies = []
        self.chapters = []
        self.abilities = []
        self.xp = 0
        self.cheatery = False

        self.missionPath = os.path.join(MISSION_PATH, inPath)

        try:
            if self.success:
                self.checkerMessage("Campaign")
                self.success = self.checkMissionFile()
            if self.success:
                self.success = self.checkTileset()
            if self.success:
                self.checkerMessage("Abilities")
                self.success = self.checkAbilities()
            if self.success:
                self.checkerMessage("Player Characters")
                self.success = self.checkCharacters()
            if self.success:
                self.checkerMessage("Enemies")
                self.success = self.checkEnemies()
            if self.success:
                self.checkerMessage("Chapters")
                self.success = self.checkChapters()
        except:
            self.success = False
            
        self.createSuccessMenu()


    def checkMissionFile(self):
        tempPath = os.path.join(self.missionPath, MISSION_FILE)

        self.checkerMessage("Campaign File", 1)
        if not(os.path.exists(tempPath)):
            return False

        missionFile = open(tempPath)
        tempName = missionFile.readline()
        tempSize = len(tempName)
        missionFile.close()
        if (tempSize > 0) and (tempSize <= MISSION_MAX_NAME):
            self.missionName = tempName
        else:
            return False

        return True

    def checkTileset(self):
        tempPath = os.path.join(self.missionPath, TILESET_FILE)

        self.checkerMessage("Tileset", 1)
        if not(os.path.exists(tempPath)):
            return False

        tileFile = pygame.image.load(tempPath).convert_alpha()

        self.tiles = []

        numOfRows = int(math.ceil(float(TILES_TOTAL) / float(TILES_PER_ROW)))
        for y in range(numOfRows):
            for x in range(TILES_PER_ROW):
                tempSurface = pygame.Surface(TILE_SIZE)
                offsetX = -1 * ((TILE_SIZE[0] + TILES_PADDING) * x)
                offsetY = -1 * ((TILE_SIZE[1] + TILES_PADDING) * y)
                tempSurface.blit(tileFile, (offsetX, offsetY))
                self.tiles.append(tempSurface)
                
        return True

    def checkCharacters(self):
        num = 0
        checker = True
        while checker:
            self.checkerMessage("Character " + str(num), 1)
            tempText = CHARACTER_FILE + str(num) + CHARACTER_FILE_EXT
            tempPath = os.path.join(self.missionPath, tempText)
            if (os.path.exists(tempPath)):

                self.checkerMessage("Character Portrait", 2)
                tempText = CHARACTER_PORTRAIT + str(num) + CHARACTER_PORTRAIT_EXT
                tempPath2 = os.path.join(self.missionPath, tempText)
                if not(os.path.exists(tempPath2)):
                       return False
                portrait = pygame.image.load(tempPath2).convert_alpha()

                self.checkerMessage("Character File", 2)
                success = self.buildCharacter(tempPath, portrait)
                if not success:
                    return False

                self.checkerMessage("Character Spritesheet", 2)
                tempText = CHARACTER_SPRITE + str(num) + CHARACTER_SPRITE_EXT
                tempPath = os.path.join(self.missionPath, tempText)
                if not(os.path.exists(tempPath)):
                       return False
                image = pygame.image.load(tempPath).convert_alpha()
                self.players[num].piece.changeSpriteSheet(image)
                
                num += 1
            else:
                checker = False

        if (num < 1) or (num > MAX_CHAR_TOTAL):
            return False
        
        return True

    def checkEnemies(self):
        num = 0
        checker = True
        while checker:
            self.checkerMessage("Enemy " + str(num), 1)
            tempText = ENEMY_FILE + str(num) + ENEMY_FILE_EXT
            tempPath = os.path.join(self.missionPath, tempText)
            if (os.path.exists(tempPath)):
                self.checkerMessage("Enemy File", 2)
                success = self.buildEnemy(tempPath)
                if not success:
                    return False
                
                self.checkerMessage("Enemy Spritesheet", 2)
                tempText = ENEMY_SPRITE + str(num) + ENEMY_SPRITE_EXT
                tempPath = os.path.join(self.missionPath, tempText)
                if not(os.path.exists(tempPath)):
                       return False
                image = pygame.image.load(tempPath).convert_alpha()
                self.enemies[num].piece.changeSpriteSheet(image)
                
                num += 1
            else:
                checker = False

        if num < 1:
            return False

        return True


    def checkChapters(self):
        num = 0
        checker = True
        while checker:
            self.checkerMessage("Chapter " + str(num), 1)
            tempText = CHAPTER_FILE + str(num) + CHAPTER_FILE_EXT
            tempPath = os.path.join(self.missionPath, tempText)
            tempText = MAP_FILE + str(num) + MAP_FILE_EXT
            tempPath2 = os.path.join(self.missionPath, tempText)
            tempText = PLAYER_POS_FILE + str(num) + PLAYER_POS_FILE_EXT
            tempPath3 = os.path.join(self.missionPath, tempText)
            tempText = OBSTACLE_FILE + str(num) + OBSTACLE_FILE_EXT
            tempPath4 = os.path.join(self.missionPath, tempText)
            self.checkerMessage("Chapter Data File", 2)
            if os.path.exists(tempPath):
                success = self.buildChapter(tempPath, tempPath2, tempPath3, tempPath4)
                if not success:
                    return False
                num += 1
            else:
                checker = False

        

        if (num < 1) or (num > MAX_CHAPTERS):
            return False

        return True

    def checkAbilities(self):
        num = 0
        checker = True
        while checker:
            self.checkerMessage("Ability " + str(num), 1)
            tempText = ABILITY_FILE + str(num) + ABILITY_FILE_EXT
            tempPath = os.path.join(self.missionPath, tempText)
            if (os.path.exists(tempPath)):
                success = self.buildAbility(tempPath)
                if not success:
                    return False
                
                num += 1
            else:
                checker = False

        if num < 1:
            return False

        return True
            

    def buildCharacter(self, inPath, portrait):
        charFile = open(inPath)

        self.checkerMessage("Name", 3)
        charName = charFile.readline()
        if not self.stringSizeChecker(charName):
            return False

        self.checkerMessage("Class", 3)
        charClass = charFile.readline()
        if not self.stringSizeChecker(charName):
            return False

        self.checkerMessage("Stats", 3)
        charStats = []
        for x in range (0, 8):
            tempString = charFile.readline()
            try:
                tempStat = int(tempString)
            except ValueError:
                return False
            if not self.statSizeChecker(tempStat):
                return False
            charStats.append(tempStat)

        self.checkerMessage("Growths", 3)
        charStatGrowths = []
        for x in range (0, 8):
            tempString = charFile.readline()
            try:
                tempStat = int(tempString)
            except ValueError:
                return False
            if not self.statSizeChecker(tempStat):
                return False
            charStatGrowths.append(tempStat)

        self.checkerMessage("Mana", 3)
        charMana = []
        for x in range (0, 3):
            tempString = charFile.readline()
            try:
                tempStat = int(tempString)
            except ValueError:
                return False
            if not self.manaSizeChecker(tempStat):
                return False
            charMana.append(tempStat)
            

        self.checkerMessage("Finalizing", 3)
        self.players.append(player.Player(charName, charClass, charStats, charStatGrowths, charMana, portrait))
        
        return True

    def buildEnemy(self, inPath):
        try:
            enemyFile = open(inPath)

            self.checkerMessage("Name", 3)
            enemyName = enemyFile.readline()
            if not self.stringSizeChecker(enemyName):
                return False

            self.checkerMessage("Stats", 3)
            enemyStats = []
            for x in range (0, 8):
                tempString = enemyFile.readline()
                try:
                    tempStat = int(tempString)
                except ValueError:
                    return False
                if not self.statSizeChecker(tempStat):
                    return False
                enemyStats.append(tempStat)

            self.checkerMessage("Reward", 3)
            enemyGift = []
            for x in range (0, 3):
                tempString = enemyFile.readline()
                try:
                    tempStat = int(tempString)
                except ValueError:
                    return False
                if not self.statSizeChecker(tempStat):
                    return False
                enemyGift.append(tempStat)

            self.checkerMessage("Finalizing", 3)
            self.enemies.append(enemy.Enemy(enemyName, enemyStats, enemyGift))
            
            return True

            
            
        except:
            return False


    def buildAbility(self, inPath):
        try:
            abilityFile = open(inPath)
            
            self.checkerMessage("Name", 2)
            abilityName = abilityFile.readline().rstrip()
            if not self.stringSizeChecker(abilityName):
                return False

            self.checkerMessage("Description", 2)
            abilityDesc = abilityFile.readline().rstrip()
            if not self.stringSizeChecker(abilityDesc, 2):
                return False

            self.checkerMessage("Range", 2)
            abilityRangeMin = int(abilityFile.readline())
            if not self.statSizeChecker(abilityRangeMin, True):
                return False
            
            abilityRangeMax = int(abilityFile.readline())
            if not self.statSizeChecker(abilityRangeMax, True):
                return False

            self.checkerMessage("Area of Effect", 2)
            abilityAOE = int(abilityFile.readline())

            self.checkerMessage("Damage", 2)
            abilityDamage = float(abilityFile.readline())
            if not self.statSizeChecker(abilityDamage, True):
                return False

            self.checkerMessage("Accuracy", 2)
            abilityAccuracy = float(abilityFile.readline())
            if not self.statSizeChecker(abilityAccuracy, True):
                return False

            self.checkerMessage("Stun", 2)
            abilityStun = float(abilityFile.readline())
            if (abilityStun < 0) or (abilityStun > 1):
                return False

            self.checkerMessage("Special Effect", 2)
            abilitySpecial = int(abilityFile.readline())

            self.checkerMessage("Mana Cost", 2)
            abilityMana = []
            for x in range (0, 4):
                tempMana = int(abilityFile.readline())
                if not self.statSizeChecker(tempMana, True):
                    return False
                abilityMana.append(tempMana)

            self.checkerMessage("Stats used", 2)
            abilityStatOff = abilityFile.readline().rstrip()
            if not(abilityStatOff == "P" or abilityStatOff == "M"):
                return False
            abilityStatDef = abilityFile.readline().rstrip()
            if not(abilityStatDef == "P" or abilityStatDef == "M"
                   or abilityStatDef == "L"):
                return False

            self.checkerMessage("Finalizing", 2)
            self.abilities.append(
                ability.Ability(abilityName, abilityDesc, abilityRangeMin,
                               abilityRangeMax, abilityAOE, abilityDamage,
                               abilityAccuracy, abilityStun, abilitySpecial,
                               abilityMana, abilityStatOff, abilityStatDef))

            return True

        except:
            return False

    def buildChapter(self, inPath, inPath2, inPath3, inPath4):
        chapterFile = open(inPath)
        
        chapterName = chapterFile.readline()
        if not self.stringSizeChecker(chapterName, 1):
            return False

        self.checkerMessage("Map File", 2)
        if not (os.path.exists(inPath2)):
            return False
        mapFile = open(inPath2)
        mapArray = mapFile.readlines()
        tempSize = len(mapArray)
        if (tempSize < MAP_SIZE_MIN) or (tempSize > MAP_SIZE_MAX):
            return False
        testSize = len(mapArray[0]) - 1
        for x in range(0, len(mapArray)):
            mapArray[x] = mapArray[x].rstrip()
            tempSize = len(mapArray[x])
            if (tempSize < MAP_SIZE_MIN) or (tempSize > MAP_SIZE_MAX):
                return False
            if tempSize != testSize:
                return False

        
        self.checkerMessage("Map Obstacles", 2)
        obstacleFile = open(inPath4)
        tempArray = obstacleFile.readlines()
        obstacleArray = []
        for x in tempArray:
            obstacleArray.append(x.split(";"))

        enemyArray = []
        for x in obstacleArray:
            if len(x) != 4:
                return False
            try:
                x[1] = int(x[1])
                x[2] = int(x[2])
                x[3] = int(x[3])
                if x[2] < 0 or x[2] > len(mapArray[0]):
                    return False
                if x[3] < 0 or x[3] > len(mapArray):
                    return False
                if x[0] == "E":
                    if x[1] < 0 or x[1] > len(self.enemies):
                        return False
            except:
                return False

        self.checkerMessage("Starting Positions File", 2)
        if not (os.path.exists(inPath3)):
            return False
        startingFile = open(inPath3)
        posArray = startingFile.readlines()
        
        if (len(posArray) < MAX_CHAR_ACTIVE) or (len(posArray) > MAX_SETUP_POSITIONS):
            return False
        
        refinedArray = []
        for element in posArray:
            tempArray = element.split(' ')
            if len(tempArray) != 2:
                return False
            tempX = 0
            tempY = 0
            try:
                tempX = int(tempArray[0])
                tempY = int(tempArray[1])
            except ValueError:
                return False

            if (tempX < 0) or (tempY < 0) or (tempX > len(mapArray[0]) - 1) or (tempY > len(mapArray) - 1):
                return False
            
            refinedArray.append((tempX, tempY))

        self.checkerMessage("Finalizing Chapter", 2)
        self.chapters.append(chapter.Chapter(chapterName, mapArray, refinedArray, obstacleArray))

        chapterFile.close()
        mapFile.close()
        return True

    def stringSizeChecker(self, inString, stringType=0):
        if stringType == 1:
            maxSize = CHAPTER_NAME_STRING_MAX
        elif stringType == 0:
            maxSize = CHARACTER_STRING_MAX
        else:
            maxSize = ABILITY_DESC_STRING_MAX

        
        tempSize = len(inString)
        if (tempSize >= 1) and (tempSize <= maxSize):
            return True
        else:
            return False

    def statSizeChecker(self, inInt, canBeZero=False):
        if canBeZero:
            statMin = 0
        else:
            statMin = 1
        
        if (inInt >= statMin) and (inInt <= STAT_MAX):
            return True
        else:
            return False

    def manaSizeChecker(self, inInt):
        if (inInt >= 1) and (inInt <= MANA_MAX):
            return True
        else:
            return False

    def createSuccessMenu(self):
        if self.success:
            self.menu = menu.Menu(SCREEN_SIZE[0], SCREEN_SIZE[1], MISSION_ERROR_MENU_HEIGHT,
                                  "Campaign loaded!", ["Continue"],
                                  MISSION_MENU_FONT_SIZE, MENU_COLORS["green"])
        else:
            self.menu = menu.Menu(SCREEN_SIZE[0], SCREEN_SIZE[1], MISSION_ERROR_MENU_HEIGHT,
                                  "Failed to load campaign", ["Back"],
                                  MISSION_MENU_FONT_SIZE, MENU_COLORS["red"])

    def update(self):
        pass

    def incMenu(self):
        self.menu.incrementSelection()

    def decMenu(self):
        self.menu.decrementSelection()

    def confirm(self):
        self.confirmed = True

    def back(self):
        return (self.confirmed and not(self.success))

    def advance(self):
        return (self.confirmed and self.success)

    def numOfChapters(self):
        return len(self.chapters)

    def numOfEnemies(self):
        return len(self.enemies)

    def checkerMessage(self, message, spaces=0):
        if DEBUG_MODE:
            spaceString = ""
            if (spaces < 0) or (spaces > 10):
                spaces = 0
            while spaces > 0:
                spaceString += " "
                spaces -= 1
            print spaceString + "Checking " + message

    def goCheat(self, inCheat):
        if inCheat == 1:
            self.cheatery = True
            self.confirm()
