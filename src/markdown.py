
def grid_to_readme(grid):
    #board_list = [[item for item in line.split(' ')] for line in str(board).split('\n')]
    markdown = ""

    # Write header in Markdown format
    markdown += "|   | A | B | C | D | E | F | G | H | I |   |\n"
    markdown += "|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"

    # Write board
    for row in range(1, 10):
        markdown += "| **" + str(row) + "** | "
        for elem in grid[row - 1]:
            markdown += "{} | ".format(elem)

        markdown += "**" + str(row) + "** |\n"

    # Write footer in Markdown format
    markdown += "|   | **A** | **B** | **C** | **D** | **E** | **F** | **G** | **H** | **I** |   |\n"

    return markdown