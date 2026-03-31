import random
import pyxel

class MineSweeper:
    def __init__(self, w, h):

        self.w = w
        self.h = h

        pyxel.init(self.w, self.h, "Mine-Sweeper BOT", 60)
        pyxel.mouse(True)

        self.grid_size = (16, 16)
        self.mines = 40
        self.starting_point = None

        self.tile_scale = self.h // self.grid_size[1]

        self.mine_grid = self.plant_mines()
        self.reveled_tiles = []
        self.flags = []
        self.player_grid = self.get_player_grid()

        pyxel.run(self.update, self.draw)


    def update(self):
        if self.is_mouse_in_game():
            tile = (pyxel.mouse_x // self.tile_scale, pyxel.mouse_y // self.tile_scale)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                
                print(f"[CLICK] -> mouse: ({pyxel.mouse_x}, {pyxel.mouse_y}) ; tile: (x={tile[0]}, y={tile[1]})")

                if self.starting_point is None:
                    self.starting_point = tile
                    self.mine_grid = self.plant_mines()

                if self.mine_grid[tile[1]][tile[0]] == 1:
                    print("GAME OVER !")
                
                elif not tile in self.flags:
                    if tile not in self.reveled_tiles:
                        self.reveled_tiles.append(tile)
                        self.big_reveal(tile)

                
                self.player_grid = self.get_player_grid()
                #print(self.reveled_tiles)
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                
                if tile in self.flags:
                    self.flags.remove(tile)
                else:
                    self.flags.append(tile)


    def draw(self):
        pyxel.cls(0)

        for j in range(0, self.grid_size[1]):
            for i in range(0, self.grid_size[0]):
                x = i*self.tile_scale
                y = j*self.tile_scale
                
                #pyxel.rect(x, y, self.tile_scale, self.tile_scale, 1 if self.mine_grid[j][i] else 7)
                pyxel.rect(x, y, self.tile_scale, self.tile_scale, 7)
                pyxel.rectb(x, y, self.tile_scale, self.tile_scale, 6)

                if (i, j) in self.reveled_tiles:
                    pyxel.text(x, y, f"{self.how_many_mines_around_me((i, j))[0]}", 2)
                elif (i, j) in self.flags:
                    pyxel.text(x, y, "F", 1)



        if self.is_mouse_in_game():
            x = pyxel.mouse_x // self.tile_scale * self.tile_scale
            y = pyxel.mouse_y // self.tile_scale * self.tile_scale
            
            pyxel.rect(x, y, self.tile_scale, self.tile_scale, 2)
        



    def is_mouse_in_game(self):
        return (0 <= pyxel.mouse_x <= self.w) and (0 <= pyxel.mouse_y <= self.h)


    def plant_mines(self):
        
        assert self.mines <= self.grid_size[0] * self.grid_size[1] - 1, "Too many mines"

        
        grille = [[0 for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]

        if self.starting_point is None: return grille

        toutes_positions = [(i, j) for i in range(self.grid_size[0]) for j in range(self.grid_size[1]) if (i, j) != self.starting_point]

        emplacements_mines = random.sample(toutes_positions, self.mines)
        
        for x, y in emplacements_mines:
            grille[y][x] = 1
            
        return grille


    def how_many_mines_around_me(self, tile:tuple[int, int], target=1):

        neighbors = [(x, y) for x in range(tile[0]-1, tile[0]+2) for y in range(tile[1]-1, tile[1] + 2) if (0 <= x < len(self.mine_grid)) and (0 <= y < len(self.mine_grid[0])) and ((x, y) != tile) and (self.mine_grid[y][x] == target)]
        return len(neighbors), neighbors
    

    def get_player_grid(self):
        # -1 -> not reveled, else -> nb of mines around
        return [[self.how_many_mines_around_me((i, j))[0] if (i, j) in self.reveled_tiles else -1 for i in range(self.grid_size[0])] for j in range(self.grid_size[1])]
    

    def big_reveal(self, tile):
        mines_around = self.how_many_mines_around_me(tile, 1)[0]

        if mines_around == 0:
            
            neighbors = self.how_many_mines_around_me(tile, 0)[1]
            
            for n in neighbors:
                if n not in self.reveled_tiles:
                    self.reveled_tiles.append(n)
                    
                    if self.how_many_mines_around_me(n, 1)[0] == 0:
                        self.big_reveal(n)
                
            

M = MineSweeper(256, 256)
