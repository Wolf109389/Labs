from zig_zag_way import zig_zag_way

def zig_zag_robot_way(arr, weight=50, weight_box=10):
    if not arr or not arr[0]:
        return []

    path = zig_zag_way(arr, coordinates=True)

    current_weight = 0
    last_row, last_col = -1, -1

    for row, col in path:
        if current_weight + weight_box > weight:
            return [last_row, last_col]

        current_weight += weight_box
        last_row, last_col = row, col
    
    return [last_row, last_col]

if __name__ == "__main__":
    print("=== Робот (зигзаг) ===")
    print("Введіть розміри матриці, а також параметри ваги для робота. \nРезультатом буде координата, на якій робот зупиниться через перевищення максимальної ваги.")

    while True:
        try:
            m = int(input("Кількість рядків: "))
            n = int(input("Кількість стовпців: "))
            if m <= 0 or n <= 0:
                print("Розміри повинні бути додатні!")
                continue
            break
        except ValueError:
            print("Помилка вводу! Введіть цілі числа.")

    matrix = []
    print("Введіть матрицю построчно (через пробіл):")
    for i in range(m):
        while True:
            try:
                row = list(map(int, input(f"Рядок {i+1}: ").split()))
                if len(row) != n:
                    print(f"Потрібно ввести {n} чисел!")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Помилка! Вводьте тільки числа.")

    while True:
        try:
            w = input("Максимальна вага (за замовчуванням 50): ")
            weight = int(w) if w else 50
            if weight <= 0:
                weight = 50

            w_b = input("Вага однієї коробки (за замовчуванням 10): ")
            weight_box = int(w_b) if w_b else 10
            if weight_box <= 0:
                weight_box = 10
            break
            
        except ValueError:
            print("Помилка вводу! Введіть цілі числа.")

    path = zig_zag_way(matrix, coordinates=True)
    print("\nЗигзаг-шлях (координати):")
    print(path)

    result = zig_zag_robot_way(matrix, weight, weight_box)
    print("\nРобот зупинився на координатах:")
    print(result)