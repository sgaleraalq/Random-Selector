import random
import curses
import time

class RandomSelector():
    def __init__(self, items):
        self.items          = items
        self.selected       = random.choice(self.items)
        self.colors         = {"black": 1, "green": 2}
        # self.console_out    = curses.initscr()
        # self.height         = self.console_out.getmaxyx()[0]-2
        # self.lines          = int(self.height / 2) if self.height % 2 == 0 else int((self.height + 1) / 2)

        # curses.start_color()
        # curses.init_pair(self.colors["red"], curses.COLOR_RED, curses.COLOR_BLACK)
        # curses.init_pair(self.colors["green"], curses.COLOR_GREEN, curses.COLOR_BLACK)

    @property
    def print_result(self):
        try: 
            self.print_other_results()
            self.console_out.addstr(curses.LINES - 1, 0, "Selected: ", curses.color_pair(self.colors["red"]))
            self.console_out.addstr(curses.LINES - 1, len("Selected: "), self.selected, curses.color_pair(self.colors["green"]))

            self.console_out.refresh()
            self.console_out.getch()

        finally: 
            curses.endwin()
        
    def print_other_results(self):
        for index in range(self.lines):
            line_position = index*2
            self.console_out.addstr(line_position, 0, "banana")

    def get_random(self, lst: list):
        index = random.choice(lst)
        lst.remove(index)
        return lst, index


    def show_result(self):
        console_out = curses.initscr()
        curses.start_color()

        curses.init_pair(self.colors["black"], curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(self.colors["green"], curses.COLOR_GREEN, curses.COLOR_BLACK)

        all_indices = list(range(len(self.selected)))

        try:
            console_out.attron(curses.color_pair(self.colors["black"]))
            console_out.refresh()

            while all_indices:
                all_indices, index = self.get_random(all_indices)
                console_out.attron(curses.color_pair(self.colors["green"]))
                console_out.addstr(curses.LINES - 1, index, self.selected[index])
                console_out.attroff(curses.color_pair(self.colors["green"]))
                console_out.refresh()
                time.sleep(1.5)
        finally:
            curses.endwin()

selector = RandomSelector(["apple", "banana", "orange"])
# selector.print_result
selector.show_result()