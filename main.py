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
print_queue = []
is_printing = False
quiz_ready = False
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
    termText.configure(fg=chosen_colour)
    termEntry.configure(fg=chosen_colour)
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
def process_print_queue():
    global is_printing
    if not print_queue:
        is_printing = False
        return

    is_printing = True
    text_to_print = print_queue.pop(0)

    termText.config(state="normal")
    termText.insert("end", "\n")
    termText.config(state="disabled")

    def type_chars(remaining_text):
        termText.config(state="normal")
        if remaining_text:
            termText.insert("end", remaining_text[0])
            termText.see("end")
            termText.config(state="disabled")
            root.after(25, lambda: type_chars(remaining_text[1:]))
        else:
            termText.config(state="normal")
            if print_queue:
                pass
            else:
                termText.insert("end", "\n> ")
            termText.see("end")
            termText.config(state="disabled")
            process_print_queue()

    root.after(100, lambda: type_chars(text_to_print))

def print_term(text):
    global is_printing
    print_queue.append(text)
    if not is_printing:
        process_print_queue()


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
            player_output += f"- {player}\n"
        print_term(player_output.strip())

def show_questionlist():
    if not questions:
        print_term("No questions loaded! Use 'quiz question load' first! \n")
    else:
        question_output = "Question List:\n"
        for q in questions:
            question_output += f"- {q}\n"
        print_term(question_output.strip())

def preface_quiz():
    global quiz_ready
    msg = "Checking quiz requirements... \n"
    if questions and players:
        "Questions and players loaded... \nQuiz ready"
        quiz_ready = True
    elif questions and not players:
        msg += "Questions loaded \nPlayers still to be loaded"
        quiz_ready = False
    elif players and not questions:
        msg += "Players loaded \nQuestions still to be loaded"
        quiz_ready = False
    else:
        msg += "Nothing loaded \nPlease load files"
        quiz_ready = False
    print_term(msg)

def show_syntax():
    syn = "To use basic commands (such as 'rickroll' or 'exit'), just type the command. For more complex commands like 'quiz', type in 'quiz', followed by a space and then the next command suggested by 'Available commands'"
    print_term(syn)

quiz_setup_step = 0

def start_quiz_setup():
    global quiz_ready, quiz_setup_step
    if quiz_ready == False:
        print_term("Run 'quiz preface' first")
        return
    quiz_setup_step = 1
    print_term("-- QUIZ SETTINGS INITIALISATION --\nRandomise question order? (y/n):")





# Execute Terminal Commands
def execute_command(e=None):
    raw_cmd = termEntry.get().strip().lower()
    termEntry.delete(0, "end")

    termText.config(state="normal")
    termText.insert("end", f"{raw_cmd}")
    termText.config(state="disabled")

    sub_commands = [c.strip() for c in raw_cmd.split("&&") if c.strip()]

    # Command Dictionary
    commands = {
        "help": lambda: print_term("Commands: quiz, syntax, rickroll, luck, clear, cls, about, exit \n"),
        "quiz": lambda: (print_term("Available commands: player, question, start, preface \nCommands for this must start with 'quiz '\n"), termEntry.insert(tk.END, "quiz ")),
        "quiz preface": lambda: preface_quiz(),
        "quiz start": lambda: (print_term("Starting Quiz... \n"), start_quiz_setup),
        "quiz player": lambda: (print_term("Available commands: load, lookup \nCommands for this must start with 'quiz player '\n"), termEntry.insert(tk.END, "quiz player ")),
        "quiz question": lambda: (print_term("Available commands: load, lookup \nCommands for this must start with 'quiz question '\n"), termEntry.insert(tk.END, "quiz question ")),
        "quiz player load": lambda: (print_term("Loading playerlist.txt"), load_playerlist()),
        "quiz question load": lambda: (print_term("Loading questionlist.txt"), load_questionlist()),
        "quiz player lookup": lambda: (show_playerlist()),
        "quiz question lookup": lambda: (show_questionlist()),
        "syntax": lambda: (show_syntax()),
        "rickroll": lambda: (print_term("RICKROLL!"), webbrowser.open_new("https://www.youtube.com/watch?v=a7Lq6ZlSqys")),
        "luck": lambda: (print_term("Opening Lucky Gamble... \n"), testLuck()),
        "clear": lambda: (clear_term(), termText.insert("end", "CRT OS v1.0\nType 'help' for commands. \n\n> ")),
        "cls": lambda: (clear_term(), termText.insert("end", "CRT OS v1.0\nType 'help' for commands. \n\n> ")),
        "about": lambda: (print_term("Terra CRT App! \n"), openMePages()),
        "exit": root.destroy
    }

    for cmd in sub_commands:
        if cmd in commands:
            commands[cmd]()
        else:
            print_term(f"Unknown command: '{cmd}'. Type 'help' for a list of commands! \n")
            break

    def handle_quiz_setup_input(raw_cmd):
        global quiz_setup_step, quiz_settings
        if quiz_setup_step == 1:
            quiz_settings["rand_questions"] == (raw_cmd == 'y')
            quiz_setup_step = 2
            print_term("Randomise player order? (y/n):")
        elif quiz_setup_step == 2:
            quiz_settings["rand_players"] = (raw_cmd == 'y')
            quiz_setup_step = 3
            print_term("Enter time limit per question (seconds):")
        elif quiz_setup_step == 3:
            try:
                quiz_settings["time_limit"] = int(raw_cmd)
            except ValueError:
                quiz_settings["time_limit"] = 15
            quiz_setup_step = 4
            print_term("Enter default skips allowed per player:")
        elif quiz_setup_step == 4:
            try:
                quiz_settings["default_skips"] = int(raw_cmd)
            except ValueError:
                quiz_settings["default_skips"] = 2
            quiz_setup_step = 5
            print_term("Enable default last chance on timeout? (y/n):")
        elif quiz_setup_step == 5:
            quiz_settings["default_last_chance"] = (raw_cmd == 'y')
            quiz_setup_step = 0
            print_term("Settings applied. Starting quiz...")
            begin_quiz_execution()

    def begin_quiz_execution()











    


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

# Things/Ideas to add:
    # A syntax menu showing how to write commands
    # A command ask menu detailing how a command works
    # An optional AI to have it generate questions for you
    # Default player (Player 1, Player 2 etc.) and Questions files
    # More fun menus and commands
    # Actual quiz funstionality
    # The time in the corner
    # A new iconbitmap (and accompanying .png made in Aseprite - Terminal)
    # Put the app logo in more places
    # Suggest a feature command (takes to GitHub issue template)
    # Report a bug command (takes to GitHub issue template)
    # Disable/Enable scanline option
    # Disable/Enable text option
    # More ideas to come later!