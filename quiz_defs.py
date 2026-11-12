import tkinter as tk
from tkinter import font, messagebox, filedialog
import webbrowser
import random
import time
import pygame
import stateVars

# Early defs in main.py
def resource_path(relative_path):
    import sys, os
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "Assets", relative_path)

# CRT
def animate_crt_beam():
    stateVars.scanline_y += 3
    if stateVars.scanline_y > stateVars.rootHeight:
        stateVars.scanline_y = 0
    stateVars.crt_canvas.coords(stateVars.moving_scanline, 0, stateVars.scanline_y, stateVars.rootWidth, stateVars.scanline_y)
    stateVars.root.after(20, animate_crt_beam)

def update_clock():
    current_time = time.strftime("%H:%M:%S")
    stateVars.clockLabel.config(text=current_time)
    stateVars.root.after(500, update_clock)

def apply_crt_flicker():
    glow_colours = ["#00FF00", "#00DD00", "#22FF22", "#00EE00", "#00BB00"]
    chosen_colour = random.choice(glow_colours)
    stateVars.titleLabel.configure(fg=chosen_colour)
    stateVars.termText.configure(fg=chosen_colour)
    stateVars.termEntry.configure(fg=chosen_colour)
    stateVars.root.after(random.randint(60, 180), apply_crt_flicker)

# Gamble
def testLuck():
    luckPopup = tk.Toplevel(stateVars.root)
    luckPopup.title("TEST YOUR LUCK...")
    luckPopup.geometry("300x300+175+175")
    luckPopup.resizable(False, False)
    luckPopup.configure(bg=stateVars.background_colour)
    try:
        luckPopup.iconbitmap(stateVars.app_icon)
    except:
        pass

    currentLuck = "FAIL!"
    titleFont = font.Font(family=stateVars.mainFontFamily, size=28, underline=True, weight="bold")
    luckLabel = tk.Label(luckPopup,
        text=currentLuck,
        font=titleFont,
        bg=stateVars.background_colour,
        fg=stateVars.foreground_colour,
        wraplength=250,
        justify="center"
    )
    luckLabel.place(x=150, y=125, anchor="n")

    def spin_luck():
        nonlocal currentLuck
        currentLuck = "WIN!" if currentLuck == "FAIL!" else "FAIL!"
        luckLabel.configure(text=currentLuck)

    currentRanNum = random.randint(10, 30)
    for i in range(currentRanNum):
        luckPopup.after(i * 100, spin_luck)

    def finish_luck():
        if currentLuck == "FAIL!":
            messagebox.showerror("You Failed!", "You lost the gamble... pay the price...")
            luckPopup.destroy()
            stateVars.root.destroy()
        else:
            messagebox.showinfo("You Win!", "Your gamble paid off! You get...")
            messagebox.showinfo("Your Prize!", "NOTHING! :o")
            luckPopup.destroy()

    luckPopup.after(((currentRanNum * 100) + 100), finish_luck)

# About Me
def openMePages():
    webbrowser.open_new("https://github.com/sadgituser")
    webbrowser.open_new("https://theprintedcraftuk.etsy.com")
    webbrowser.open_new("mailto:kavi@mistrypi.dev")

# Text on stateVars.termText
def process_print_queue():
    if not stateVars.print_queue:
        stateVars.is_printing = False
        return

    stateVars.is_printing = False
    text_to_print = stateVars.print_queue.pop(0)
    stateVars.termText.config(state="normal")
    stateVars.termText.insert("end", "\n")
    stateVars.termText.config(state="disabled")

    def type_chars(remaining_text):
        stateVars.termText.config(state="normal")
        if remaining_text:
            stateVars.termText.insert("end", remaining_text[0])
            stateVars.termText.see("end")
            stateVars.termText.config(state="disabled")
            stateVars.root.after(25, lambda: type_chars(remaining_text[1:]))
        else:
            stateVars.termText.config(state="normal")
            if stateVars.print_queue:
                pass
            else:
                stateVars.termText.insert("end", "\n> ")
            stateVars.termText.see("end")
            stateVars.termText.config(state="disabled")
            process_print_queue()

    stateVars.root.after(100, lambda: type_chars(text_to_print))

def print_term(text):
    stateVars.print_queue.append(text)
    if not stateVars.is_printing:
        process_print_queue()

# Terminal commands
def clear_term():
    stateVars.termText.config(state="normal")
    stateVars.termText.delete("1.0", "end")
    stateVars.termText.config(state="disabled")
    print_term("")

def load_playerlist():
    filepath = filedialog.askopenfilename(title="Select the playerlist.txt file!", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, "r") as f:
                stateVars.players = [line.strip() for line in f if line.strip()]
            print_term(f"Successfully loaded {len(stateVars.players)} players! \n")
        except Exception as e:
            print_term(f"Failed to load player list: {str(e)} \n")

def load_questionlist():
    filepath = filedialog.askopenfilename(title="Select the question.txt file!", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, "r") as f:
                stateVars.questions = [line.strip() for line in f if line.strip()]
                print_term(f"Successfully loaded {len(stateVars.questions)} questions! \n")
        except Exception as e:
            print_term(f"Failed to load question list: {str(e)} \n")

def show_playerlist():
    if not stateVars.players:
        print_term("No players loaded! Use 'quiz player load' first! \n")
    else:
        player_output = "Player List:\n\n"
        for player in stateVars.players:
            player_output += f"- {player}\n"
        print_term(player_output.strip())

def show_questionlist():
    if not stateVars.questions:
        print_term("No questions loaded! Use 'quiz question load' first! \n")
    else:
        question_output = "Question List:\n\n"
        for question in stateVars.questions:
            question_output += f"- {question}\n"
        print_term(question_output.strip())

def preface_quiz():
    msg = "Checking quiz requirements... \n"
    if stateVars.questions and stateVars.players:
        msg += "Players and questions loaded... \nQuiz ready\n"
        stateVars.quiz_ready = True
    elif stateVars.questions and not stateVars.players:
        msg += "Questions loaded \nPlayers still to be loaded, load players with 'quiz player load' or 'quiz player dfault' for default players\n"
        stateVars.quiz_ready = False
    elif stateVars.players and not stateVars.questions:
        msg += "Players loaded \nQuestions still to be loaded, load questions with 'quiz question load' or 'quiz question default' for default questions\n"
        stateVars.quiz_ready = False
    else:
        msg += "Nothing loaded\nPlease load files by typing 'quiz player load' or 'quiz question load'... Replace load with 'default' if you want to use the defaults\n"
        stateVars.quiz_ready = False
    print_term(msg)

def show_syntax():
    syn = "To use basic commands (such as 'rickroll' or 'exit'), just type the command. For more complex commands like 'quiz', type in 'quiz', followed by a space and then the next command suggested by 'Available commands' or what the program suggests for you to do!"
    print_term(syn)


# Quiz components
def start_quiz_setup():
    if stateVars.quiz_ready == False:
        print_term("Run 'quiz preface' first\n")
        return
    stateVars.quiz_setup_step = 1
    print_term("-- QUIZ SETTINGS --\nRandomise question order (y/n): ")

def toggle_pause():
    if stateVars.waiting_for_next:
        return
    stateVars.is_paused = not stateVars.is_paused
    if stateVars.is_paused:
        if stateVars.current_timer_id:
            stateVars.root.after_cancel(stateVars.current_timer_id)
            stateVars.current_timer_id = None
        stateVars.quizPauseButton.config(text="RESUME")
    else:
        stateVars.quizPauseButton.config(text="PAUSE")
        stateVars.current_timer_id = stateVars.root.after(1000, update_quiz_timer)

def force_quit_quiz():
    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None
    if stateVars.intro_timer_id:
        stateVars.root.after_cancel(stateVars.intro_timer_id)
        stateVars.intro_timer_id = None
    stateVars.waiting_for_next = False
    stateVars.is_paused = False
    stateVars.quiz_setup_step = 0
    stateVars.root.unbind("<Key>")
    reset_screen_colours()
    stateVars.quizPlayerLabel.place_forget()
    stateVars.quizQuestionLabel.place_forget()
    stateVars.quizTimerLabel.place_forget()
    stateVars.quizStatusLabel.place_forget()
    stateVars.quizPauseButton.place_forget()
    stateVars.quizQuitButton.place_forget()
    stateVars.titleLabel.place(x=(stateVars.rootWidth // 2), y=20, anchor="n")
    stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="normal")
    pygame.mixer.music.set_volume(0.3)
    show_terminal_from_quiz()
    print_term("Quiz force quit by user \n")

def load_default_players():
    stateVars.players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7", "Player 8", "Player 9", "Player 10"]
    print_term(f"Loaded {len(stateVars.players)} default players! \n")

def load_default_questions():
    stateVars.questions = ["What is the largest mammal on Earth?", 
        "Who wrote 'Romeo and Juliet'?", 
        "What is the chemical symbol for gold?", 
        "Which ocean is the largest?", 
        "What is 12 x 8?", 
        "Who painted the Mona Lisa?", 
        "What is the boiling point of water in degrees Celsius?", 
        "Which country is home to the Great Pyramid of Giza?", 
        "What is the fastest land animal?", 
        "Who invented the telephone?", 
        "What is the square root of 144?", 
        "Which gas do plants absorb from the atmosphere?", 
        "What is the smallest prime number?", 
        "Who was the first person to walk on the Moon?", 
        "Which continent is the Sahara Desert located on?", 
        "What is the capital of Japan?", 
        "How many bones are in the adult human body?", 
        "Which planet is closest to the Sun?", 
        "What is the hardest natural substance?", 
        "Who discovered gravity after observing a falling apple?", 
        "What is the largest continent?", 
        "How many days are there in a leap year?", 
        "What is the currency of the United Kingdom?", 
        "Which element has the chemical symbol O?", 
        "What is the tallest mountain in the world?", 
        "Who wrote 'Harry Potter'?", 
        "How many colours are there in a rainbow?", 
        "What is the capital city of Australia?", 
        "Which bird is often associated with delivering babies in stories?", 
        "What is the freezing point of water in degrees Celsius?", 
        "Which organ pumps blood around the human body?", 
        "What is the longest river in the world?", 
        "Who painted the ceiling of the Sistine Chapel?", 
        "Which country invented pizza?", 
        "What is the largest planet in the Solar System?", 
        "How many minutes are in one hour?", 
        "What is the chemical symbol for silver?", 
        "Who was the first President of the United States?", 
        "What is the capital of Canada?", 
        "Which instrument has 88 keys?", 
        "What is the tallest animal in the world?", 
        "Which planet has rings that are clearly visible from Earth?", 
        "What is the primary language spoken in Brazil?", 
        "What is 15 squared?", 
        "Who wrote 'The Hobbit'?", 
        "Which metal is liquid at room temperature?", 
        "What is the largest species of shark?", 
        "What is the national sport of Japan?", 
        "Which country is famous for the Eiffel Tower?", 
        "What is the value of Pi rounded to two decimal places?", 
        "How many continents are there on Earth?", 
        "What is the largest desert in the world?", 
        "Who developed the theory of relativity?", 
        "What is the capital of Spain?", 
        "Which planet is known for its Great Red Spot?", 
        "What is the name of the galaxy that contains our Solar System?", 
        "How many players are on a standard football (soccer) team on the field?", 
        "What is the world's most abundant gas?", 
        "Who painted 'Starry Night'?", 
        "What is the capital of Germany?", 
        "How many strings does a standard guitar have?"]
    print_term(f"Loaded {len(stateVars.questions)} default questions! \n")

def handle_quiz_setup_input(raw_cmd):
    if stateVars.quiz_setup_step == 1:
        stateVars.quiz_settings['rand_questions'] = (raw_cmd == 'y')
        stateVars.quiz_setup_step = 2
        print_term("Randomise player order? (y/n):")
    elif stateVars.quiz_setup_step == 2:
        stateVars.quiz_settings['rand_players'] = (raw_cmd == 'y')
        stateVars.quiz_setup_step = 3
        print_term("Enter time limit per question (seconds - applies to all questions):")
    elif stateVars.quiz_setup_step == 3:
        try:
            stateVars.quiz_settings['time_limit'] = int(raw_cmd)
        except ValueError:
            stateVars.quiz_settings['time_limit'] = 15
        stateVars.quiz_setup_step = 4
        print_term("Enter default skips allowed per player: ")
    elif stateVars.quiz_setup_step == 4:
        try:
            stateVars.quiz_settings['default_skips'] = int(raw_cmd)
        except ValueError:
            stateVars.quiz_settings['default_skips'] = 2
        stateVars.quiz_setup_step = 5
        print_term("Enable default last chance on timeout? (y/n):")
    elif stateVars.quiz_setup_step == 5:
        stateVars.quiz_settings['default_last_chance'] = (raw_cmd == 'y')
        stateVars.quiz_setup_step = 0
        print_term("Settings applied. Starting quiz... \n")
        begin_quiz_execution()

def begin_quiz_execution():
    pygame.mixer.music.set_volume(0.1)
    stateVars.quiz_active_players = [{
        "name": p,
        "skips": stateVars.quiz_settings['default_skips'],
        "eliminated": False,
        "last_chance": False
    } for p in stateVars.players]

    if stateVars.quiz_settings['rand_players']:
        random.shuffle(stateVars.quiz_active_players)

    if stateVars.quiz_settings['rand_questions']:
        random.shuffle(stateVars.quiz_active_questions)

    stateVars.current_player_idx = 0
    stateVars.current_question_idx = 0

    hide_terminal_for_quiz()
    show_next_quiz_turn()

def hide_terminal_for_quiz():
    stateVars.termText.place_forget()
    stateVars.promptLabel.place_forget()
    stateVars.termEntry.place_forget()
    stateVars.crt_canvas.itemconfigure("scanlines", state="hidden")
    stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="hidden")
    stateVars.root.focus_set()

def show_terminal_from_quiz():
    stateVars.termText.place(x=15, y=80, width=(stateVars.rootWidth - 30), height=(stateVars.rootHeight - 200))
    stateVars.promptLabel.place(x=15, y=(stateVars.rootHeight - 55))
    stateVars.termEntry.place(x=35, y=(stateVars.rootHeight - 55), width=(stateVars.rootWidth - 50), height=30)
    stateVars.crt_canvas.itemconfigure("scanlines", state="normal")
    stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="normal")
    stateVars.termEntry.focus()

def show_next_quiz_turn():
    stateVars.waiting_for_next = False
    stateVars.is_paused = False

    if stateVars.intro_timer_id:
        stateVars.root.after_cancel(stateVars.intro_timer_id)
        stateVars.intro_timer_id = None
    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None

    stateVars.quizPauseButton.config(text="PAUSE")

    active_remaining = [p for p in stateVars.quiz_active_players if not p['eliminated']]
    if len(active_remaining) == 1:
        show_winner_screen(active_remaining[0]['name'])
        return
    elif not active_remaining:
        end_quiz("Quiz Over! All players eliminated!")
        return

    if stateVars.current_question_idx >= len(stateVars.quiz_active_questions):
        stateVars.current_question_idx = 0
        if stateVars.quiz_settings['rand_questions']:
            random.shuffle(stateVars.quiz_active_questions)

    while stateVars.quiz_active_players[stateVars.current_player_idx]['eliminated']:
        stateVars.current_player_idx = (stateVars.current_player_idx + 1) % len(stateVars.quiz_active_players)

    player = stateVars.quiz_active_players[stateVars.current_player_idx]
    
    stateVars.titleLabel.place_forget()
    stateVars.quizQuestionLabel.place_forget()
    stateVars.quizTimerLabel.place_forget()
    stateVars.quizPauseButton.place_forget()
    stateVars.quizQuitButton.place_forget()

    playerFont = font.Font(family=stateVars.mainFontFamily, size=48, weight="bold", underline=True)
    statusFont = font.Font(family=stateVars.mainFontFamily, size=17)

    stateVars.quizPlayerLabel.config(text=player['name'], fg=stateVars.foreground_colour, font=playerFont)
    stateVars.quizPlayerLabel.place(x=(stateVars.rootWidth // 2), y=30, anchor="n")

    status_text = f"Skips Left: {player['skips']}"
    if stateVars.quiz_settings['default_last_chance']:
        status_text += f" | Last Chance: {'FINAL CHANCE' if player['last_chance'] else 'NO'}"
    stateVars.quizStatusLabel.config(text=status_text, fg=stateVars.foreground_colour, font=statusFont)
    stateVars.quizStatusLabel.place(x=(stateVars.rootWidth // 2), y=150, anchor="n")

    stateVars.root.unbind("<Key>")
    stateVars.root.after(3000, start_actual_question)

def start_actual_question():
    player = stateVars.quiz_active_players[stateVars.current_player_idx]
    question = stateVars.quiz_active_questions[stateVars.current_question_idx]

    playerFont = font.Font(family=stateVars.mainFontFamily, size=48, weight="bold", underline=True)
    statusFont = font.Font(family=stateVars.mainFontFamily, size=17)
    questionFont = font.Font(family=mainFontFamily, size=24, weight="bold")
    timerFont = font.Font(family=mainFontFamily, size=18, weight="bold")

    stateVars.quizPlayerLabel.config(text=player['name'], fg=stateVars.foreground_colour, font=playerFont)
    stateVars.quizPlayerLabel.place(x=(stateVars.rootWidth // 2), y=15, anchor="n")
    stateVars.quizQuestionLabel.config(text=question, fg=stateVars.foreground_colour, font=questionFont)
    stateVars.quizQuestionLabel.place(x=(stateVars.rootWidth // 2), y=120, anchor="n")

    status_text = f"Skips Left: {player['skips']}"
    if stateVars.quiz_settings['default_last_chance']:
        status_text += f" | Last Chance: {'FINAL CHANCE' if player['last_chance'] else 'NO'}"
    stateVars.quizStatusLabel.config(text=status_text, fg=stateVars.foreground_colour, font=statusFont)
    stateVars.quizStatusLabel.place(x=(stateVars.rootWidth // 2), y=330, anchor="n")

    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None

    time_remaining = stateVars.quiz_settings['time_limit']
    stateVars.quizTimerLabel.config(text=f"Time: {time_remaining}s", fg=stateVars.foreground_colour, font=timerFont)
    stateVars.quizTimerLabel.place(x=(stateVars.rootWidth // 2), y=410, anchor="n")

    stateVars.quizPauseButton.place(x=(stateVars.rootWidth // 2 - 110), y=500, width=100, height=40)
    stateVars.quizQuitButton.place(x=(stateVars.rootWidth // 2 + 10), y=500, width=100, height=40)

    stateVars.root.bind("<Key>", handle_quiz_keypress)
    stateVars.current_timer_id = stateVars.root.after(1000, update_quiz_timer)

def update_quiz_timer():
    if stateVars.waiting_for_next or stateVars.is_paused:
        return
    if stateVars.time_remaining > 0:
        stateVars.time_remaining -= 1
        stateVars.quizTimerLabel.config(f"Time: {stateVars.time_remaining}s")
        stateVars.current_timer_id = stateVars.root.after(1000, update_quiz_timer)
    else:
        handle_timeout()

def handle_timeout():
    player = stateVars.quiz_active_players[stateVars.current_player_idx]
    flash_screen("#FFA500", "TIME OUT")
    if stateVars.quiz_settings['default_last_chance'] and not player['last_chance']:
        player['last_chance'] = True
    else:
        player['eliminated'] = True
    prepare_for_next_turn()

def flash_screen(colour, message):
    stateVars.waiting_for_next = True
    if current_timer_id:
        root.after_cancel(current_timer_id)
        current_timer_id = None
    
    root.configure(bg=colour)
    crt_canvas.configure(bg=colour)
    quizPlayerLabel.config(bg=colour, fg="#000000")
    quizQuestionLabel.config(bg=colour, fg="#000000", font=winnerFont)
    quizTimerLabel.config(bg=colour, fg="#000000")
    quizStatusLabel.config(bg=colour, fg="#000000")
    quizPauseButton.place_forget()
    quizQuitButton.place_forget()
    
    quizQuestionLabel.config(text=message)