import pygame as pg, sys

pg.init()
scr = pg.display.set_mode((800, 800))
clock = pg.time.Clock()

class World:
    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.state = {
            (i * cell_size, j * cell_size): False if (i + j) % 2 else True
            for i in range(self.width // self.cell_size)
            for j in range(self.height // self.cell_size)
        }

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

def main():

    grid = World(800, 800, 20)
    
    while True:
        events = pg.event.get()
        mouse = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.QUIT: sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                grid.flip_cell_state(mouse[0] // grid.cell_size, mouse[1] // grid.cell_size)

        scr.fill((0, 0, 0))
        grid.render(scr)
        pg.display.flip()

if __name__ == "__main__":
    main()