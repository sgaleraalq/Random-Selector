import time

import random
import curses

class RandomSelector():
    def __init__(self, items):
        self.items              = items
        self.selected           = random.choice(self.items)
        self.colors             = {"black": 1, "green": 2}
        self.console_out        = curses.initscr()
        self.height             = self.console_out.getmaxyx()[0]-2
        self.lines              = int(self.height / 2) if self.height % 2 == 0 else int((self.height + 1) / 2)
        self.lines_list         = ["" for _ in range(self.lines)]
        self.letters_selected   = ["" for _ in range(len(self.selected))]

        curses.start_color()
        curses.init_pair(self.colors["black"], curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(self.colors["green"], curses.COLOR_GREEN, curses.COLOR_BLACK)

    @property
    def stop_curses(self):
        curses.endwin()

    def get_random(self, lst: list):
        index = random.choice(lst)
        lst.remove(index)
        return lst, index


    def all_choices(self, total_time: float):
        start_time = time.time()
        end_time = start_time + total_time
        
        while time.time() < end_time:
            new_choice = random.choice(self.items)
            self.lines_list.pop(0)
            self.lines_list.append(new_choice)
            self.console_out.clear()
            self.console_out.addstr(curses.LINES - 1, 0, self.selected)

            for index, choice in enumerate(self.lines_list):
                for letter in range(len(choice)):

                    if letter <= len(self.letters_selected) - 1 and self.letters_selected[letter] == choice[letter]:
                        self.console_out.attron(curses.color_pair(self.colors["green"]))
                        self.console_out.addstr(index * 2, letter, choice[letter])
                        self.console_out.attroff(curses.color_pair(self.colors["green"]))
                    
                    else:
                        self.console_out.addstr(index * 2, letter, choice[letter])
            
            ## Print last line
            # for letter in range(len(self.letters_selected)):
            #     if self.letters_selected[letter] != "":
            #         self.console_out.attron(curses.color_pair(self.colors["green"]))
            #         self.console_out.addstr(curses.LINES - 1, letter, self.letters_selected[letter])
            #         self.console_out.attroff(curses.color_pair(self.colors["green"]))


            self.console_out.refresh()
            time.sleep(1)

        if self.console_out.getch():
            self.stop_curses

    def show_result(self, time_per_letter: float):
        all_indices = list(range(len(self.selected)))
        self.all_choices(time_per_letter * len(self.selected))

        try:
            self.console_out.attron(curses.color_pair(self.colors["black"]))
            self.console_out.refresh()

            while all_indices:
                all_indices, index = self.get_random(all_indices)
                self.letters_selected[index] = self.selected[index]
                self.console_out.attron(curses.color_pair(self.colors["green"]))
                self.console_out.addstr(curses.LINES - 1, index, self.selected[index])
                self.console_out.attroff(curses.color_pair(self.colors["green"]))
                self.console_out.refresh()
                time.sleep(time_per_letter)
            self.console_out.getch()

        finally:
            curses.endwin()

selector = RandomSelector(["apple", "banana", "orange", "grape", "kiwi", "mango", "pear", "peach", "plum", "strawberry"])
selector.show_result(0.5)
# selector.all_choices(2)