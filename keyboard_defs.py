import tkinter as tk
from tkinter import font, messagebox, filedialog
import webbrowser
import random
import time
import os
import stateVars
import quiz_defs

stateVars.keyboard_game_ready = False

def start_keyboard_game(raw_cmd):
    if stateVars.keyboard_game_ready == False:
        quiz_defs.print_term("Are you ready to start? This game requires focus and readiness! The keyboard layout will shift a lot, so be wary! \n")
        if raw_cmd == 'y':
            quiz_defs.print_term("Starting...")
            stateVars.keyboard_game_ready = True
            #initialise_keyboard_screen()

