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
typeSpeed = 25
versionNum = 1.8
waiting_for_custom_speed = False

# Fonts
titleFont = None
playerFont = None
statusFont = None
questionFont = None
timerFont = None
winnerFont = None
descFont = None
locked_font = None
# Colours
current_colour_index = 0
colour_preset_names = ["green", "red", "blue", "turquoise", "yellow", "magenta", "gray"]
colour_presets = {
    "green": ["#00FF00", "#00DD00", "#22FF22", "#00EE00", "#1BF81B", "#0DD30D"],
    "red": ["#FF0000", "#FA2222", "#FF2424", "#E00000", "#DD0B0B", "#C70000"],
    "blue": ["#0000FF", "#1414F8", "#0D0DEE", "#2222FF", "#0000C2", "#0F0FE6"],
    "turquoise": ["#40E0D0", "#30F0DD", "#22D3C1", "#0AC0AE", "#2EFFEA", "#40E0D0"],
    "yellow": ["#FFFF00", "#E4E424", "#CFCF00", "#FFFF52", "#E6E62D", "#C7C712"],
    "magenta": ["#FF00FF", "#F026F0", "#FF4DFF", "#C703C7", "#DB28DB", "#D448D4"],
    "gray": ["#696969", "#868686", "#A1A1A1", "#AAAAAA", "#5E5E5E", "#555555"]
}


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


# Command history
command_history = []
history_index = 0
current_input = ""


# This file cannot be run, it is a Python (.py) file with all of the variables that assists main.py working in CRT-MultiApp.
# This is not a module on PyPI (Python Package Index) eitherm it is only a module that contains the variables necessary for the main function of CRT-MultiApp's main.py file to work.
# If you have stumbled across this file somehow and it is not in the same directory as main.py for CRT-MultiApp, then go to:
# https://github.com/sadgituser/CRT-MultiApp
# and download the executable from the releases page
