import tkinter as tk
from tkinter import font

# Config
CONFIG_FILE = None
config = {}

# Widgets and Windows
root = None
crt_canvas = None
moving_scanline = None
scanline_y = 0
titleLabel = None
clockLabel = None
termText = None
promptLabel = None
termEntry = None
quizPlayerLabel = None
quizQuestionLabel = None
quizTimerLabel = None
quizStatusLabel = None
quizPauseButton = None
quizQuitButton = None

# 'root' window variables
rootWidth, rootHeight = 800, 700
background_colour, foreground_colour = "#000000", "#00FF00"
active_background_colour, active_foreground_colour = "#00CC00", "#000000"
mainFontFamily = "Consolas"
app_icon = "app-icon.ico"
bg_music_path = "bg_music.mp3"

# Fonts
titleFont = font.Font(family=mainFontFamily, size=28, underline=True, weight="bold")
playerFont = font.Font(family=mainFontFamily, size=48, weight="bold", underline=True)
statusFont = font.Font(family=mainFontFamily, size=17)
questionFont = font.Font(family=mainFontFamily, size=24, weight="bold")
timerFont = font.Font(family=mainFontFamily, size=18, weight="bold")
winnerFont = font.Font(family=mainFontFamily, size=48, underline=True, weight="bold")
descFont = font.Font(family=mainFontFamily, size=14)
locked_font = font.Font(family=mainFontFamily, size=28, weight="bold", underline=True)


# Quiz variables
players = []
questions = []
print_queue = []
is_printing = False
quiz_ready = False
quiz_settings = {
    "rand_questions": False,
    "rand_players": False,
    "time_limit": 15,
    "default_skips": 1,
    "default_last_chance": True
}
quiz_active_players = []
quiz_active_questions = []
current_player_idx = 0
current_question_idx = 0
current_timer_id = None
time_remaining = 0
waiting_for_next = False
is_paused = False
is_last_chance_action = False
intro_timer_id = None
winner_flashing = False
winner_timer_id = None
winner_can_exit = False
quiz_setup_step = 0

# password
is_locked = False 
lock_frame = None
lock_password_entry = None
lock_logo_image = None
lock_error_label = None 
lock_was_paused = False
lock_was_waiting = False
lock_previous_key_binding = None 

#command history
command_history = []
history_index = 0
current_input = ""


# This file cannot be run, it is a Python (.py) file with all of the variables that assists main.py working in CRT-MultiApp.
# This is not a module on PyPI (Python Package Index) eitherm it is only a module that contains the variables necessary for the main function of CRT-MultiApp's main.py file to work.
# If you have stumbled across this file somehow and it is not in the same directory as main.py for CRT-MultiApp, then go to:
# https://github.com/sadgituser/CRT-MultiApp
# and download the executable from the releases page
