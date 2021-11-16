import os
import os.path
import sys
import re
from enum import Enum
from datetime import date
import src.minesweeper as ms
import src.markdown as mk
import encrypt as cy
import random

class Action(Enum):
    UNKNOWN = 0
    PLAY = 1
    NEW_GAME = 2
    RESTART = 3

def parse_issue(title):
    """Parse issue title and return a tuple with (action, <move>)"""

    if 'game: restart' in title.lower():
        return (Action.RESTART, None)

    if 'game: new' in title.lower():
        match_obj = re.match('Game: New ([A-I][1-9])', title, re.I)
        source = match_obj.group(1)
        return (Action.NEW_GAME, (source).lower())
    
    if 'game: show' in title.lower():
        command = title.split()
        if len(command) != 4:
            return (Action.UNKNOWN, None)
        code = int(command[3])
        match_obj = re.match('Game: Show ([A-I][1-9])', title, re.I)
        source = match_obj.group(1)
        return (Action.PLAY, (source).lower(), code)

    return (Action.UNKNOWN, None)

def test_main(play):
    action = parse_issue(play)

    if action[0] == Action.UNKNOWN:
        with open('README.md', 'w') as file:
            to_write = "Invalid Command"
            file.write(to_write)
        return

    elif action[0] == Action.RESTART:
        # Show empty grid
        game = ms.MineSweeper()
        curr = game.get_empty_grid() # Empty grid to show
        with open('README.md', 'w') as file:
            to_write = mk.grid_to_readme(curr)
            file.write(to_write)
        return

    game = None
    curr = None
    grid = None
    c_date = None
    code = None
    if action[0] == Action.NEW_GAME:
        # Start new game
        game = ms.MineSweeper()
        game.createGame(action[1])
        c_date = date.today().strftime("%d/%m/%Y")
        code = random.randint(0, 1e7)
    elif action[0] == Action.PLAY:
        if not os.path.exists('games/current.json'):
            return False, 'ERROR: There is no game in progress! Start a new game first'
        # Load game from "games/current.txt"
        game = ms.MineSweeper()
        curr, grid, c_date, code = cy.load_current_play()
        if (code != action[2]):
            return False, 'ERROR: Invalid code'
        game.load_files(curr, grid)

    state = game.play(action[1])
    u_curr, u_grid = game.get_files()
    cy.save_current_game(u_curr, c_date)
    cy.save_bombs(u_grid, c_date, code + 1)
    if state[0] == 0:
        # Game over
        with open('README.md', 'w') as file:
            to_write = mk.grid_to_readme(u_grid) + "\n You lose"
            file.write(to_write)
    elif state[0] == 1:
        if state[1] == 0:
            # Repited play
            with open('README.md', 'w') as file:
                to_write = mk.grid_to_readme(u_curr) + "\n Repited Play" + "\n Play with code: " + str(code + 1)
                file.write(to_write)
        else:
            # Valid play
            with open('README.md', 'w') as file:
                to_write = mk.grid_to_readme(u_curr) + "\n Unlocked cells : " + str(state[1])+ "\n Play with code: " + str(code + 1)
                file.write(to_write)
    elif state[0] == 2:
        # WIn
        with open('README.md', 'w') as file:
            to_write = mk.grid_to_readme(u_grid) + "\n You Win!!" + "\n Write [Game: Restart] to start a new game"
            file.write(to_write)



if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        f =  sys.argv[2:]
        play = " ".join(f)
        test_main(play)  # Play be like: Game: Show A9 by sebastianolmos | Game: Start new game

        sys.exit(0)

        

        