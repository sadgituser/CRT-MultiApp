import tkinter as tk
from tkinter import font, messagebox, filedialog
import webbrowser
import random
import time
import os
import stateVars
import config_manager


# Early defs in main.py
def resource_path(relative_path):
    import sys, os
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "Assets", relative_path)


# Command History Management
def load_saved_history():
    stateVars.command_history = config_manager.load_command_history(stateVars.config)[-7:]

    stateVars.history_index = len(stateVars.command_history)
    stateVars.current_input = ""

def save_entered_command(command):
    command = command.strip()

    if not command:
        return 

    stateVars.command_history.append(command)
    stateVars.command_history = stateVars.command_history[-7:]

    config_manager.save_command_history(
        stateVars.config,
        stateVars.command_history

    )

    stateVars.history_index = len(stateVars.command_history)

def history_up(event=None):
    history = stateVars.command_history

    if not history:
        return "break"

    if stateVars.history_index == len(history):
        stateVars.current_input = stateVars.termEntry.get()

    if stateVars.history_index > 0:
        stateVars.history_index -= 1

    stateVars.termEntry.delete(0, tk.END)
    stateVars.termEntry.insert(0, history[stateVars.history_index])

    return "break"

def history_down(event=None):
    history = stateVars.command_history

    if not history:
        return "break"

    if stateVars.history_index < len(history) - 1:
        stateVars.history_index += 1
        command = history[stateVars.history_index]
    else:
        stateVars.history_index = len(history)
        command = stateVars.current_input

    stateVars.termEntry.delete(0, tk.END)
    stateVars.termEntry.insert(0, command)

    return "break"


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


flicker = None

def apply_crt_flicker():
    global flicker
    preset_name = stateVars.colour_preset_names[stateVars.current_colour_index]
    glow_colours = stateVars.colour_presets[preset_name]
    chosen_colour = random.choice(glow_colours)
    stateVars.titleLabel.configure(fg=chosen_colour)
    stateVars.termText.configure(fg=chosen_colour)
    stateVars.termEntry.configure(fg=chosen_colour)
    flicker = stateVars.root.after(random.randint(10, 100), apply_crt_flicker)

def stop_crt_flicker():
    global flicker
    if flicker is not None:
        stateVars.root.after_cancel(flicker)
        flicker = None
    stateVars.titleLabel.configure(fg=stateVars.foreground_colour)
    stateVars.termText.configure(fg=stateVars.foreground_colour)
    stateVars.termEntry.configure(fg=stateVars.foreground_colour)

def change_colour():
    stateVars.current_colour_index = (stateVars.current_colour_index + 1) % len(stateVars.colour_preset_names)
    preset_name = stateVars.colour_preset_names[stateVars.current_colour_index]
    stateVars.foreground_colour = stateVars.colour_presets[preset_name][0]

    stateVars.clockLabel.configure(fg=stateVars.foreground_colour)
    stateVars.promptLabel.configure(fg=stateVars.foreground_colour)
    stateVars.termEntry.configure(
        fg=stateVars.foreground_colour,
        insertbackground=stateVars.foreground_colour,
        highlightbackground=stateVars.foreground_colour
    )
    stateVars.termText.configure(insertbackground=stateVars.foreground_colour)
    print_term(f"Colour preset changed to {preset_name}\n")

def set_speed(typingSpeed):
    stateVars.typeSpeed = typingSpeed

def prompt_custom_speed():
    stateVars.waiting_for_custom_speed = True
    print_term("Enter custom typing delay in ms (e.g. 5 to 200):")

def handle_custom_speed_input(raw_cmd):
    stateVars.waiting_for_custom_speed = False
    try:
        speed_ms = int(raw_cmd)
        if speed_ms < 1:
            raise ValueError("Speed must be positive")
        set_speed(speed_ms)
        print_term(f"Custom speed set to {speed_ms}ms")
    except ValueError:
        print_term("Invalid number. Keeping current speed.")



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
    luckLabel = tk.Label(luckPopup,
        text=currentLuck,
        font=stateVars.titleFont,
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
    webbrowser.open_new("https://github.com/sadgituser/CRT-MultiApp")
    webbrowser.open_new("https://theprintedcraftuk.etsy.com")
    webbrowser.open_new("mailto:kavi@mistrypi.dev")

# Text on stateVars.termText
def process_print_queue():
    if not stateVars.print_queue:
        stateVars.is_printing = False
        return

    stateVars.is_printing = True
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
            stateVars.root.after(stateVars.typeSpeed, lambda: type_chars(remaining_text[1:]))
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
    stateVars.termText.insert("end", f"CRT OS v{stateVars.versionNum}\nType 'help' for commands. \n\n> ")
    stateVars.termText.config(state="disabled")

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
        msg += "Questions loaded \nPlayers still to be loaded, load players with 'quiz player load' or 'quiz player default' for default players\n"
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
        stateVars.quizQuestionLabel.config(text="QUESTION HIDDEN!")
        stateVars.quizPauseButton.config(text="RESUME")
    else:
        current_question = stateVars.quiz_active_questions[stateVars.current_question_idx]
        stateVars.quizQuestionLabel.config(text=current_question)
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
            stateVars.quiz_settings['default_skips'] = 1
        stateVars.quiz_setup_step = 5
        print_term("Enable default last chance on timeout? (y/n):")
    elif stateVars.quiz_setup_step == 5:
        stateVars.quiz_settings['default_last_chance'] = (raw_cmd == 'y')
        stateVars.quiz_setup_step = 0
        print_term("Settings applied. Starting quiz... \n")
        begin_quiz_execution()

def begin_quiz_execution():
    stateVars.quiz_active_players = [{
        "name": p,
        "skips": stateVars.quiz_settings['default_skips'],
        "eliminated": False,
        "last_chance": False
    } for p in stateVars.players]

    if stateVars.quiz_settings['rand_players']:
        random.shuffle(stateVars.quiz_active_players)
    
    stateVars.quiz_active_questions = list(stateVars.questions)
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
    stateVars.termText.place(x=15, y=80, width=(stateVars.rootWidth - 30), height=(stateVars.rootHeight - 150))
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


    stateVars.quizPlayerLabel.config(text=player['name'], fg=stateVars.foreground_colour, font=stateVars.playerFont)
    stateVars.quizPlayerLabel.place(x=(stateVars.rootWidth // 2), y=30, anchor="n")

    status_text = f"Skips Left: {player['skips']}"
    if stateVars.quiz_settings['default_last_chance']:
        status_text += f" | Last Chance: {'FINAL CHANCE' if player['last_chance'] else 'NO'}"
    stateVars.quizStatusLabel.config(text=status_text, fg=stateVars.foreground_colour, font=stateVars.statusFont)
    stateVars.quizStatusLabel.place(x=(stateVars.rootWidth // 2), y=150, anchor="n")

    stateVars.root.unbind("<Key>")
    stateVars.root.after(3000, start_actual_question)

def start_actual_question():
    player = stateVars.quiz_active_players[stateVars.current_player_idx]
    question = stateVars.quiz_active_questions[stateVars.current_question_idx]

    stateVars.quizPlayerLabel.config(text=player['name'], fg=stateVars.foreground_colour, font=stateVars.playerFont)
    stateVars.quizPlayerLabel.place(x=(stateVars.rootWidth // 2), y=15, anchor="n")
    stateVars.quizQuestionLabel.config(text=question, fg=stateVars.foreground_colour, font=stateVars.questionFont)
    stateVars.quizQuestionLabel.place(x=(stateVars.rootWidth // 2), y=120, anchor="n")

    status_text = f"Skips Left: {player['skips']}"
    if stateVars.quiz_settings['default_last_chance']:
        status_text += f" | Last Chance: {'FINAL CHANCE' if player['last_chance'] else 'NO'}"
    stateVars.quizStatusLabel.config(text=status_text, fg=stateVars.foreground_colour, font=stateVars.statusFont)
    stateVars.quizStatusLabel.place(x=(stateVars.rootWidth // 2), y=330, anchor="n")

    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None

    stateVars.time_remaining = stateVars.quiz_settings['time_limit']
    stateVars.quizTimerLabel.config(text=f"Time Remaining: {stateVars.time_remaining}s", fg=stateVars.foreground_colour, font=stateVars.timerFont)
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
        stateVars.quizTimerLabel.config(text=f"Time Remaining: {stateVars.time_remaining}s")
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
    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None
    
    stateVars.root.configure(bg=colour)
    stateVars.crt_canvas.configure(bg=colour)
    stateVars.quizPlayerLabel.config(bg=colour, fg="#000000")
    stateVars.quizQuestionLabel.config(bg=colour, fg="#000000", font=stateVars.winnerFont)
    stateVars.quizTimerLabel.config(bg=colour, fg="#000000")
    stateVars.quizStatusLabel.config(bg=colour, fg="#000000")
    stateVars.clockLabel.config(bg=colour, fg="#000000")
    stateVars.quizPauseButton.place_forget()
    stateVars.quizQuitButton.place_forget()
    
    stateVars.quizQuestionLabel.config(text=message)

def prepare_for_next_turn():
    stateVars.waiting_for_next = True

def reset_screen_colours():
    stateVars.root.configure(bg=stateVars.background_colour)
    stateVars.crt_canvas.configure(bg=stateVars.background_colour)
    stateVars.quizPlayerLabel.config(bg=stateVars.background_colour, fg=stateVars.foreground_colour, font=stateVars.playerFont)
    stateVars.quizQuestionLabel.config(bg=stateVars.background_colour, fg=stateVars.foreground_colour, font=stateVars.questionFont)
    stateVars.quizTimerLabel.config(bg=stateVars.background_colour, fg=stateVars.foreground_colour, font=stateVars.timerFont)
    stateVars.quizStatusLabel.config(bg=stateVars.background_colour, fg=stateVars.foreground_colour, font=stateVars.statusFont)
    stateVars.clockLabel.config(bg=stateVars.background_colour, fg=stateVars.foreground_colour, font=stateVars.descFont)

def handle_quiz_keypress(event):
    player = stateVars.quiz_active_players[stateVars.current_player_idx]
    key = event.char.lower()

    if stateVars.waiting_for_next:
        if key == 'n':
            reset_screen_colours()
            if stateVars.is_last_chance_action:
                stateVars.is_last_chance_action = False
                stateVars.waiting_for_next = False
                stateVars.quizPlayerLabel.config(text=player['name'], fg=stateVars.foreground_colour, font=stateVars.playerFont)
                stateVars.quizPlayerLabel.place(x=(stateVars.rootWidth // 2), y=15, anchor="n")
                stateVars.quizQuestionLabel.config(text=stateVars.quiz_active_questions[stateVars.current_question_idx], fg=stateVars.foreground_colour, font=stateVars.questionFont)
                stateVars.quizQuestionLabel.place(x=(stateVars.rootWidth // 2), y=120, anchor="n")

                status_text = f"Skips Left: {player['skips']}"
                if stateVars.quiz_settings['default_last_chance']:
                    status_text += f" | Last Chance: {'FINAL CHANCE' if player['last_chance'] else 'NO'}"
                stateVars.quizStatusLabel.config(text=status_text, fg=stateVars.foreground_colour, font=stateVars.statusFont)
                stateVars.quizStatusLabel.place(x=(stateVars.rootWidth // 2), y=330, anchor="n")

                stateVars.quizTimerLabel.config(text=f"Time Remaining: {stateVars.time_remaining}s", fg=stateVars.foreground_colour, font=stateVars.timerFont)
                stateVars.quizTimerLabel.place(x=(stateVars.rootWidth // 2), y=410, anchor="n")

                stateVars.quizPauseButton.place(x=(stateVars.rootWidth // 2 - 110), y=500, width=100, height=40)
                stateVars.quizQuitButton.place(x=(stateVars.rootWidth // 2 + 10), y=500, width=100, height=40)

                stateVars.root.bind("<Key>", handle_quiz_keypress)
                if stateVars.current_timer_id:
                    stateVars.root.after_cancel(stateVars.current_timer_id)
                stateVars.current_timer_id = stateVars.root.after(1000, update_quiz_timer)
            else:
                stateVars.quizPlayerLabel.place_forget()
                stateVars.quizQuestionLabel.place_forget()
                stateVars.quizTimerLabel.place_forget()
                stateVars.quizStatusLabel.place_forget()
                stateVars.quizPauseButton.place_forget()
                stateVars.quizQuitButton.place_forget()
                stateVars.titleLabel.place(x=(stateVars.rootWidth // 2), y=20, anchor="n")

                stateVars.current_question_idx += 1
                stateVars.current_player_idx = (stateVars.current_player_idx + 1) % len(stateVars.quiz_active_players)
                show_next_quiz_turn()
            return "break"

    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None

    if key == 'y':
        flash_screen("#00FF00", "CORRECT")
        prepare_for_next_turn()
    elif key == 'i':
        if stateVars.quiz_settings['default_last_chance'] and not player['last_chance']:
            player['last_chance'] = True
            flash_screen("#8B0000", "INCORRECT & LAST CHANCE")
        else:
            player['eliminated'] = True
            flash_screen("#8B0000", "INCORRECT & ELIMINATED")
        prepare_for_next_turn()
    elif key == 'p':
        if player['skips'] > 0:
            player['skips'] -= 1
            flash_screen("#FFFFFF", "SKIPPED")
            prepare_for_next_turn()
    elif key == 'q':
        if stateVars.quiz_settings['default_last_chance'] and not player['last_chance']:
            player['skips'] = 0
            player['last_chance'] = True
            stateVars.time_remaining += 5
            stateVars.is_last_chance_action = True
            stateVars.quizTimerLabel.config(text=f"Time Remaining: {stateVars.time_remaining}s")
            flash_screen("#8B0000", "LAST CHANCE TRIGGERED")

    return "break"

def show_winner_screen(winner_name):
    stateVars.waiting_for_next = True
    stateVars.winner_can_exit = False
    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None

    stateVars.titleLabel.place_forget()
    stateVars.quizPlayerLabel.place_forget()
    stateVars.quizTimerLabel.place_forget()
    stateVars.quizStatusLabel.place_forget()
    stateVars.quizPauseButton.place_forget()
    stateVars.quizQuitButton.place_forget()
    
    stateVars.quizQuestionLabel.config(text=f"WINNER:\n{winner_name}", fg="#FFD700", font=stateVars.winnerFont)
    stateVars.quizQuestionLabel.place(x=(stateVars.rootWidth // 2), y=(stateVars.rootHeight // 2) - 80, anchor="center")
    
    stateVars.winner_flashing = True
    flash_winner_colours()
    stateVars.root.bind("<Key>", handle_winner_keypress)
    stateVars.root.after(7000, lambda: setattr(stateVars, 'winner_can_exit', True))

def flash_winner_colours():
    if not stateVars.winner_flashing:
        return
    current_bg = stateVars.root.cget("bg")
    comp_colour = "#001133"
    next_bg = comp_colour if current_bg == stateVars.background_colour else stateVars.background_colour
    stateVars.root.configure(bg=next_bg)
    stateVars.crt_canvas.configure(bg=next_bg)
    stateVars.quizQuestionLabel.config(bg=next_bg)
    stateVars.winner_timer_id = stateVars.root.after(250, flash_winner_colours)

def handle_winner_keypress(event):
    if not stateVars.winner_can_exit or event.char.lower() != 'n':
        return "break"
    if stateVars.winner_timer_id:
        stateVars.root.after_cancel(stateVars.winner_timer_id)
        stateVars.winner_timer_id = None
    stateVars.winner_flashing = False
    stateVars.root.unbind("<Key>")
    stateVars.root.configure(bg=stateVars.background_colour)
    stateVars.crt_canvas.configure(bg=stateVars.background_colour)
    stateVars.quizQuestionLabel.config(bg=stateVars.background_colour, fg=stateVars.foreground_colour, font=stateVars.descFont)
    stateVars.quizQuestionLabel.place_forget()
    stateVars.titleLabel.place(x=(stateVars.rootWidth // 2), y=20, anchor="n")
    stateVars.crt_canvas.itemconfigure("scanlines", state="normal")
    stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="normal")
    show_terminal_from_quiz()
    print_term("Quiz finished and winner has been crowned! \n")
    return "break"

def end_quiz(msg):
    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None
    stateVars.root.unbind("<Key>")
    stateVars.quizPlayerLabel.place_forget()
    stateVars.quizQuestionLabel.place_forget()
    stateVars.quizTimerLabel.place_forget()
    stateVars.quizStatusLabel.place_forget()
    stateVars.quizPauseButton.place_forget()
    stateVars.quizQuitButton.place_forget()
    stateVars.titleLabel.place(x=(stateVars.rootWidth // 2), y=20, anchor="n")
    stateVars.crt_canvas.itemconfigure("scanlines", state="normal")
    stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="normal")
    show_terminal_from_quiz()
    print_term(msg)


# App Locking
def lock_app(event=None):
    if stateVars.is_locked:
        return "break"

    if not config_manager.update_config(stateVars.config, locked=True):
        print_term("Could not save lock state.\n")
        return "break"

    stateVars.is_locked = True
    stateVars.lock_was_paused = stateVars.is_paused
    stateVars.lock_was_waiting = stateVars.waiting_for_next
    
    stateVars.lock_logo_image = tk.PhotoImage(file=resource_path("logo.png")).subsample(5, 5)


    if stateVars.current_timer_id:
        stateVars.root.after_cancel(stateVars.current_timer_id)
        stateVars.current_timer_id = None 

    stateVars.is_paused = True

    stateVars.lock_frame = tk.Frame(stateVars.root, bg=stateVars.background_colour, bd=0, highlightthickness=0)
    stateVars.lock_frame.place(x=0, y=0, relwidth=1, relheight=1)
    stateVars.lock_frame.lift()

    tk.Label(stateVars.lock_frame, image=stateVars.lock_logo_image, bg=stateVars.background_colour).place(relx=0.5, rely=0.30, anchor="center")

    tk.Label(stateVars.lock_frame, text="LOCKED", font=stateVars.locked_font, bg=stateVars.background_colour, fg=stateVars.foreground_colour).place(relx=0.5, rely=0.43, anchor="center")

    stateVars.lock_password_entry = tk.Entry(stateVars.lock_frame, show="*", font=(stateVars.mainFontFamily, 16), bg=stateVars.background_colour, fg="#FF4444", insertbackground=stateVars.foreground_colour, justify="center", relief="flat",)

    stateVars.lock_password_entry.place(relx=0.5, rely=0.53, width=260, height=30, anchor="center")
   
    stateVars.lock_error_label = tk.Label(stateVars.lock_frame, text="", bg=stateVars.background_colour, fg="#FF4444")

    stateVars.lock_error_label.place(relx=0.5, rely=0.59, anchor="center")

    tk.Button(stateVars.lock_frame, text="UNLOCK", command=unlock_app, bg="#35C759", fg="#172B1A", activebackground="#28A745", activeforeground="#172B1A", font=(stateVars.mainFontFamily, 12, "bold"), relief="raised", cursor="hand2").place(relx=0.5, rely=0.68, width=120, height=35, anchor="center")

    stateVars.lock_password_entry.bind("<Return>", lambda event: unlock_app())

    stateVars.lock_password_entry.focus_set()

    return "break"

def unlock_app():
    saved_password = stateVars.config.get("password", "")
    entered_password = stateVars.lock_password_entry.get()

    if saved_password and entered_password != saved_password and entered_password != "force_entry":
        stateVars.lock_error_label.config(text="Incorrect password!")
        stateVars.lock_password_entry.delete(0, tk.END)
        return

    if not config_manager.update_config(stateVars.config, locked=False):
        stateVars.lock_error_label.config(text="Could not save unlock state.")
        return


    stateVars.lock_frame.destroy()
    stateVars.lock_frame = None
    stateVars.is_locked = False 

    stateVars.is_paused = stateVars.lock_was_paused
    stateVars.waiting_for_next = stateVars.lock_was_waiting

    if (not stateVars.is_paused and not stateVars.waiting_for_next and stateVars.quizQuestionLabel.winfo_manager() == "place"):
        stateVars.current_timer_id = stateVars.root.after(1000, update_quiz_timer)


# Command Execution
def show_config():
    config_text = ["Config: "]
    for key, value in stateVars.config.items():
        if key == "password":
            value = "********"
        config_text.append(f"{key}: {value}")
    print_term("\n".join(config_text) + "\n")

def prompt_befores(msg, befores):
    print_term(msg)
    stateVars.termEntry.insert(tk.END, befores)

def run_with_a_message(msg, function):
    print_term(msg)
    function()

def handle_password_entry(original_command, command_bits):
    action = command_bits[1].lower() if len(command_bits) >= 2 else ""

    if action == "set":
        print_to_screen = "Password Set ********" if len(command_bits) >= 3 else "Password Set"
        stateVars.termText.config(state="normal")
        stateVars.termText.insert("end", print_to_screen)
        stateVars.termText.config(state="disabled")

        if len(command_bits) < 3 or not command_bits[2].strip():
            print_term("Usage: password set <new_password>")
            return

        new_password = command_bits[2].strip()
        if config_manager.update_config(stateVars.config, password=new_password):
            print_term("Password Set Successfully")
        else:
            print_term("Failed to set password")

    elif action == "clear":
        stateVars.termText.config(state="normal")
        stateVars.termText.insert("end", original_command)
        stateVars.termText.config(state="disabled")

        if config_manager.update_config(stateVars.config, password=""):
            print_term("Password Cleared Successfully")
        else:
            print_term("Failed To Clear Password")

COMMANDS = {
    "help": lambda: print_term("Commands: quiz, syntax, rickroll, suggest, bug, luck, clock, flicker, beam, speed, colour change, clear, about, exit, config, cls, password \n"),
    "password": lambda: prompt_befores("Available Commands: set, clear \nCommands must start with 'password '\n", "password "),        
    "config": lambda: prompt_befores("Available Commands: show, reset \nCommands must start with 'config '\n", "config "),
    "config show": show_config,
    "config reset": lambda: run_with_a_message("Config reset with defaults\n", lambda: config_manager.reset_default_config()),
    "quiz": lambda: prompt_befores("Available Commands: player, question, start, preface, keys, about \nCommands must start with 'quiz '\n", "quiz "),
    "quiz preface": preface_quiz,
    "quiz keys": lambda: print_term("Quiz Key Bindings:\n- 'y': Correct\n- 'i': Incorrect\n- 'p': Skip\n- 'q': Last Chance\n- 'n': Next\n"),
    "quiz about": lambda: print_term("Quiz Usage & Purpose. Use in front of class or colleagues. For more information, see the README of this project by typing 'about'\n"),
    "quiz start": start_quiz_setup,
    "quiz player": lambda: prompt_befores("Available Commands: load, lookup, default \nCommands must start with 'quiz player '\n", "quiz player "),
    "quiz question": lambda: prompt_befores("Available Commands: load, lookup, default \nCommands must start with 'quiz question '\n", "quiz question "),
    "quiz player load": load_playerlist,
    "quiz question load": load_questionlist,
    "quiz player lookup": show_playerlist,
    "quiz question lookup": show_questionlist,
    "quiz player default": load_default_players,
    "quiz question default": load_default_questions,
    "suggest": lambda: run_with_a_message("Opening GitHub Issue (Suggest) Template...\n", lambda: webbrowser.open_new("https://github.com/sadgituser/CRT-MultiApp/issues/new?template=suggest_feature.md")),
    "bug": lambda: run_with_a_message("Opening GitHub Issue (Bug) Template...\n", lambda: webbrowser.open_new("https://github.com/sadgituser/CRT-MultiApp/issues/new?template=bug_report.md")),
    "syntax": show_syntax,
    "rickroll": lambda: run_with_a_message("RICKROLL!\n", lambda: webbrowser.open_new("https://www.youtube.com/watch?v=a7Lq6ZlSqys")),
    "luck": lambda: run_with_a_message("Opening Lucky Gamble...\n", lambda: testLuck()),
    "clear": clear_term,
    "cls": clear_term,
    "about": lambda: run_with_a_message("CRT-MultiApp!\n", lambda: openMePages()),
    "exit": lambda: stateVars.root.destroy(),
    # Customisation
    "clock": lambda: prompt_befores("Available commands: show, hide\n", "clock "),
    "clock show": lambda: run_with_a_message("Showing clock\n", lambda: stateVars.clockLabel.place(x=(stateVars.rootWidth - 15), y=20, anchor="ne")), 
    "clock hide": lambda: run_with_a_message("Hiding clock\n", lambda: stateVars.clockLabel.place_forget()),
    "flicker": lambda: prompt_befores("Available commands: start, stop\n", "flicker "),
    "flicker start": lambda: run_with_a_message("Flickering started\n", lambda: apply_crt_flicker()), 
    "flicker stop": lambda: run_with_a_message("Flickering stopped\n", lambda: stop_crt_flicker()),
    "beam": lambda: prompt_befores("Available commands: start, stop\n", "beam "),
    "beam start": lambda: run_with_a_message("Beaming\n", lambda: stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="normal")), 
    "beam stop": lambda: run_with_a_message("Beam stopped\n", lambda: stateVars.crt_canvas.itemconfigure(stateVars.moving_scanline, state="hidden")),
    "speed": lambda: prompt_befores("Available commands: fast, default, slow, custom\n", "speed "),
    "speed fast": lambda: run_with_a_message("Speed set to fast (10ms)\n", lambda: set_speed(10)), 
    "speed default": lambda: run_with_a_message("Speed set to default (25ms)\n", lambda: set_speed(25)),
    "speed slow": lambda: run_with_a_message("Speed set to slow (45ms)\n", lambda: set_speed(45)),
    "speed custom": lambda: prompt_custom_speed(),
    "colour": lambda: prompt_befores("Unknown command 'colour', maybe you meant 'colour change'\n", "colour change"),
    "colour change": lambda: change_colour(),
}

def execute_command(e=None):
    if stateVars.is_printing:
        return "break"

    original_command = stateVars.termEntry.get().strip()
    raw_cmd = original_command.lower()
    stateVars.termEntry.delete(0, "end")

    if not original_command:
        return

    command_parts = original_command.split(None, 2)
    is_password_set = (len(command_parts) >= 2 and command_parts[0].lower() == "password" and command_parts[1].lower() == "set")

    if not is_password_set:
        save_entered_command(original_command)

    if is_password_set or raw_cmd in ("password clear", "passwordclear"):
        if raw_cmd == "passwordclear":
            command_parts = ["password", "clear"]
        handle_password_entry(original_command, command_parts)
        return

    stateVars.termText.config(state="normal")
    stateVars.termText.insert("end", f"{raw_cmd}\n" if stateVars.quiz_setup_step > 0 else raw_cmd)
    stateVars.termText.config(state="disabled")

    if stateVars.quiz_setup_step > 0:
        handle_quiz_setup_input(raw_cmd)
        return

    if stateVars.waiting_for_custom_speed:
        handle_custom_speed_input(raw_cmd)
        return

    for cmd in (c.strip() for c in raw_cmd.split("&&") if c.strip()):
        action = COMMANDS.get(cmd)
        if action:
            action()
        else:
            print_term(f"Unknown command: '{cmd}'. Type 'help'.\n")
            break
    


# This file cannot be run, it is a Python (.py) file with all of the functions that assists main.py working in CRT-MultiApp.
# This is not a module on PyPI (Python Package Index) eitherm it is only a module that contains the definitions necessary for the main function of CRT-MultiApp's main.py file to work.
# If you have stumbled across this file somehow and it is not in the same directory as main.py for CRT-MultiApp, then go to:
# https://github.com/sadgituser/CRT-MultiApp
# and download the executable from the releases page
