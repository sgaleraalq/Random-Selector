from main import RandomSelector
import curses

groups = ["Denmark", "England", "France"]

group = RandomSelector(groups)

class GroupSelector():
    def __init__(self, groups, participants):
        self.groups = groups
        self.participants = participants
        self.console_out = curses.initscr()
    

    # On exit, stop curses
    @property
    def stop_curses(self):
        curses.endwin()
    

## If exit, stop curses