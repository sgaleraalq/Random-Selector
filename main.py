import curses
import random
import threading
import time

class RandomSelector():
    def __init__(self, items, time_selected_item=0.5, time_all_items=0.01):
        self.items              = items
        self.selected           = random.choice(self.items)
        self.colors             = {"black": 1, "green": 2}
        self.console_out        = None 
        self.height             = None
        self.lines              = None
        self.lines_list         = None
        self.selected_letters   = None
        self.all_indices        = None
        self.interval_x         = time_selected_item
        self.interval_y         = time_all_items
        self.stop_event         = threading.Event()
        self.last_choice        = ""

    def initialize(self):
        self.console_out = curses.initscr()
        self.height = self.console_out.getmaxyx()[0]-2
        self.lines = int(self.height / 2) if self.height % 2 == 0 else int((self.height + 1) / 2)
        self.lines_list = ["" for _ in range(self.lines)]
        self.selected_letters = ["" for _ in range(len(self.selected))]
        self.all_indices = list(range(len(self.selected)))

        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(self.colors["black"], curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(self.colors["green"], curses.COLOR_GREEN, curses.COLOR_BLACK)

    @property
    def stop_curses(self):
        curses.endwin()

    def get_random(self):
        index = random.choice(self.all_indices)
        self.all_indices.remove(index)
        self.selected_letters[index] = self.selected[index]
        return

    def main(self):
        self.initialize()
        thread_x = threading.Thread(target=self.print_all_choices)
        thread_y = threading.Thread(target=self.print_selected)

        thread_x.start()
        thread_y.start()

        try:
            while not self.stop_event.is_set():
                self.console_out.refresh()
                time.sleep(0.1)

                if len(self.all_indices) == 0:
                    self.stop_event.set()
                    break

            if self.console_out.getch():
                self.stop_curses

        except KeyboardInterrupt:
            self.stop_event.set()
            thread_x.join()
            thread_y.join()
            self.stop_curses 

    def print_all_choices(self):
        while not self.stop_event.is_set():
            new_choice = random.choice(self.items)
            if new_choice != self.last_choice:
                self.last_choice = new_choice
                self.lines_list.append(new_choice)
                self.lines_list.pop(0)
            
            self.console_out.move(curses.LINES - 1, curses.COLS - 1)

            for index, word in enumerate(self.lines_list):
                self.console_out.move(index * 2, 0)
                self.console_out.clrtoeol()
                for letter in range(len(word)):
                    if letter <= len(self.selected_letters) - 1 and self.selected_letters[letter] == word[letter]:
                        self.console_out.attron(curses.color_pair(self.colors["green"]))
                        self.console_out.addstr(index * 2, letter, word[letter])
                        self.console_out.attroff(curses.color_pair(self.colors["green"]))
                    else:
                        self.console_out.addstr(index * 2, letter, word[letter])
            time.sleep(self.interval_y)
        return

    def print_selected(self):
        while not self.stop_event.is_set():
            if len(self.all_indices) > 0: 
                self.get_random()
            for letter in range(len(self.selected_letters)):
                if self.selected_letters[letter] != "":
                    self.console_out.attron(curses.color_pair(self.colors["green"]))
                    self.console_out.addstr(curses.LINES - 1, letter, self.selected_letters[letter])
                    self.console_out.attroff(curses.color_pair(self.colors["green"]))
            time.sleep(self.interval_x)

        return


algorithm_list = [
    "binary search algorithm",
    "quick sort algorithm",
    "merge sort algorithm",
    "depth first search algorithm",
    "breadth first search algorithm",
    "bubble sort algorithm",
    "insertion sort algorithm",
    "selection sort algorithm",
    "heap sort algorithm"
]

selector = RandomSelector(algorithm_list)
selector.main()
