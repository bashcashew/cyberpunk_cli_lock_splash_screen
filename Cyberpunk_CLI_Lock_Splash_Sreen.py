import os
import time
import random
import curses
from rich.console import Console
import signal

#' Disable Ctrl+C + Ctrl+Z
def disable_ctrl_c(signal_received, frame):
    pass
def disable_ctrl_z(signal_received, frame):
    pass

signal.signal(signal.SIGINT, disable_ctrl_c)
signal.signal(signal.SIGINT, disable_ctrl_z)
signal.signal(signal.SIGTSTP, disable_ctrl_z)

#' Optional: Reset the terminal settings for safety ;)
def reset_terminal():
    os.system("stty sane")  #' Reseta terminal to sane settings

# Strings for commands and animations
commands = """samurai@internal-cdprojektred.com/:~ cd HAX
samurai@internal-cdprojektred.com/HAX/:~ ls"""

beep = r"""
          _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \                /::\    \        
       /::::\    \              /::::\    \              /::::\    \              /::::\    \       
      /::::::\    \            /::::::\    \            /::::::\    \            /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \     
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \    
   /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \   
  /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \  
 /:::/\:::\   \:::\ ___\  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\ 
/:::/__\:::\   \:::|    |/:::/__\:::\   \:::\____\/:::/__\:::\   \:::\____\/:::/  \:::\   \:::|    |
\:::\   \:::\  /:::|____|\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\::/    \:::\  /:::|____|
 \:::\   \:::\/:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \/_____/\:::\/:::/    / 
  \:::\   \::::::/    /    \:::\   \:::\    \       \:::\   \:::\    \               \::::::/    /  
   \:::\   \::::/    /      \:::\   \:::\____\       \:::\   \:::\____\               \::::/    /   
    \:::\  /:::/    /        \:::\   \::/    /        \:::\   \::/    /                \::/____/    
     \:::\/:::/    /          \:::\   \/____/          \:::\   \/____/                  ~~          
      \::::::/    /            \:::\    \               \:::\    \                                  
       \::::/    /              \:::\____\               \:::\____\                                 
        \::/____/                \::/    /                \::/    /                                 
         ~~                       \/____/                  \/____/                                  
"""

Greetings = r"""
...      
"""

#' Utility functions
def random_delay(min_time=0.1, max_time=0.2):
    time.sleep(random.uniform(min_time, max_time))

def glitch_effect(window, text, glitch_duration=2):
    #' Defines the color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

    colors = [curses.color_pair(i) for i in range(1, 7)]
    height, width = window.getmaxyx()
    start_time = time.time()

    while time.time() - start_time < glitch_duration:
        window.clear()

        #' Randomizes the colors + characters displayed on-screen
        for y in range(height):
            for x in range(width):
                char = random.choice(['@', '#', '%', '&', '$', '*', '+', '!', '?', ' ', '.', ',', ';', ':', '0', '1', '2', '3'])
                color = random.choice(colors)
                
                #' Simulates screen distortion randomly
                if random.random() < 0.1:
                    shift_x = random.randint(-5, 5)
                    shift_y = random.randint(-2, 2)
                    
                    #' Ensures valid bounds
                    shifted_x = max(0, min(x + shift_x, width - 1))
                    shifted_y = max(0, min(y + shift_y, height - 1))
                    
                    try:
                        window.addstr(shifted_y, shifted_x, char, color)
                    except curses.error:
                        pass
                else:
                    try:
                        window.addstr(y, x, char, color)
                    except curses.error:
                        pass

        window.refresh()
        random_delay(0.01, 0.05)  #'Glitch intesity adjustment

    #' After the glitch sim. the splash screen will pop-up
    window.clear()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        try:
            window.addstr((height - len(lines)) // 2 + i, max(0, (width - len(line)) // 2), line)
        except curses.error:
            pass
    window.refresh()
    random_delay(0.05, 0.1)

def draw_text(window, text):
    height, width = window.getmaxyx()
    lines = text.split('\n')
    for line in lines:
        for char in line:
            window.addstr(height // 2, max(0, (width - len(line)) // 2), char)
            window.refresh()
            random_delay(0.05, 0.1)
        window.addstr("\n")
    window.refresh()

def type_out_command(window, text, delay_min=0.05, delay_max=0.1):
    height, width = window.getmaxyx()
    y_offset = 2  # Start typing from the 3rd row

    for line in text.split('\n'):
        for i, char in enumerate(line):
            window.addstr(y_offset, max(0, (width - len(line)) // 2 + i), char)
            window.refresh()
            random_delay(delay_min, delay_max)
        y_offset += 1  # Move to the next line
    window.clear()
    window.refresh()

def type_out_password(window, prompt="Password: ", delay_min=0.05, delay_max=0.1, y_position=None, x_position=None):
    curses.echo()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  #' Red for typing
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  #' White for backspace

    height, width = window.getmaxyx()
    
    #' Defaults to centering
    if y_position is None or y_position >= height:
        y_position = max(0, height // 2 - 1)
    if x_position is None or x_position + len(prompt) >= width:
        x_position = max(0, (width - len(prompt)) // 2)

    try:
        window.addstr(y_position, x_position, prompt)
        window.refresh()
    except curses.error:
        return False

    password = ''
    while True:
        key = window.getch()

        if key == 10:
            if password == "PASSWORD": #' obviously not best practice at all xD
                return True
            else:
                window.clear()
                window.addstr(y_position + 2, x_position, "Incorrect password. Try again.")
                window.refresh()
                time.sleep(1)
                window.clear()
                window.refresh()
                window.addstr(y_position, x_position, prompt)
        elif key == 27:
            break
        elif key == 127:
            if password:
                password = password[:-1]
                window.clear()
                window.addstr(y_position, x_position, prompt)
                window.addstr(y_position + 1, x_position, "*" * len(password), curses.color_pair(2))
                window.refresh()
        elif 32 <= key <= 126:
            password += chr(key)
            window.clear()
            window.addstr(y_position, x_position, prompt)
            window.addstr(y_position + 1, x_position, "*" * len(password), curses.color_pair(1))  # Red for typing
            window.refresh()

        random_delay(delay_min, delay_max)
    
    curses.noecho()
    return False

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    console = Console()


    height, width = stdscr.getmaxyx()


    type_out_command(stdscr, commands)


    glitch_effect(stdscr, beep)
    random_delay(10)
    type_out_command(stdscr, str(""))
    while True:
        correct_password = type_out_password(stdscr)
        if correct_password:
            break


    stdscr.getch()


curses.wrapper(main)
