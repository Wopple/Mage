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
import view
import controller

import title_m
import title_v

import missionSel_m
import missionSel_v

import loadSel_m
import loadSel_v

import chapterNameScreen_m
import chapterNameScreen_v

import prebattleScreen_m
import prebattleScreen_v

import postbattleScreen_m
import postbattleScreen_v

import battleScreen_m
import battleScreen_v

import abilityViewer_m
import abilityViewer_v

import phaseAnim_m
import phaseAnim_v

import no_c
import menu_c
import cursor_c
import AI_c

import game_m
import game_v

import abilityLibrary_m
import abilityLibrary_v

from constants import *



def changeMVC(val, newM, newV, newC):
    #Changes the Model/View/Controller currently in use
    #Val must be a new value than the previous value in order to
    #register.
    global state
    global screen
    global m
    global v
    global c
    
    if state != val:
        state = val
        m = newM
        v = newV
        c = newC
        m.setView(v)
        c.setView(v)
        c.setModel(m)
        v.setModel(m)
        v.setScreen(screen)

def changeC(newC):
    #Changes only the controller
    global c
    c = newC
    c.setView(v)
    c.setModel(m)

def proceed(tickClock=True):
    #Progresses by one frame, updating each component of the MVC system.
    global m
    global v
    global c
    global clock
    
    m.update()
    v.update(tickClock)
    c.update()
    checkError()
    if tickClock:
        clock.tick(FRAME_RATE)

def checkError():
    if (m.checkError()) or (v.checkError()) or (c.checkError()):
        print m.checkError(), v.checkError(), c.checkError()
        criticalError(1)

def criticalError(val):
    print "\nCritical Error!"

    if val == 1:
        print "Undefined MVC"
    else:
        print "Unspecified Error Type"

    sys.exit(0)


def mainLoop():
    #Main Game Loop
    global game

    #Runs Title Screen/Main Menu
    checker01 = False
    changeMVC(1, title_m.Model(), title_v.View(), menu_c.Controller())
    proceed()
    if m.advance():
        if m.titleMenu.value() == 1:
            #Runs the Campaign Selection menu
            changeMVC(2, missionSel_m.Model(), missionSel_v.View(), menu_c.Controller())
            while not(m.either()):
                proceed()
            if m.advance():
                checker01 = True
                screenshot = pygame.Surface(SCREEN_SIZE)
                screenshot.blit(screen, (0,0))
                v.update()
        elif m.titleMenu.value() == 2:
            #Runs the Load Game section
            changeMVC(3, loadSel_m.Model(), loadSel_v.View(), menu_c.Controller())
            while not(m.either()):
                proceed()
            if m.advance():
                checker01 = True
    if checker01:
        #Initiates the game model, which involves much loading and file reading
        missionPath = m.getCurrMission()[2]
        game = game_m.Model(missionPath)
        changeMVC(4, game, game_v.View(), menu_c.Controller())
        screen.blit(screenshot, (0,0))

        while not(m.either()):
            proceed()

        if m.cheatery:
            changeMVC(11, abilityLibrary_m.Model(game.abilities), abilityLibrary_v.View(), menu_c.Controller())
            while not(m.back()):
                proceed()
        elif m.advance():
            #Begins the game loop
            gameLoop(0)

    changeMVC(1, title_m.Model(), title_v.View(), menu_c.Controller())


def gameLoop(inChapter):
    global game
    currChapter = inChapter

    #Loop for every chapter in the game
    while (currChapter >= 0) and (currChapter < game.numOfChapters()):
        
        theChapter = game.chapters[currChapter]
        chapterNameScreen(theChapter, currChapter)
        activeChars = chapterPrebattleSelect(theChapter)
        xpGained = chapterBattle(game.tiles, theChapter, activeChars, game.enemies)
        game.xp += xpGained
        chapterPostbattleXP(theChapter, activeChars)
        currChapter += 1
        changeMVC(0, model.Model(), view.View(), controller.Controller())

def chapterNameScreen(theChapter, currChapter):
    changeMVC(5, chapterNameScreen_m.Model(currChapter, theChapter.name), chapterNameScreen_v.View(), no_c.Controller())
    while not (m.advance()):
        proceed()

def chapterPrebattleSelect(theChapter):
    changeMVC(6, prebattleScreen_m.Model(game.players), prebattleScreen_v.View(), cursor_c.Controller())
    while not (m.advance()):
        proceed()
    activeChars = []
    for sel in range(len(m.planningScreen.pieceBox.charSelections)):
        if m.planningScreen.pieceBox.charSelections[sel]:
            activeChars.append(game.players[sel])
    return activeChars

def chapterBattle(tiles, theChapter, activeChars, enemyList):
    battleModel = battleScreen_m.Model(tiles, theChapter, activeChars, enemyList)
    battleView = battleScreen_v.View()
    changeMVC(8, battleModel, battleView, cursor_c.Controller())
    phase = -1
    menuOpen = False
    stationOpen = False
    while not (m.advance()):
        proceed()
        if phase != m.phase:
            phase = m.phase
            changePhaseAnim(phase, battleModel, battleView)
            if phase == 1 or phase == 0:
                changeC(cursor_c.Controller())
            elif phase == 2:
                changeC(AI_c.Controller())

        if (stationOpen != m.stationOpen) and (phase != 2):
            stationOpen = m.stationOpen
            if stationOpen:
                changeC(cursor_c.Controller())
            else:
                menuOpen = False
        if (menuOpen != m.menuOpen) and (m.stationOpen == False) and (phase != 2):
            menuOpen = m.menuOpen
            if menuOpen:
                changeC(menu_c.Controller())
            else:
                changeC(cursor_c.Controller())

        if m.cardsOpen:
            changeMVC(12, abilityViewer_m.Model(m.getAbilitiesFromCursorActor(), screen), abilityViewer_v.View(), menu_c.Controller())
            while not (m.either()):
                proceed()
            if m.advance():
                battleModel.performAction(m.getSel())
            changeMVC(8, battleModel, battleView, cursor_c.Controller())
            m.cardsOpen = False
            
        
    return m.xpGained

def chapterPostbattleXP(theChapter, activeChars):
    changeMVC(7, postbattleScreen_m.Model(activeChars, game.xp), postbattleScreen_v.View(), cursor_c.Controller())
    while not (m.advance()):
        proceed()
        if m.planningScreen.changeC:
            m.planningScreen.changeC = False

            if m.planningScreen.menuOpen:
                changeC(menu_c.Controller())
            else:
                changeC(cursor_c.Controller())
    game.xp = m.planningScreen.xp

def changePhaseAnim(phase, battleModel, battleView):
    phaseAnimModel = phaseAnim_m.Model(phase)
    phaseAnimView = phaseAnim_v.View()
    noC = no_c.Controller()

    while not (phaseAnimModel.advance()):
        changeMVC(9, battleModel, battleView, noC)
        proceed(False)
        changeMVC(10, phaseAnimModel, phaseAnimView, noC)
        proceed()
    changeMVC(8, battleModel, battleView, noC)
    m.phaseAnimComplete()
        



pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Working Title")
clock = pygame.time.Clock()

m = model.Model()
v = view.View()
c = controller.Controller()

game = model.Model()

state = 0

while not(m.back()):
    mainLoop()
