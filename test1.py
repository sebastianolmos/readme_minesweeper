import json
import src.encript as cr

def parse_current_file():
    with open('games/current.json') as current_play:
        data = json.load(current_play)
        grid = []
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        columns=['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in columns:
            tmp_row = []
            for j in rows:
                tmp_row.append(data[i][j])
            grid.append(tmp_row)
        print(grid)

def parse_bombs_file():
    data = cr.get_decrypted_bombs()
    my_json = data.decode('utf8').replace("'", '"')
    data2 = json.loads(my_json)
    grid = []
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    columns=['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in columns:
        tmp_row = []
        for j in rows:
            tmp_row.append(data2[i][j])
        grid.append(tmp_row)
    print(grid)

parse_current_file()
parse_bombs_file()