import tkinter as tk
from tkinter import *
import sys
import os
from tkinter import font, messagebox, filedialog
from PIL import Image, ImageTk
import webbrowser
import time
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Early definitions
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "Assets", relative_path)


# Variables
background_colour, foreground_colour = "#000000", "#00FF00"
active_background_colour, active_foreground_colour = "#00CC00", "#000000"
rootWidth, rootHeight = 800, 700
app_icon = resource_path("app_icon.ico") # Change this to something that makes more sense later
mainFontFamily = "IBM Plex Mono"
bg_music_path = resource_path("bg_music.mp3")
red, green = "#FF0000", "#00FF00"


# Music (initialise)
pygame.mixer.init()


# Initialise main window
root=tk.Tk()
root.title("Quiz")
root.geometry(f"{rootWidth}x{rootHeight}+100+100")
root.resizable(False, False)
root.configure(bg=background_colour)
root.iconbitmap(app_icon)

# Fonts
titleFont = font.Font(family=mainFontFamily, size=28, underline=True, weight="bold")
descFont = font.Font(family=mainFontFamily, size=14)
buttonFont = font.Font(family=mainFontFamily, size=17, underline=True)

# Widgets
titleLabel = tk.Label(root,
    text="QUIZ",
    font=titleFont,
    bg=background_colour,
    fg=foreground_colour,
    wraplength=(rootWidth-25),
    justify="center"
)
titleLabel.place(x=(rootWidth // 2), y=15, anchor="n")


descLabel = tk.Label(root,
    text="INITIALISING QUIZ APP!",
    font=descFont,
    bg=background_colour,
    fg=foreground_colour,
    wraplength=(rootWidth-25),
    justify="center"
)
descLabel.place(x=(rootWidth // 2), y=75, anchor="n")


def openMePages():
    webbrowser.open_new("https://github.com/sadgituser")
    webbrowser.open_new_tab("https://theprintedcraftuk.etsy.com")
    webbrowser.open_new_tab("mailto:kavi@mistrypi.dev")

meButton = tk.Button(root,
    text="DEV'S WORKS (LOTS OF TABS)",
    font=buttonFont,
    activebackground=active_background_colour,
    activeforeground=active_foreground_colour,
    bg=foreground_colour,
    fg=background_colour,
    command=openMePages,
    justify="center",
    relief="raised"
)
meButton.place(x=225, y=(rootHeight - 70), anchor="n")


closeButton = tk.Button(root,
    text="EXIT",
    font=buttonFont,
    activebackground=active_background_colour, 
    activeforeground=active_foreground_colour, 
    bg=foreground_colour, 
    fg=background_colour,
    command=root.destroy,
    justify="center",
    relief="raised"
)
closeButton.place(x=475, y=(rootHeight - 70), anchor="n")

def testLuck():
    luckPopup = tk.Toplevel(root)
    luckPopup.title("TEST YOUR LUCK...")
    luckPopup.geometry("300x300+150+150")
    luckPopup.resizable(False, False)
    luckPopup.configure(bg=red)
    luckPopup.iconbitmap(app_icon)

    currentLuck = "FAIL!"

    luckLabel = tk.Label(luckPopup,
        text=currentLuck,
        font=descFont,
        bg=background_colour,
        fg=foreground_colour,
        wraplength=75,
        justify="center"
    )
    luckLabel.place(x=150, y=125, anchor="n")

    def spin_luck():
        global currentLuck
        global luckLabel

        if currentLuck == "FAIL!":
            currentLuck = "WIN!"
        else:
            currentLuck = "FAIL!"
        luckLabel.configure(text=currentLuck)
    

    for i in range(5, 25):
        luckPopup.after(50, spin_luck)










luckButton = tk.Button(root,
    text="TEST YOUR LUCK",
    font=buttonFont,
    activebackground=active_background_colour,
    activeforeground=active_foreground_colour,
    bg=foreground_colour,
    fg=background_colour,
    command=testLuck,
    justify="center",
    relief="raised"
)
luckButton.place(x=650, y=(rootHeight - 70), anchor="n")







# Add logic for playing music here:
try:
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    messagebox.showerror("Music Fail", f"Failed to load background music: {str(e)}")


# Initialise main window
root.mainloop()
