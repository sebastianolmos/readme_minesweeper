from cryptography.fernet import Fernet
import json

def generate_key():
    #this generates a key and opens a file 'key.key' and writes the key there
    key = Fernet.generate_key()
    with open('key.key','wb') as file:
        file.write(key)

def encrypt_bombs(data):
    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('key.key','rb') as file:
        key = file.read()
    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encode_data = json.dumps(data, indent=2).encode('utf-8')
    encrypted = fernet.encrypt(encode_data)

    #this writes your new, encrypted data into a new JSON file
    with open('games/bombs.json','wb') as f:
        f.write(encrypted)

def get_decrypted_bombs():
    with open('key.key','rb') as file:
        key = file.read()
    with open('games/bombs.json','rb') as f:
        data = f.read()
    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    return decrypted

def save_current_game(curr, c_date):
    data = get_json_data(curr)
    data["date"] = c_date
    with open('games/current.json','w') as f:
        json.dump(data, f)

def save_bombs(grid, c_date, code):
    data = get_json_data(grid)
    data["date"] = c_date
    data["code"] = code
    encrypt_bombs(data)

def load_current_play():
    curr = parse_current_file()
    grid, c_date, code = parse_bombs_file()
    return curr, grid, c_date, code

def get_json_data(grid):
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    columns=['1', '2', '3', '4', '5', '6', '7', '8', '9']
    dicc = {}
    for i in range(len(grid)):
        tmp_dicc = {}
        for j in range(len(grid[i])):
            tmp_dicc[rows[j]] = grid[i][j]
        dicc[columns[i]] = tmp_dicc
    return dicc


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
        return grid

def parse_bombs_file():
    data = get_decrypted_bombs()
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
    return grid, data2["date"], data2["code"]