import random
import curses

class RandomSelector():
    def __init__(self, items):
        self.items  = items
        self.selected = random.choice(self.items)
        self.red = 1     # Definir un par de colores para rojo
        self.green = 2   # Definir un par de colores para verde
        self.reset_color = 0  # Par de colores para restablecer el color

        # Inicializar la pantalla de curses
        self.console_out = curses.initscr()

        # Inicializar pares de colores
        curses.start_color()
        curses.init_pair(self.red, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.green, curses.COLOR_GREEN, curses.COLOR_BLACK)

    @property
    def print_result(self):
        try: 
            # Imprimir el mensaje con colores definidos en la última línea de la pantalla
            self.console_out.addstr(curses.LINES - 1, 0, "Selected: ", curses.color_pair(self.red))
            self.console_out.addstr(curses.LINES - 1, len("Selected: "), self.selected, curses.color_pair(self.green))

            # Refrescar la pantalla para mostrar los cambios
            self.console_out.refresh()

            # Esperar a que el usuario presione una tecla
            self.console_out.getch()
        finally: 
            curses.endwin()

selector = RandomSelector(["apple", "banana", "orange"])
selector.print_result