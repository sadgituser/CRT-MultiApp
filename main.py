import tkinter as tk
from tkinter import *
import sys
import os
from tkinter import font, messagebox, filedialog
import webbrowser
import random
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import stateVars
import quiz_defs

app_icon = quiz_defs.resource_path("app-icon.ico")
bg_music_path = quiz_defs.resource_path("bg_music.mp3")


# Music (initialise)
pygame.mixer.init()


# Initialise main window
stateVars.root=tk.Tk()
stateVars.root.title("CRT-MultiApp")
stateVars.root.geometry(f"{stateVars.rootWidth}x{stateVars.rootHeight}+100+100")
stateVars.root.resizable(False, False)
stateVars.root.configure(bg=stateVars.background_colour)
try:
    stateVars.root.iconbitmap(app_icon)
except:
    pass


# CRT Effect
stateVars.crt_canvas = tk.Canvas(stateVars.root, width=stateVars.rootWidth, height=stateVars.rootHeight, bg=stateVars.background_colour, highlightthickness=0)
stateVars.crt_canvas.place(x=0, y=0, relwidth=1, relheight=1)

for y in range(0, stateVars.rootHeight, 3):
    stateVars.crt_canvas.create_line(0, y, stateVars.rootWidth, y, fill="#001100", stipple="gray50", tags="scanlines")

moving_scanline = stateVars.crt_canvas.create_line(0, 0, stateVars.rootWidth, 0, fill="#00FF44", width=10, stipple="gray25")
scanline_y = 0
stateVars.moving_scanline = moving_scanline



# Fonts
titleFont = font.Font(family=stateVars.mainFontFamily, size=28, underline=True, weight="bold")
descFont = font.Font(family=stateVars.mainFontFamily, size=14)
buttonFont = font.Font(family=stateVars.mainFontFamily, size=17, underline=True)
playerFont = font.Font(family=stateVars.mainFontFamily, size=48, weight="bold", underline=True)
questionFont = font.Font(family=stateVars.mainFontFamily, size=24, weight="bold")
timerFont = font.Font(family=stateVars.mainFontFamily, size=18, weight="bold")
statusFont = font.Font(family=stateVars.mainFontFamily, size=17)
winnerFont = font.Font(family=stateVars.mainFontFamily, size=48, underline=True, weight="bold")


# Widgets
titleLabel = tk.Label(stateVars.root,
    text="THE CRT",
    font=titleFont,
    bg=stateVars.background_colour,
    fg=stateVars.foreground_colour,
    wraplength=(stateVars.rootWidth-25),
    justify="center"
)
titleLabel.place(x=(stateVars.rootWidth // 2), y=20, anchor="n")
stateVars.titleLabel = titleLabel


clockLabel = tk.Label(stateVars.root,
    font=descFont,
    bg=stateVars.background_colour,
    fg=stateVars.foreground_colour
)
clockLabel.place(x=(stateVars.rootWidth - 15), y=20, anchor="ne")
stateVars.clockLabel = clockLabel


termText = tk.Text(stateVars.root, 
    bg="#000500", 
    fg=stateVars.foreground_colour, 
    insertbackground=stateVars.foreground_colour, 
    font=descFont, 
    relief="flat"
)
termText.place(x=15, y=80, width=(stateVars.rootWidth - 30), height=(stateVars.rootHeight - 150))
termText.insert("end", "CRT OS v1.0\nType 'help' for commands. \n\n> ")
termText.config(state="disabled")
stateVars.termText = termText


promptLabel = tk.Label(stateVars.root, 
    text=">",
    font=descFont,
    bg=stateVars.background_colour,
    fg=stateVars.foreground_colour
)
promptLabel.place(x=15, y=(stateVars.rootHeight - 55))
stateVars.promptLabel = promptLabel

termEntry = tk.Entry(stateVars.root,
    bg=stateVars.background_colour,
    fg=stateVars.foreground_colour,
    insertbackground=stateVars.foreground_colour,
    font=descFont,
    relief="flat",
    highlightthickness=1,
    highlightbackground=stateVars.foreground_colour
)
termEntry.place(x=35, y=(stateVars.rootHeight - 55), width=(stateVars.rootWidth - 50), height=30)
termEntry.focus()
stateVars.termEntry = termEntry


quizPlayerLabel = tk.Label(stateVars.root, 
    font=playerFont, 
    bg=stateVars.background_colour, 
    fg=stateVars.foreground_colour, 
    justify="center"
)
stateVars.quizPlayerLabel = quizPlayerLabel

quizQuestionLabel = tk.Label(stateVars.root, 
    font=questionFont, 
    bg=stateVars.background_colour, 
    fg=stateVars.foreground_colour, 
    wraplength=(stateVars.rootWidth - 50), 
    justify="center"
)
stateVars.quizQuestionLabel = quizQuestionLabel

quizTimerLabel = tk.Label(stateVars.root, 
    font=timerFont, 
    bg=stateVars.background_colour, 
    fg=stateVars.foreground_colour, 
    justify="center"
)
stateVars.quizTimerLabel = quizTimerLabel

quizStatusLabel = tk.Label(stateVars.root, 
    font=statusFont, 
    bg=stateVars.background_colour, 
    fg=stateVars.foreground_colour, 
    justify="center"
)
stateVars.quizStatusLabel = quizStatusLabel


quiz_setup_step = 0
winner_flashing = False
winner_timer_id = None
winner_can_exit = False


quizPauseButton = tk.Button(stateVars.root,
    text="PAUSE",
    font=descFont,
    bg=stateVars.background_colour,
    fg=stateVars.foreground_colour,
    relief="solid",
    command=quiz_defs.toggle_pause
)
stateVars.quizPauseButton = quizPauseButton

quizQuitButton = tk.Button(stateVars.root,
    text="QUIT QUIZ",
    font=descFont,
    bg=stateVars.background_colour,
    fg="#FF0000",
    relief="solid",
    command=quiz_defs.force_quit_quiz
)
stateVars.quizQuitButton = quizQuitButton

# Music Logic
try:
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    messagebox.showerror("Music Fail", f"Failed to load background music: {str(e)}")


# Initialise main window
quiz_defs.apply_crt_flicker()
quiz_defs.animate_crt_beam()
quiz_defs.update_clock()

termEntry.bind("<Return>", quiz_defs.execute_command)
stateVars.root.mainloop()
