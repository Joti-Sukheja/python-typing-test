import curses
from curses import wrapper
import random
import time

def start_screen(stdscr):
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr("Welcome to the typing test game!")
    stdscr.addstr("\nPress any key to start!")
    stdscr.refresh()
    stdscr.getkey()

def load_text():
    with open("text.txt","r")as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def display_text(stdscr, user_text, target_text,wpm = 0 ):
    for i, key in enumerate(user_text): 
             color = curses.color_pair(2)
             if key != target_text[i]:
                 color = curses.color_pair(3) 
                 key = "f"   
             stdscr.addstr(0,i,key,color)
             stdscr.addstr(2,0,f"wpm = {wpm}")

def WPM_test(stdscr):
    target_text = load_text()
    user_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    while True:
        elapsed_time = max(time.time() - start_time, 1)
        wpm = round((len(user_text)/(elapsed_time/60))/5)
        stdscr.clear()
        stdscr.addstr(target_text) 
        display_text(stdscr, user_text, target_text,wpm ) 

        if "".join(user_text)==target_text:
            stdscr.nodelay(False) 
            break
        try: 
           key = stdscr.getkey()
        except:
            continue


        if ord(key) == 27:
           break

        if key in ("KEY_BACKSPACE","\b","\x7f"):
           if len(user_text)  > 0: 
             user_text.pop()
        elif len(user_text)< len(target_text):
            user_text.append(key)

        
        stdscr.refresh()  

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) 
    
 
    start_screen(stdscr)
    while True: 
      WPM_test(stdscr) 
      stdscr.addstr("\nDone! press any key to continue! ('escape' to quit)")
      key = stdscr.getkey()
      if ord(key) == 27:
       break
      
wrapper(main)
