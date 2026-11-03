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


# Music (initialise)
pygame.mixer.init()


# Initialise main window
root=tk.Tk()
root.title("Quiz")
root.geometry(f"{rootWidth}x{rootHeight}+100+100")
root.resizable(False, False)
root.configure(bg=background_colour)
try:
    root.iconbitmap(app_icon)
except:
    pass

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
    text="DEV'S WORKS",
    font=buttonFont,
    activebackground=active_background_colour,
    activeforeground=active_foreground_colour,
    bg=foreground_colour,
    fg=background_colour,
    command=openMePages,
    justify="center",
    relief="raised"
)
meButton.place(x=200, y=(rootHeight - 70), anchor="n")


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
closeButton.place(x=400, y=(rootHeight - 70), anchor="n")

def testLuck():
    luckPopup = tk.Toplevel(root)
    luckPopup.title("TEST YOUR LUCK...")
    luckPopup.geometry("300x300+150+150")
    luckPopup.resizable(False, False)
    luckPopup.configure(bg=background_colour)
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
        nonlocal currentLuck
        if currentLuck == "FAIL!":
            currentLuck = "WIN!"
        else:
            currentLuck = "FAIL!"
        luckLabel.configure(text=currentLuck)
    

    for i in range(random.randint(5, 30)):
        luckPopup.after(i * 10, spin_luck)

    if currentLuck == "FAIL!":
        time.sleep(3)
        messagebox.showerror("You Failed", "You lost the gamble...")
        os._exit(1)
    else:
        time.sleep(3)
        messagebox.showinfo("You Win", "Your gamble paid off and you get to keep using the app!")
        luckPopup.destroy()


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
luckButton.place(x=600, y=(rootHeight - 70), anchor="n")


# CRT Effect
crt_canvas = tk.Canvas(root, width=rootWidth, height=rootHeight, bg=background_colour, highlightthickness=0)
crt_canvas.place(x=0, y=0, relwidth=1, relheight=1)

# Scan Lines
for y in range(0, rootHeight, 3):
    crt_canvas.create_line(0, y, rootWidth, y, fill="#001100", stipple="gray50", tags="scanlines")

# Moving Scanline
moving_scanline = crt_canvas.create_line(0, 0, rootWidth, 0, fill="#00FF44", width=2, stipple="gray25")
scanline_y = 0

def animate_crt_beam():
    global scanline_y
    scanline_y += 3
    if scanline_y > rootHeight:
        scanline_y = 0
    crt_canvas.coords(moving_scanline, 0, scanline_y, rootWidth, scanline_y)
    root.after(20, animate_crt_beam)
animate_crt_beam()

# Fisheye & Curves & Shadows
# TL Corner
crt_canvas.create_arc(-100, -100, 200, 200, start=270, extent=90, fill="#050505", outline="")
crt_canvas.create_oval(10, 10, 40, 25, fill="#003300", outline="")
#TR Corner
crt_canvas.create_arc(rootWidth - 200, -100, rootWidth + 100, 200, start=180, extent=90, fill="#050505", outline="")
crt_canvas.create_oval(rootWidth - 40, 10, rootWidth - 10, 25, fill="#003300", outline="")
#BL Corner
crt_canvas.create_arc(-100, rootHeight - 200, 200, rootHeight + 100, start=0, extent=90, fill="#050505", outline="")
#BR Corner
crt_canvas.create_arc(rootWidth - 200, rootHeight - 200, rootWidth + 100, rootHeight + 100, start=90, extent=90, fill="#050505", outline="")

# CRT Flicker
def apply_crt_flicker():
    glow_colours = ["#00FF00", "#00DD00", "#22FF22", "#00EE00"]
    chosen_colour = random.choice(glow_colours)
    titleLabel.configure(fg=chosen_colour)
    descLabel.configure(fg=chosen_colour)
    root.after(random.randint(60, 180), apply_crt_flicker)
apply_crt_flicker()

# Lift buttons to remain in canvas
meButton.lift()
closeButton.lift()
luckButton.lift()



# Music Logic
try:
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    messagebox.showerror("Music Fail", f"Failed to load background music: {str(e)}")


# Initialise main window
root.mainloop()
