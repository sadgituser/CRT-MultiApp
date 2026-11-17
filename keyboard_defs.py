import tkinter as tk
from tkinter import font, messagebox, filedialog
import webbrowser
import random
import time
import os
import stateVars
import quiz_defs


def start_keyboard_game():
    if stateVars.keyboard_game_ready == False:
        stateVars.keyboard_game_ready = True
