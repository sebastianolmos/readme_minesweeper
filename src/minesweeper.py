import random

class MineSweeper:
    def __init__(self) -> None:
        self.gridsize = 9
        self.numberofmines = 10
        self.currgrid = None
        self.grid = None

    def load_files(self, crrgrid, grid):
        self.currgrid = crrgrid
        self.grid = grid

    def get_files(self):
        return self.currgrid, self.grid

    def getrandomcell(self, grid):
        gridsize = len(grid)
        a = random.randint(0, gridsize - 1)
        b = random.randint(0, gridsize - 1)
        return (a, b)

    def getneighbors_grid(self, grid, rowno, colno):
        gridsize = len(grid)
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))

        return neighbors

    def getmines(self, grid, start):
        mines = []
        neighbors = self.getneighbors_grid(grid, *start)

        for i in range(self.numberofmines):
            cell = self.getrandomcell(grid)
            while cell == start or cell in mines or cell in neighbors:
                cell = self.getrandomcell(grid)
            mines.append(cell)

        return mines

    def getnumbers(self, grid):
        for rowno, row in enumerate(grid):
            for colno, cell in enumerate(row):
                if cell != 'X':
                    # Gets the values of the neighbors
                    values = [grid[r][c] for r, c in self.getneighbors_grid(grid,
                                                                rowno, colno)]

                    # Counts how many are mines
                    grid[rowno][colno] = str(values.count('X'))
        return grid

    def createGame(self, start):
        columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        rowno = int(start[1])
        colno = columns.index(start[0])
        start = (rowno, colno)
        self.currgrid = [[' ' for i in range(self.gridsize)] for i in range(self.gridsize)]
        emptygrid = [['0' for i in range(self.gridsize)] for i in range(self.gridsize)]
        mines = self.getmines(emptygrid, start)
        for i, j in mines:
            emptygrid[i][j] = 'X'
        self.grid = self.getnumbers(emptygrid)

    def getneighbors(self, rowno, colno):
        gridsize = len(self.grid)
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (rowno + i) < gridsize and -1 < (colno + j) < gridsize:
                    neighbors.append((rowno + i, colno + j))
        return neighbors

    def showcells(self, rowno, colno):
        # Exit function if the cell was already shown
        if self.currgrid[rowno][colno] != ' ':
            return 0

        # Show current cell
        self.currgrid[rowno][colno] = self.grid[rowno][colno]
        cell_count = 1
        # Get the neighbors if the cell is empty
        if self.grid[rowno][colno] == '0':
            for r, c in self.getneighbors(rowno, colno):
                # Repeat function for each neighbor that doesn't have a flag
                if self.currgrid[r][c] != 'F':
                    cell_count += self.showcells(r, c)
        return cell_count
    
    def countblanks(self):
        c = 0
        for i in self.currgrid:
            for j in i:
                if j == ' ':
                    c += 1
        return c

    def play(self, cell):
        columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        rowno = int(cell[1]) -1
        colno = columns.index(cell[0])
        currcell = self.currgrid[rowno][colno]
        unlocked = 0

        if self.grid[rowno][colno] == 'X':
            # Game Over
            self.grid[rowno][colno] = 'Z'
            return (0,0)
        if currcell == ' ':
            unlocked = self.showcells(rowno, colno)
            if self.countblanks() == self.numberofmines:
                # Blanks are only mines -> you win
                return (2, 0)
            else:
                return (1,unlocked)
        else:
            return (1,0)

        
    def get_empty_grid(self):
        self.currgrid = [[' ' for i in range(self.gridsize)] for i in range(self.gridsize)]
        return self.currgrid