from typing import Any, Iterator, Optional


class TreeNode:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.__left: Optional["TreeNode"] = None
        self.__right: Optional["TreeNode"] = None

    @property
    def left(self) -> Optional["TreeNode"]:
        return self.__left

    @left.setter
    def left(self, node) -> None:
        if not isinstance(node, (TreeNode | None)):
            raise ValueError(f"Можно присвоить только объект класса {TreeNode.__name__}")
        self.__left = node

    @property
    def right(self) -> Optional["TreeNode"]:
        return self.__right

    @right.setter
    def right(self, node) -> None:
        if not isinstance(node, (TreeNode | None)):
            raise ValueError(f"Можно присвоить только объект класса {TreeNode.__name__}")
        self.__right = node

    def is_leaf(self) -> bool:
        return not self.left and not self.right

    def __str__(self) -> str:
        return f"Node: {self.value}"

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class BinaryTree:
    def __init__(self) -> None:
        self.__root: Optional["TreeNode"] = None

    def pos_elements_search_1(self) -> list[int | float]:
        elements = self.traverse_inorder()
        return [el for el in elements if el > 0]

    def pos_elements_search_2(self) -> list[int | float]:
        elements = []

        def traverse(node: Optional["TreeNode"]) -> None:
            if not node:
                return

            if node.value > 0:
                traverse(node.left)
                elements.append(node.value)
            traverse(node.right)

        traverse(self.__root)
        return elements

    def insert(self, value: Any) -> None:
        if not self.__root:
            self.__root = TreeNode(value)
            return

        node = self.__root
        while True:
            if value < node.value:
                if not node.left:
                    node.left = TreeNode(value)
                    break
                node = node.left
            else:
                if not node.right:
                    node.right = TreeNode(value)
                    break
                node = node.right

    def delete(self, value: Any) -> bool:
        if not self.__root:
            return False

        if self.__root.value == value:
            self.__root = self.__delete_node(self.__root)
            return True

        parent = self.find_parent(value)
        if not parent:
            return False

        if parent.left and parent.left.value == value:
            node_to_delete = parent.left
            parent.left = self.__delete_node(node_to_delete)
        elif parent.right and parent.right.value == value:
            node_to_delete = parent.right
            parent.right = self.__delete_node(node_to_delete)
        else:
            return False

        return True

    def __delete_node(self, node: TreeNode):
        if node.is_leaf():
            return None

        if not node.right:
            return node.left
        if not node.left:
            return node.right

        min_parent = node
        min_node = node.right
        while min_node.left:
            min_parent = min_node
            min_node = min_node.left
        node.value = min_node.value

        if min_parent.left is min_node:
            min_parent.left = min_node.right
        else:
            min_parent.right = min_node.right

        return node

    def find_parent(self, value: Any) -> Optional["TreeNode"]:
        node = self.__root
        while node:
            if (node.left and node.left.value == value) or (node.right and node.right.value == value):
                return node

            if value < node.value:
                node = node.left
            else:
                node = node.right

        return None

    def search(self, value: Any) -> TreeNode:
        node = self.__root
        while node:
            if value == node.value:
                return node

            if value < node.value:
                node = node.left
            else:
                node = node.right

        raise ValueError("Такого значения в дереве нет")

    def traverse_preorder(self) -> list[Any]:
        result = []

        def next_node(root: Optional["TreeNode"]) -> None:
            if not root:
                return

            result.append(root.value)
            next_node(root.left)
            next_node(root.right)

        next_node(self.__root)
        return result

    def traverse_inorder(self) -> list[Any]:
        result = []

        def next_node(root: Optional["TreeNode"]) -> None:
            if not root:
                return

            next_node(root.left)
            result.append(root.value)
            next_node(root.right)

        next_node(self.__root)
        return result

    def traverse_postorder(self) -> list[Any]:
        result = []

        def next_node(root: Optional["TreeNode"]) -> None:
            if not root:
                return

            next_node(root.left)
            next_node(root.right)
            result.append(root.value)

        next_node(self.__root)
        return result

    def is_empty(self) -> bool:
        return not self.__root

    def __contains__(self, item: Any) -> bool:
        try:
            self.search(item)
            return True
        except ValueError:
            return False

    def max(self, node: Optional["TreeNode"] = None) -> TreeNode:
        if node is None:
            node = self.__root
        if not isinstance(node, TreeNode):
            raise ValueError(f"Элемент должен принадлежать классу {TreeNode.__name__}")
        if self.is_empty():
            raise ValueError("Дерево пусто")

        while node.right:
            node = node.right
        return node

    def min(self, node: Optional["TreeNode"] = None) -> TreeNode:
        if self.is_empty():
            raise ValueError("Дерево пусто")
        if node is None:
            node = self.__root
        if not isinstance(node, TreeNode):
            raise ValueError(f"Элемент должен принадлежать классу {TreeNode.__name__}")

        while node.left:
            node = node.left
        return node

    def size(self) -> int:
        if self.is_empty():
            return 0
        return self.__get_size(self.__root)

    @staticmethod
    def __get_size(node: Optional["TreeNode"]) -> int:
        if not node:
            return 0
        return 1 + BinaryTree.__get_size(node.left) + BinaryTree.__get_size(node.right)

    def display(self) -> None:
        def _display(node: Optional["TreeNode"], level=0):
            if node:
                _display(node.right, level + 1)
                print(' ' * 4 * level + '->', node.value)
                _display(node.left, level + 1)

        _display(self.__root)

    def __iter__(self) -> Iterator:
        return iter(self.traverse_inorder())


def get_int(prompt: str, min: int = 0, max: int = 100_000_000) -> int:
    while True:
        try:
            num = int(input(prompt))

            if num < min or num > max:
                print(f"Число должно быть в диапозоне от {min} до {max}")
                continue

            return num
        except ValueError:
            print("Ошибка: необходимо ввести целое число. Попробуйте снова.")


def get_elem(prompt: str) -> int | float | str:
    while True:
        try:
            data_type = get_int("Введите тип элемента (0 - int, 1 - float, 2 - str): ", 0, 2)
            user_input = input(prompt)

            if data_type == 0:
                return int(user_input)
            elif data_type == 1:
                return float(user_input)
            elif data_type == 2:
                return user_input
        except ValueError:
            if data_type == 0:
                print("Ошибка: необходимо ввести целое число. Попробуйте снова.")
            elif data_type == 1:
                print("Ошибка: необходимо ввести вещественное число. Попробуйте снова.")
            else:
                print("Неизвестная ошибка. Попробуйте снова.")


def main():
    tree = BinaryTree()
    size = get_int("Введите кол-во элементов дерева: ")
    arr = [get_elem("Введите элемент дерева: ") for _ in range(size)]

    for i in arr:
        tree.insert(i)

    print(f"\nПоложительные элементы: {tree.pos_elements_search_2()}")


if __name__ == "__main__":
    main()
