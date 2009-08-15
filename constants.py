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
import pygame
import sys
import ability

pygame.mixer.init()

FRAME_RATE = 40
SCREEN_SIZE = (800, 600)
ENTIRE_SCREEN = pygame.Rect( (0,0), SCREEN_SIZE )
FADE_IN = 10

DEBUG_MODE = True

BLACK = (0, 0, 0)
TRANSPARENT_COLOR = (255, 0, 255)

COLOR_MIN = 0
COLOR_MAX = 255

MENU_COLOR_ON = (200, 200, 200)
MENU_COLOR_OFF = (100, 100, 100)
MENU_COLOR_BG = (20, 20, 20)

MAX_CHAR_TOTAL = 12
MAX_CHAR_ACTIVE = 5
MAX_SETUP_POSITIONS = 10
MAX_CHAPTERS = 50

# A+(B^(Cn + D))
XP_FORMULA_A = 10
XP_FORMULA_B = 25
XP_FORMULA_C = 0.125
XP_FORMULA_D = 0.6

MAX_LEVEL = 20

PIECE_SIZE = (32, 64)

STARTING_MANA_MULTIPLIER = 2

TILE_SIZE = (32, 32)
TILES_PER_ROW = 4
TILES_TOTAL = 4
TILES_PADDING = 1

MAP_SIZE_MIN = 5
MAP_SIZE_MAX = 30
MAP_OUTLINE_SIZE = 1
MAP_OUTLINE_COLOR = (30, 30, 30)

SPRITE_SHEET_NUM_X = 3

SPRITE_SHEET_IDLE = 0
SPRITE_SHEET_ACTIVE = 1

IDLE_ANIM_SPEED = (20, 5)
ACTIVE_ANIM_SPEED = (11, 4)

BLACK_SCREEN = pygame.Surface(SCREEN_SIZE)
BLACK_SCREEN.fill((0, 0, 0), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

BOX_FONT_COLOR = (250, 250, 250)

FONTS = ["fontdata.ttf"]

DATA_PATH = "data"
MISSION_PATH = os.path.join(DATA_PATH, "missions")
GRAPHICS_PATH = os.path.join(DATA_PATH, "graphics")
SOUND_PATH = os.path.join(DATA_PATH, "sounds")
MISSION_FILE = "mission.dat"
TILESET_FILE = "tileset.png"
MISSION_PICTURE = "missionpic.png"
CHAPTER_FILE = "chapter"
CHAPTER_FILE_EXT = ".dat"
CHARACTER_FILE = "character"
CHARACTER_FILE_EXT = ".dat"
CHARACTER_SPRITE = "charpiece"
CHARACTER_SPRITE_EXT = ".png"
CHARACTER_PORTRAIT = "charport"
CHARACTER_PORTRAIT_EXT = ".png"
MAP_FILE = "map"
MAP_FILE_EXT = ".dat"
PLAYER_POS_FILE = "playerpos"
PLAYER_POS_FILE_EXT = ".dat"
ENEMY_FILE = "enemy"
ENEMY_FILE_EXT = ".dat"
ENEMY_SPRITE = "enemypiece"
ENEMY_SPRITE_EXT = ".png"
OBSTACLE_FILE = "mapPlacement"
OBSTACLE_FILE_EXT = ".dat"
ABILITY_FILE = "ability"
ABILITY_FILE_EXT = ".dat"

MENU_LIST_SIZE = 10

MENU_COLORS = {"red": (200, 10, 10),
               "bright_blue": (10, 100, 210),
               "yellow": (180, 180, 5),
               "green": (10, 150, 10),
               "deep_blue": (5, 30, 100)
               }
FONT_COLORS = {"yellow": (180, 180, 5),
               "white": (250, 250, 250),
               "gray": (120, 120, 120),
               "black": (2, 2, 2)
               }

AURA_COLORS = {"blue": (20, 90, 160),
               "red": (180, 30, 30),
               "yellow": (180, 150, 30)
               }

CURSOR_IMAGE = "cursor1.png"
CURSOR_SIZE = (6, 6)
CURSOR_STEPS = 4
CURSOR_ANIM_SPEED = 6

CURSOR_HOLD_DELAY1 = 18
CURSOR_HOLD_DELAY2 = 2

MAIN_MENU_FONT_SIZE = 20
MAIN_MENU_COLOR_ON = MENU_COLOR_ON
MAIN_MENU_COLOR_OFF = MENU_COLOR_OFF
MAIN_MENU_COLOR_BG = MENU_COLOR_BG

MISSION_MENU_SIZE_SINGLE = (200, 20)
MISSION_MENU_HEIGHT_B = SCREEN_SIZE[1] - 50
MISSION_MENU_COLOR_ON = MENU_COLOR_ON
MISSION_MENU_COLOR_OFF = MENU_COLOR_OFF
MISSION_MENU_COLOR_BG = MENU_COLOR_BG
MISSION_SCREEN_SPACING = 10
MISSION_SCREEN_FONT_SIZE = 20
MISSION_MENU_FONT_SIZE = 14
MISSION_PICTURE_SIZE = (750, 300)
MISSION_PICTURE_COLOR = (70, 70, 70)
MISSION_PICTURE_NEM_SIZE = 12
MISSION_PICTURE_NEM_COLOR = (250, 250, 250)
MISSION_ERROR_MENU_HEIGHT = 50
MISSION_MAX_NAME = 30

BATTLE_MENU_ELEMENT_SIZE = (120, 20)
BATTLE_MENU_FONT_SIZE = 14
BATTLE_MENU_COLOR_ON = FONT_COLORS["yellow"]
BATTLE_MENU_COLOR_OFF = FONT_COLORS["gray"]
BATTLE_MENU_COLOR_BG = MENU_COLORS["deep_blue"]

CHARACTER_STRING_MAX = 20
CHAPTER_NAME_STRING_MAX = 30
ABILITY_DESC_STRING_MAX = 120
STAT_MAX = 99
MANA_MAX = 6

CHAPTER_NAME_SECONDS = 3

CHAPTER_NAME_PATTERN = "bar2.png"
CHAPTER_NAME_BORDER = "border1.png"
CHAPTER_NAME_PATTERN_SIZE = 300
CHAPTER_NAME_BAR_HEIGHT = 100
CHAPTER_NAME_BORDER_SIZE = 6
CHAPTER_NAME_FONTSIZE1 = 16
CHAPTER_NAME_FONTSIZE2 = 22
CHAPTER_NAME_COLOR = (250, 250, 250)
CHAPTER_NAME_MOVE_UP_DELAY = 5
CHAPTER_NAME_BG_PATTERN = "background3.png"
CHAPTER_NAME_BG_PATTERN_SIZE = (100, 100)
CHAPTER_NAME_BG_DIREC = 2
CHAPTER_NAME_BG_SPEED = 1

LIBRARY_BG_PATTERN = "background1.png"
LIBRARY_BG_PATTERN_SIZE = (50, 50)
LIBRARY_BG_DIREC = 0
LIBRARY_BG_SPEED = 1

CARD_TAB_SIZE = (75, 25)
CARD_TAB_FILE = "tab"
CARD_TAB_FILE_EXT = ".png"

CARD_OUTTER_PADDING = 5
CARD_INNER_PADDING = 3
CARD_TAB_ROW_LENGTH = (CARD_TAB_SIZE[0] * 4) + (CARD_INNER_PADDING * 3)
CARD_NEUTRAL_COLOR = (230, 230, 230)
CARD_INDENT_COLOR = (180, 180, 180)
CARD_NAME_SIZE = (CARD_TAB_ROW_LENGTH, 25)
CARD_DESC_SIZE = (CARD_NAME_SIZE[0], 130)
CARD_FONT = FONTS[0]
CARD_FONT_SIZE_BIG = 20
CARD_FONT_COLOR = FONT_COLORS["black"]

tempXBlah =  CARD_TAB_ROW_LENGTH + (CARD_OUTTER_PADDING * 2)
tempYBlah = (CARD_NAME_SIZE[1] + CARD_DESC_SIZE[1] + (CARD_OUTTER_PADDING * 2)
             + CARD_TAB_SIZE[1] + (CARD_INNER_PADDING * 2))
CARD_SIZE = (tempXBlah, tempYBlah)


PLANNING_BG_IMAGE = "background1.png"
PLANNING_BG_SIZE = (50, 50)
PLANNING_BG_DIREC = 0
PLANNING_BG_SPEED = 3

PLANNING_BOX_PATTERN = "background2.png"
PLANNING_BOX_BORDER = "border1.png"
PLANNING_BOX_PATTERN_SIZE = (20, 20)
PLANNING_BOX_BORDER_SIZE = 6
PLANNING_BOX_FONT = FONTS[0]
PLANNING_BOX_FONT_SIZE = 16
PLANNING_BOX_SIZE1 = (600, 50)
PLANNING_BOX_SIZE2 = (80, 40)
PLANNING_BOX_CHARS_PER_COL = 4
PLANNING_BOX_PADDING = 10
PLANNING_BOX_PIECE_FILL = (20, 50, 100)
PLANNING_BOX_DONE_SIZE = (60, 20)
PLANNING_BOX_LIGHT_RANGE = 25
PLANNING_XP_BAR_SIZE = (200, 15)
PLANNING_XP_BAR_COLOR_FULL = (30, 210, 220)
PLANNING_XP_BAR_COLOR_EMPTY = (10, 10, 10)
PLANNING_XP_BAR_PADDING = 10
PLANNING_XP_TEXT_SIZE = (30, 20)
PLANNING_XP_TEXT2_SIZE = (100, 20)

STAT_BOX_PATTERN = "background2.png"
STAT_BOX_BORDER = "border1.png"
STAT_BOX_PATTERN_SIZE = (20, 20)
STAT_BOX_BORDER_SIZE = 6
STAT_BOX_FONT = FONTS[0]
STAT_BOX_FONT_SIZE = 20
STAT_BOX_ELEMENT_SIZE = (55, 30)
STAT_BOX_PADDING = 25
NAME_BOX_ELEMENT_SIZE = (180, 25)
NAME_BOX_PADDING = 10
NAME_BOX_FONT_SIZE = 16

MANA_BOX_PATTERN = "background2.png"
MANA_BOX_BORDER = "border1.png"
MANA_BOX_PATTERN_SIZE = (20, 20)
MANA_BOX_BORDER_SIZE = 6
MANA_BOX_FONT = FONTS[0]
MANA_BOX_FONT_SIZE = 16
MANA_BOX_ELEMENT_SIZE= (60, 30)
MANA_BOX_PADDING = 10
MANA_TICK_SIZE = (5, MANA_BOX_ELEMENT_SIZE[1])
MANA_TICK_SPACING = 4
MANA_TICK_COLORS = [(200, 20, 20), (30, 30, 200), (220, 200, 10), (20, 20, 20)]



PORTRAIT_SIZE_ORIG = (600, 600)
PORTRAIT_SIZE_PLANNING = (200, 200)

PORTRAIT_BOX_PATTERN = "background2.png"
PORTRAIT_BOX_BORDER = "border1.png"
PORTRAIT_BOX_PATTERN_SIZE = (20, 20)
PORTRAIT_BOX_BORDER_SIZE = 6
PORTRAIT_BOX_PADDING = 0

PHASE_IMAGE = "phase"
PHASE_IMAGE_EXT = ".png"
PHASE_IMAGE_HEIGHT = 115
PHASE_IMAGE_WIDTHS = [209, 247, 215]
PHASE_IMAGE_SPEED_FAST = 40
PHASE_IMAGE_SPEED_SLOW = 1
PHASE_IMAGE_SLOW_TIME = 30

CHAR_STATION_PATTERN = "background2.png"
CHAR_STATION_BORDER = "border1.png"
CHAR_STATION_PATTERN_SIZE = (20, 20)
CHAR_STATION_BORDER_SIZE = 6
CHAR_STATION_PADDING = 10

SHUTTER_ALPHA = 150
SHUTTER_SPEED = 12

AURA_ALPHA_MIN = 120
AURA_ALPHA_MAX = 180
AURA_ALPHA_SPEED = 3

SYMBOL_FILE = "symbol"
SYMBOL_FILE_ON = "On"
SYMBOL_FILE_OFF = "Off"
SYMBOL_FILE_EXT = ".png"
SYMBOL_SIZE_ORIG = 215
SYMBOL_SIZE_LARGE = 50
SYMBOL_SIZE_SMALL = 25
SYMBOL_ABOVE = 5

STARFIELD_PATTERN = "background3.png"
STARFIELD_PATTERN_SIZE = (100, 100)

CORNER_INFO_PORTRAIT_SIZE = 100
CORNER_INFO_PADDING = 10
CORNER_INFO_COLOR = (230, 230, 120)
CORNER_INFO_ALPHA = 220

SOUND_ON = True

SOUND_FILES = ["cursor.wav",
               "select.wav",
               "cancel.wav",
               "phasein.wav",
               "phaseout.wav"]

SOUNDS = []
for sound in SOUND_FILES:
    tempFile = os.path.join(SOUND_PATH, sound)
    SOUNDS.append(pygame.mixer.Sound(tempFile))


def fatalError():
    print "Fatal Error!! - The impossible has happened"
    print "Program terminated"
    sys.exit()

def addUnique(inList, element):
    checker = True

    for x in inList:
        if x == element:
            checker = False

    if checker:
        inList.append(element)
