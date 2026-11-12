import tkinter as tk

# Widgets and Windows! (root & quiz)
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

# root window variables
rootWidth, rootHeight = 800, 700
background_colour, foreground_colour = "#000000", "#00FF00"
active_background_colour, active_foreground_colour = "#00CC00", "#000000"
mainFontFamily = "Consolas"
app_icon = "app-icon.ico"
bg_music_path = "bg_music.mp3"

# Quiz variables
players = []
questions = []
print_queue = []
is_printing = []
quiz_ready = []
quiz_settings = {
    "rand_questions": False,
    "rand_players": False,
    "time_limit": 15,
    "default_skips": 2,
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
