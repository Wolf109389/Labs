import os

class Node:
    def __init__(self, value, priority):
        self.height = 1
        self.value = value
        self.priority = priority
        self.left = None
        self.right = None


class AVLPriorityQueue:
    def __init__(self):
        self.root = None

    def balance(self, node):
        return self.height(node.left) - self.height(node.right)
    
    def height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left),
                              self.height(node.right))

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, value, priority):
        self.root = self._insert(self.root, value, priority)

    def _insert(self, node, value, priority):
        if not node:
            return Node(value, priority)

        if priority > node.priority:
            node.left = self._insert(node.left, value, priority)
        else:
            node.right = self._insert(node.right, value, priority)

        self.update_height(node)
        return self._balance(node)

    def _balance(self, node):
        bf = self.balance(node)

        if bf > 1:
            if self.balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if bf < -1:
            if self.balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def extract_max(self):
        if not self.root:
            return None

        self.root, node = self._extract_max(self.root)
        return node.value, node.priority

    def _extract_max(self, node):
        if not node.left:
            return node.right, node

        node.left, res = self._extract_max(node.left)
        self.update_height(node)
        return self._balance(node), res

    def peek(self):
        node = self.root
        if not node:
            return None

        while node.left:
            node = node.left

        return node.value, node.priority

    def get_top_n(self, n):
        result = []
        self._get_top_n(self.root, result, n)
        return result

    def _get_top_n(self, node, result, n):
        if not node or len(result) >= n:
            return

        self._get_top_n(node.left, result, n)

        if len(result) < n:
            result.append((node.value, node.priority))

        self._get_top_n(node.right, result, n)

    def change_priority(self, value, new_priority):
        self.root, node = self._remove_by_value(self.root, value)
        if node:
            self.insert(node.value, new_priority)
            return True
        return False

    def _remove_by_value(self, node, value):
        if not node:
            return None, None

        removed = None

        if value == node.value:
            removed = node

            if not node.left:
                return node.right, removed
            if not node.right:
                return node.left, removed

            temp = node.left
            while temp.right:
                temp = temp.right

            node.value = temp.value
            node.priority = temp.priority

            node.left, _ = self._remove_by_value(node.left, temp.value)

        else:
            node.left, removed = self._remove_by_value(node.left, value)
            if not removed:
                node.right, removed = self._remove_by_value(node.right, value)

        self.update_height(node)
        return self._balance(node), removed

    def inorder(self):
        self._inorder(self.root)

    def _inorder(self, node):
        if not node:
            return
        self._inorder(node.left)
        print(f"value={node.value}, priority={node.priority}")
        self._inorder(node.right)


def clear_menu():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    pq = AVLPriorityQueue()

    while True:
        clear_menu()
        print("\n--- MENU ---"
              "\n1. Додати процес"
              "\n2. Змінити пріоритет"
              "\n3. Взяти max"
              "\n4. Подивитись top N"
              "\n5. Вивести всі"
              "\n0. Вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":
            try:
                value = input("Назва процесу: ")
                priority = int(input("Пріоритет: "))
                pq.insert(value, priority)
                print(f"Процес '{value}' з пріоритетом {priority} додано.")
            except ValueError:
                print("Помилка: Пріоритет повинен бути числом.")

        elif choice == "2":
            try:
                value = input("Процес: ")
                new_priority = int(input("Новий пріоритет: "))
                if pq.change_priority(value, new_priority):
                    print("Пріоритет змінено.")
                else:
                    print("Не знайдено процес із такою назвою.")
            except ValueError:
                print("Помилка: Пріоритет повинен бути числом.")

        elif choice == "3":
            try:
                res = pq.extract_max()
                if res:
                    print("Max:", res)
                else:
                    print("Черга порожня.")
            except Exception as e:
                print("Сталася помилка при взятті max:", e)

        elif choice == "4":
            try:
                n = int(input("N: "))
                top = pq.get_top_n(n)
                if top:
                    print("Top:", top)
                else:
                    print("Черга порожня або N=0.")
            except ValueError:
                print("Помилка: N повинен бути числом.")

        elif choice == "5":
            try:
                if pq.root:
                    pq.inorder()
                else:
                    print("Черга порожня.")
            except Exception as e:
                print("Сталася помилка при виведенні:", e)

        elif choice == "0":
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

        input("\nНатисніть Enter, щоб продовжити")
        
if __name__ == "__main__":
    main_menu()
