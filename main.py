import random
import curses
import threading
import time

class RandomSelector():
    def __init__(self, items):
        self.items              = items
        self.selected           = random.choice(self.items)
        self.colors             = {"black": 1, "green": 2}
        self.console_out        = None 
        self.height             = None
        self.lines              = None
        self.lines_list         = None
        self.selected_letters   = None
        self.all_indices        = None
        self.interval_x         = 0.1
        self.interval_y         = 0.1
        self.stop_event         = threading.Event()
        self.index              = float("inf")

    def initialize(self):
        self.console_out = curses.initscr()
        self.height = self.console_out.getmaxyx()[0]-2
        self.lines = int(self.height / 2) if self.height % 2 == 0 else int((self.height + 1) / 2)
        self.lines_list = ["" for _ in range(self.lines)]
        self.selected_letters = ["" for _ in range(len(self.selected))]
        self.all_indices = list(range(len(self.selected)))

        curses.start_color()
        curses.init_pair(self.colors["black"], curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(self.colors["green"], curses.COLOR_GREEN, curses.COLOR_BLACK)

    @property
    def stop_curses(self):
        curses.endwin()

    def get_random(self):
        self.index = random.choice(self.all_indices)
        self.all_indices.remove(self.index)
        return

    def main(self):
        self.initialize()
        thread_x = threading.Thread(target=self.print_all_choices)
        thread_y = threading.Thread(target=self.print_selected)

        thread_x.start()
        thread_y.start()

        start_time = time.time()
        try:
            while time.time() - start_time < 2:
                self.console_out.refresh()
                time.sleep(0.1)

            self.stop_event.set()
            self.stop_curses

        except KeyboardInterrupt:
            self.stop_event.set()
            thread_x.join()
            thread_y.join()
            self.stop_curses 

    def print_all_choices(self):
        while not self.stop_event.is_set():
            for index, word in enumerate(self.lines_list):
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
            self.get_random()
            print(self.selected_letters)
            for letter in range(len(self.selected_letters)):
                if self.selected_letters[letter] != "":
                    self.console_out.attron(curses.color_pair(self.colors["green"]))
                    self.console_out.addstr(curses.LINES - 1, letter, self.selected_letters[letter])
                    self.console_out.attroff(curses.color_pair(self.colors["green"]))
            time.sleep(self.interval_x)

        return

selector = RandomSelector(["apple", "banana", "orange", "grape", "kiwi", "mango", "pear", "peach", "plum", "strawberry"])
selector.main()
