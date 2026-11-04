import tkinter as tk
from tkinter import *
import sys
import os
from tkinter import font, messagebox, filedialog
from PIL import Image, ImageTk
import webbrowser
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
mainFontFamily = "Consolas"
bg_music_path = resource_path("bg_music.mp3")
players = []
questions = []


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


# CRT Effect
crt_canvas = tk.Canvas(root, width=rootWidth, height=rootHeight, bg=background_colour, highlightthickness=0)
crt_canvas.place(x=0, y=0, relwidth=1, relheight=1)

# Scan Lines
for y in range(0, rootHeight, 3):
    crt_canvas.create_line(0, y, rootWidth, y, fill="#001100", stipple="gray50", tags="scanlines")

# Moving Scanline
moving_scanline = crt_canvas.create_line(0, 0, rootWidth, 0, fill="#00FF44", width=10, stipple="gray25")
scanline_y = 0

def animate_crt_beam():
    global scanline_y
    scanline_y += 3
    if scanline_y > rootHeight:
        scanline_y = 0
    crt_canvas.coords(moving_scanline, 0, scanline_y, rootWidth, scanline_y)
    root.after(20, animate_crt_beam)
animate_crt_beam()


# CRT Flicker
def apply_crt_flicker():
    glow_colours = ["#00FF00", "#00DD00", "#22FF22", "#00EE00"]
    chosen_colour = random.choice(glow_colours)
    titleLabel.configure(fg=chosen_colour)
    root.after(random.randint(60, 180), apply_crt_flicker)



# Fonts
titleFont = font.Font(family=mainFontFamily, size=28, underline=True, weight="bold")
descFont = font.Font(family=mainFontFamily, size=14)
buttonFont = font.Font(family=mainFontFamily, size=17, underline=True)

# Widgets
titleLabel = tk.Label(root,
    text="THE CRT",
    font=titleFont,
    bg=background_colour,
    fg=foreground_colour,
    wraplength=(rootWidth-25),
    justify="center"
)
titleLabel.place(x=(rootWidth // 2), y=20, anchor="n")



# Gamble
def testLuck():
    luckPopup = tk.Toplevel(root)
    luckPopup.title("TEST YOUR LUCK...")
    luckPopup.geometry("300x300+150+150")
    luckPopup.resizable(False, False)
    luckPopup.configure(bg=background_colour)
    try:
        luckPopup.iconbitmap(app_icon)
    except:
        pass

    currentLuck = "FAIL!"

    luckLabel = tk.Label(luckPopup,
        text=currentLuck,
        font=titleFont,
        bg=background_colour,
        fg=foreground_colour,
        wraplength=250,
        justify="center"
    )
    luckLabel.place(x=150, y=125, anchor="n")

    def spin_luck():
        nonlocal currentLuck
        currentLuck = "WIN!" if currentLuck == "FAIL!" else "FAIL!"
        luckLabel.configure(text=currentLuck)
    
    currentRanNum = random.randint(5, 25)

    for i in range(currentRanNum):
        luckPopup.after(i * 100, spin_luck)

    def finish_luck():
        if currentLuck == "FAIL!":
            messagebox.showerror("You Failed", "You lost the gamble...")
            luckPopup.destroy()
            root.destroy()
        else:
            messagebox.showinfo("You Win", "Your gamble paid off!")
            luckPopup.destroy()

    luckPopup.after(((currentRanNum * 100) + 100), finish_luck)


def openMePages():
    webbrowser.open_new("https://github.com/sadgituser")
    webbrowser.open_new_tab("https://theprintedcraftuk.etsy.com")
    webbrowser.open_new_tab("mailto:kavi@mistrypi.dev")


# Terminal Output Box
termText = tk.Text(root, 
    bg="#000500", 
    fg=foreground_colour, 
    insertbackground=foreground_colour, 
    font=descFont, 
    relief="flat"
)
termText.place(x=15, y=80, width=(rootWidth - 30), height=(rootHeight - 200))
termText.insert("end", "CRT OS v1.0\nType 'help' for commands. \n\n> ")
termText.config(state="disabled")

# Terminal Entry
promptLabel = tk.Label(root, 
    text=">",
    font=descFont,
    bg=background_colour,
    fg=foreground_colour
)
promptLabel.place(x=15, y=(rootHeight - 55))

termEntry = tk.Entry(root,
    bg=background_colour,
    fg=foreground_colour,
    insertbackground=foreground_colour,
    font=descFont,
    relief="flat",
    highlightthickness=1,
    highlightbackground=foreground_colour
)
termEntry.place(x=35, y=(rootHeight - 55), width=(rootWidth - 50), height=30)
termEntry.focus()

# Print to the Terminal
def print_term(text):
    termText.config(state="normal")
    termText.insert("end", "\n")
    termText.config(state="disabled")

    def type_chars(remaining_text):
        termText.config(state="normal")
        if remaining_text:
            termText.insert("end", remaining_text[0])
            termText.see("end")
            termText.config(state="disabled")
            root.after(30, lambda: type_chars(remaining_text[1:]))
        else:
            termText.insert("end", "\n> ")
            termText.see("end")
            termText.config(state="disabled")

    root.after(1000, lambda: type_chars(text))


# Terminal Commands
def clear_term():
    termText.config(state="normal")
    termText.delete("1.0", "end")
    termText.config(state="disabled")
    print_term("")

def load_playerlist():
    global players
    filepath = filedialog.askopenfilename(title = "Select the playerlist.txt file!", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, "r") as f:
                players = [line.strip() for line in f if line.strip()]
            print_term(f"Successfully loaded {len(players)} players! \n")
        except Exception as e:
            print_term(f"Failed to load player list: {e} \n")

def load_questionlist():
    global questions
    filepath = filedialog.askopenfilename(title="Select the questionslist.txt file!", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, "r") as f:
                questions = [line.strip() for line in f if line.strip()]
            print_term(f"Successfully loaded {len(questions)} questions! \n")
        except Exception as e:
            print_term(f"Failed to load question list: {e} \n")

def show_playerlist():
    if not players:
        print_term("No players loaded! Use 'quiz player load' first! \n")
    else:
        player_output = "Player List:\n"
        for player in players:
            player_output != f"- {player}\n"
        print_term(player_output.strip(), "\n")

def show_questionlist():
    if not questions:
        print_term("No questions loaded! Use 'quiz question load' first! \n")
    else:
        question_output = "Question List:\n"
        for q in questions:
            question_output += f"- {q}\n"
        print_term(question_output.strip(), "\n")


# Execute Terminal Commands
def execute_command(e=None):
    cmd = termEntry.get().strip().lower()
    termEntry.delete(0, "end")

    termText.config(state="normal")
    termText.insert("end", f"{cmd}")
    termText.config(state="disabled")

    # Command Dictionary
    commands = {
        "help": lambda: print_term("Commands: quiz, rickroll, luck, clear, about, exit \n"),
        "quiz": lambda: print_term("Available commands: player, question, start, preface \n"),
        "quiz preface": lambda: (print_term("Checking Quiz Requirements... (Coming Soon!)")),
        "quiz start": (lambda: print_term("Starting Quiz... (Coming Soon!)")),
        "quiz player": lambda: (print_term("Available commands: load, lookup")),
        "quiz question": lambda: (print_term("Available commands: load, lookup")),
        "quiz player load": lambda: (print_term("Loading playerlist.txt"), load_playerlist()),
        "quiz question load": lambda: (print_term("Loading questionlist.txt"), load_questionlist()),
        "quiz player lookup": lambda: (show_playerlist()),
        "quiz question lookup": lambda: (show_questionlist()),
        "rickroll": lambda: (print_term("RICKROLL"), webbrowser.open_new("https://www.youtube.com/watch?v=a7Lq6ZlSqys")),
        "luck": lambda: (print_term("Opening Lucky Gamble... \n"), testLuck()),
        "clear": lambda: clear_term(),
        "cls": lambda: clear_term(),
        "about": lambda: (print_term("Terra CRT App! \n"), openMePages()),
        "exit": root.destroy
    }

    if cmd in commands:
        commands[cmd]()
    else:
        print_term(f"Unknown command: '{cmd}'. Type 'help' for a list of commands! \n")
    



# Music Logic
try:
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    messagebox.showerror("Music Fail", f"Failed to load background music: {str(e)}")


# Initialise main window
apply_crt_flicker()
termEntry.bind("<Return>", execute_command)
root.mainloop()
