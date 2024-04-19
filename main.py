import random
import curses
import time

class RandomSelector():
    def __init__(self, items):
        self.items          = items
        self.selected       = random.choice(self.items)
        self.colors         = {"red": 1, "green": 2, "reset": 0}
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


    def show_result(self):
        remaining_indices = list(range(len(self.selected)))  # Lista de índices disponibles

        while remaining_indices:
            to_be_added = random.choice(remaining_indices)  # Selecciona un índice aleatorio
            print(to_be_added)
            remaining_indices.remove(to_be_added)  # Elimina el índice seleccionado de la lista
            time.sleep(1)
        print(self.selected)

selector = RandomSelector(["apple", "banana", "orange"])
# selector.print_result
selector.show_result()