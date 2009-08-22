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

import model

import minimenu
import menu
import textline
import incint
import missionPicture

from constants import *

class Model(model.Model):
    def __init__(self):
        super(Model, self).__init__()

        self.selectMenu()
        self.goBack = False
        self.goForward = False
        self.loadingMessage = textline.TextLine(SCREEN_SIZE[0], SCREEN_SIZE[1], 100, "Loading...", MISSION_SCREEN_FONT_SIZE, 1)


    def selectMenu(self):
        self.missionList = []
        for root, ds, fs in os.walk(MISSION_PATH):
            for item in ds:
                itemName, numOfMissions = self.checkMission(item)
                if (itemName != "") and (numOfMissions != 0):
                    self.missionList.append([itemName, numOfMissions, item])

        def compare(a, b):
            if a[2] < b[2]:
                return -1
            elif a[2] > b[2]:
                return 1
            else:
                return 0
        self.missionList.sort(compare)

        listSize = len(self.missionList)

        if listSize <= 0:
            self.noMissionsFound()
        else:
            self.page = incint.IncInt(1, 1, listSize)
            self.menu = minimenu.MiniMenu(pygame.Rect((0, 0), (MISSION_MENU_SIZE_SINGLE)),
                                  ["Begin Campaign", "Previous", "Next"],
                                  MISSION_MENU_FONT_SIZE, MISSION_MENU_COLOR_ON,
                                  MISSION_MENU_COLOR_OFF, MISSION_MENU_COLOR_BG)
            self.menu.rect.bottom = MISSION_MENU_HEIGHT_B
            self.menu.center(ENTIRE_SCREEN, True, False)
            self.buildPage()

    def buildPage(self):
        self.state = "page"

        currMission = self.getCurrMission()
        
        tempText = "Campaign " + str(self.page.value) + " of " + str(self.page.maximum) + ": " + currMission[0]
        self.textChapterName = textline.TextLine(SCREEN_SIZE[0], SCREEN_SIZE[1], MISSION_SCREEN_SPACING, tempText, MISSION_SCREEN_FONT_SIZE)

        tempText = "Number of Chapters: " + str(currMission[1])
        self.textNumOfChapters = textline.TextLine(SCREEN_SIZE[0], SCREEN_SIZE[1], (self.textChapterName.rect.bottom + MISSION_SCREEN_SPACING), tempText, MISSION_SCREEN_FONT_SIZE)

        tempPath = os.path.join(MISSION_PATH, currMission[2])
        self.missionPicture = missionPicture.MissionPicture(self.textNumOfChapters.rect.bottom, self.menu.rect.top, tempPath)       

    def noMissionsFound(self):
        self.state = "notfound"
        self.menu = menu.Menu(SCREEN_SIZE[0], SCREEN_SIZE[1], MISSION_ERROR_MENU_HEIGHT,
                                          "Error: No Missions Found", ["Back"],
                                          MISSION_MENU_FONT_SIZE, MENU_COLORS["red"])

    def checkMission(self, item):
        missionName = ""
        numOfMissions = 0
        
        missionPath = os.path.join(MISSION_PATH, item)
        missionPath = os.path.join(missionPath, MISSION_FILE)
        if (os.path.exists(missionPath)):
            missionFile = open(missionPath)
            tempName = missionFile.readline()
            tempSize = len(tempName)
            missionFile.close()
            if (tempSize > 0) and (tempSize <= MISSION_MAX_NAME):
                missionName = tempName

        checker = True
        while checker:
            tempText = CHAPTER_FILE + str(numOfMissions) + CHAPTER_FILE_EXT
            chapterPath = os.path.join(MISSION_PATH, item)
            chapterPath = os.path.join(chapterPath, tempText)
            if (os.path.exists(chapterPath)):
                numOfMissions += 1
            else:
                checker = False
            
        return missionName, numOfMissions

    def incMenu(self):
        self.menu.inc()

    def decMenu(self):
        self.menu.dec()

    def confirm(self):
        if self.state == "page":
            if self.menu.value() == 1:
                self.goForward = True
            if self.menu.value() == 2:
                self.page.decrement()
                self.buildPage()
            elif self.menu.value() == 3:
                self.page.increment()
                self.buildPage()

        elif self.state == "notfound":
            self.goBack = True

    def back(self):
        return self.goBack

    def advance(self):
        return self.goForward

    def update(self):
        pass

    def getCurrMission(self):
        return self.missionList[self.page.value - 1]
