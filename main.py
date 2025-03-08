import pygame as pg, sys

pg.init()
scr = pg.display.set_mode((800, 800))
clock = pg.time.Clock()

class GameOfLife:
    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.state = {
            (i * self.cell_size, j * self.cell_size): False
            for i in range(self.width // self.cell_size)
            for j in range(self.height // self.cell_size)
        }

        self.x_bound, self.y_bound = self.width // self.cell_size - 1, self.height // self.cell_size - 1

    def render(self, surf: pg.Surface):
        for cell_position, cell_state in self.state.items():
            pg.draw.rect(surf, (100, 100, 100), [*cell_position, self.cell_size, self.cell_size], 1)
            if cell_state: pg.draw.rect(surf, (255, 255, 255), [*cell_position, self.cell_size, self.cell_size])

    def get_cell_state(self, x: int, y: int):
        return self.state[(x * self.cell_size, y * self.cell_size)]
    
    def set_cell_state(self, x: int, y: int, state: bool):
        self.state[(x * self.cell_size, y * self.cell_size)] = state

    def flip_cell_state(self, x: int, y: int):
        if self.get_cell_state(x, y): self.set_cell_state(x, y, False)
        else: self.set_cell_state(x, y, True)

    def check_up(self, x: int, y: int):
        if y - 1 < 0: return False
        return self.get_cell_state(x, y - 1)
    
    def check_down(self, x: int, y: int):
        if y + 1 > self.y_bound: return False
        return self.get_cell_state(x, y + 1)
    
    def check_left(self, x: int, y: int):
        if x - 1 < 0: return False
        return self.get_cell_state(x - 1, y)
    
    def check_right(self, x: int, y: int):
        if x + 1 > self.x_bound: return False
        return self.get_cell_state(x + 1, y)
    
    def check_upper_left(self, x: int, y: int):
        if x - 1 < 0 or y - 1 < 0: return False
        return self.get_cell_state(x - 1, y - 1)
    
    def check_upper_right(self, x: int, y: int):
        if x + 1 > self.x_bound or y - 1 < 0: return False
        return self.get_cell_state(x + 1, y - 1)
    
    def check_lower_left(self, x: int, y: int):
        if x - 1 < 0 or y + 1 > self.y_bound: return False
        return self.get_cell_state(x - 1, y + 1)
    
    def check_lower_right(self, x: int, y: int):
        if x + 1 > self.x_bound or y + 1 > self.y_bound: return False
        return self.get_cell_state(x + 1, y + 1)
    
    def get_number_of_neighbors(self, x: int, y: int):
        return int(
            self.check_down(x, y) + self.check_up(x, y) +
            self.check_right(x, y) + self.check_left(x, y) +
            self.check_lower_left(x, y) + self.check_lower_right(x, y) +
            self.check_upper_left(x, y) + self.check_upper_right(x, y)
        )

    def update_grid(self):
        buffer_state = {
            (i * self.cell_size, j * self.cell_size): False
            for i in range(self.width // self.cell_size)
            for j in range(self.height // self.cell_size)
        }

        for cell_position, cell_state in self.state.items():
            number_of_neighbors = self.get_number_of_neighbors(cell_position[0] // self.cell_size, cell_position[1] // self.cell_size)
            if number_of_neighbors < 2 and cell_state: buffer_state[cell_position] = False
            elif number_of_neighbors > 3 and cell_state: buffer_state[cell_position] = False
            elif number_of_neighbors == 3 and not cell_state: buffer_state[cell_position] = True
            elif (number_of_neighbors == 2 or number_of_neighbors == 3) and cell_state: buffer_state[cell_position] = True

        self.state = buffer_state.copy()

def main():

    grid = GameOfLife(800, 800, 20)

    mouse_down = False
    erasing = False
    autoplay = False

    tick = 0
    
    while True:
        tick += 1
        events = pg.event.get()
        mouse = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_SPACE: grid.update_grid()
                elif event.key == pg.K_p: autoplay = not autoplay

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_down = True
                if event.button == 1: erasing = False
                elif event.button == 3: erasing = True

            if event.type == pg.MOUSEBUTTONUP:
                mouse_down = False
                erasing = False

        scr.fill((0, 0, 0))

        if autoplay and not tick % 10: grid.update_grid()

        if mouse_down:
            if not erasing: grid.set_cell_state(mouse[0] // grid.cell_size, mouse[1] // grid.cell_size, True)
            else: grid.set_cell_state(mouse[0] // grid.cell_size, mouse[1] // grid.cell_size, False)

        grid.render(scr)
        clock.tick(60)
        pg.display.flip()

if __name__ == "__main__":
    main()