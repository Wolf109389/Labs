import os
from collections import deque
from colorama import Fore, Style, init

def strip_quotes(token):
    token = token.strip()
    if token.startswith("'") and token.endswith("'") and len(token) >= 2:
        return token[1:-1]
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        return token[1:-1]
    return token

def extract_two_ints(line):
    tokens = []
    current = ''
    for ch in line:
        if ch.isdigit() or (ch in '+-' and current == ''):
            current += ch
        else:
            if current != '':
                tokens.append(current)
                current = ''
    if current != '':
        tokens.append(current)

    if len(tokens) != 2:
        return None
    try:
        return int(tokens[0]), int(tokens[1])
    except ValueError:
        return None

def parse_dims(line):
    return extract_two_ints(line)

def parse_point(line):
    return extract_two_ints(line)

def parse_row(line):
    tokens = [t.strip() for t in line.split(',') if t.strip()]
    return [strip_quotes(t) for t in tokens]

def read_input(filename):
    if not os.path.exists(filename):
        print("Файл не знайдено")
        return None

    with open(filename, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 3:
        print("Недостатньо рядків у файлі")
        return None

    dims = parse_dims(lines[0])
    start = parse_point(lines[1])
    replacement = strip_quotes(lines[2])

    if dims is None or start is None or not replacement:
        print("Невірний формат вхідних даних")
        return None

    h, w = dims
    start_y, start_x = start

    matrix_lines = lines[3:]
    matrix = [parse_row(r) for r in matrix_lines]

    if len(matrix) != h or any(len(row) != w for row in matrix):
        print("Розмір матриці не відповідає зазначеним параметрам")
        return None

    if not (0 <= start_y < h and 0 <= start_x < w):
        print("Координати початкової точки за межами поля")
        return None

    return h, w, start_x, start_y, replacement, matrix

def flood_fill(matrix, x, y, new_color):
    h = len(matrix)
    w = len(matrix[0]) if h > 0 else 0
    old_color = matrix[y][x]
    if old_color == new_color:
        return

    queue = deque([(x, y)])
    while queue:
        cx, cy = queue.popleft()
        if matrix[cy][cx] != old_color:
            continue
        matrix[cy][cx] = new_color

        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and matrix[ny][nx] == old_color:
                queue.append((nx, ny))

def write_output(filename, matrix):
    with open(filename, 'w', encoding='utf-8') as f:
        for row in matrix:
            row_text = '[' + ','.join(f"'{c}'" for c in row) + ']'
            f.write(row_text + '\n')

def print_matrix_color(matrix):
    for row in matrix:
        for c in row:
            print(color_map.get(c, '') + c + Style.RESET_ALL, end=' ')
        print()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print("==== МЕНЮ ====")
    print("1. Заливка") 
    print("2. Змінити файл")
    print("3. Показати матрицю")
    print("4. Створити матрицю")
    print("5. Створити кластерну матрицю")
    print("6. Вийти")

def generate_matrix_to_file(filename):
    print("Введіть сід або натисніть Enter для рандомного:")
    seed_input = input().strip()

    if seed_input == '':
        seed = random.randint(0, 10**9)
        print(f"Використано випадковий seed: {seed}")
    else:
        try:
            seed = int(seed_input)
        except ValueError:
            print("Невірний seed")
            return

    random.seed(seed)

    h = random.randint(5, 15)
    w = random.randint(5, 15)

    colors = ['R','G','Y','B','W','X','C','Z','Q','P','O']

    matrix = [[random.choice(colors) for _ in range(w)] for _ in range(h)]

    start_y = random.randint(0, h-1)
    start_x = random.randint(0, w-1)

    replacement = random.choice(colors)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{h} {w}\n")
        f.write(f"{start_y} {start_x}\n")
        f.write(f"'{replacement}'\n")

        for row in matrix:
            row_text = ','.join(f"'{c}'" for c in row)
            f.write(row_text + '\n')

    print("Матриця записана в input.txt")

import random
from collections import deque

def generate_clustered_matrix_to_file(filename):
    print("Введіть сід або натисніть Enter для рандомного:")
    seed_input = input().strip()

    if seed_input == '':
        seed = random.randint(0, 10**9)
        print(f"Seed: {seed}")
    else:
        try:
            seed = int(seed_input)
        except ValueError:
            print("Невірний seed")
            return

    random.seed(seed)

    h = random.randint(5, 15)
    w = random.randint(5, 15)

    colors = ['R','G','Y','B','W','X','C','Z','Q','P','O']

    matrix = [[None for _ in range(w)] for _ in range(h)]

    num_seeds = random.randint(3, 6)

    queue = deque()

    for _ in range(num_seeds):
        y = random.randint(0, h-1)
        x = random.randint(0, w-1)
        color = random.choice(colors)

        matrix[y][x] = color
        queue.append((x, y, color))

    while queue:
        x, y, color = queue.popleft()

        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy

            if 0 <= nx < w and 0 <= ny < h and matrix[ny][nx] is None:
                if random.random() < 0.8:
                    matrix[ny][nx] = color
                    queue.append((nx, ny, color))

    for y in range(h):
        for x in range(w):
            if matrix[y][x] is None:
                matrix[y][x] = random.choice(colors)

    start_y = random.randint(0, h-1)
    start_x = random.randint(0, w-1)

    replacement = random.choice(colors)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{h} {w}\n")
        f.write(f"{start_y} {start_x}\n")
        f.write(f"'{replacement}'\n")

        for row in matrix:
            row_text = ','.join(f"'{c}'" for c in row)
            f.write(row_text + '\n')

    print("Кластерна матриця записана в input.txt")

def main():
    filename = 'input.txt'
    parsed = read_input(filename)

    if parsed is None:
        print('Не вдалося прочитати дані')
        return

    h, w, x, y, replacement, matrix = parsed

    while True:
        clear_console()
        menu()
        choice = input("Обери пункт: ").strip()

        if choice == '1':
            clear_console()
            try:
                x = int(input("Введи X: "))
                y = int(input("Введи Y: "))
                new_color = input("Новий колір: ").strip()

                if not (0 <= y < h and 0 <= x < w):
                    print("Координати поза межами")
                    input("Натисни Enter...")
                    continue

                flood_fill(matrix, x, y, new_color)
                write_output('output.txt', matrix)
                print("Готово! Результат записано в output.txt")
                input("Натисни Enter...")

            except ValueError:
                print("Невірний ввід")
                input("Натисни Enter...")

        elif choice == '2':
            clear_console()
            new_file = input("Введи ім'я файлу: ").strip()
            parsed = read_input(new_file)

            if parsed is None:
                print("Не вдалося завантажити файл")
            else:
                filename = new_file
                h, w, x, y, replacement, matrix = parsed
                print("Файл змінено")

            input("Натисни Enter...")

        elif choice == '3':
            clear_console()
            print("Поточна матриця:")
            print_matrix_color(matrix)
            input("Натисни Enter...")

        elif choice == '4':
            clear_console()
            generate_matrix_to_file('input.txt')

            parsed = read_input('input.txt')
            if parsed:
                h, w, x, y, replacement, matrix = parsed

            input("Натисни Enter...")

        elif choice == '5':
            clear_console()
            generate_clustered_matrix_to_file('input.txt')

            parsed = read_input('input.txt')
            if parsed:
                h, w, x, y, replacement, matrix = parsed

            input("Натисни Enter...")

        elif choice == '6':
            print("Вихід...")
            break

        else:
            print("Невірний пункт меню")
            input("Натисни Enter...")


if __name__ == '__main__':
    init()

    color_map = {
        'R': Fore.RED,
        'G': Fore.GREEN,
        'Y': Fore.YELLOW,
        'B': Fore.BLUE,
        'W': Fore.WHITE,
        'X': Fore.MAGENTA,
        'C': Fore.CYAN,
        'Z': Fore.LIGHTBLACK_EX,
        'Q': Fore.LIGHTRED_EX,
        'P': Fore.LIGHTGREEN_EX,
        'O': Fore.LIGHTYELLOW_EX,
        }
    
    main()