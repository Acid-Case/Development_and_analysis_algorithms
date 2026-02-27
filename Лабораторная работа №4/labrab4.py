from typing import Any, Iterator


class TreeNode:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.__left = None
        self.__right = None

    @property
    def left(self) -> "TreeNode":
        return self.__left

    @left.setter
    def left(self, node) -> None:
        if not isinstance(node, TreeNode):
            raise ValueError(f"Можно присвоить только объект класса {TreeNode.__name__}")
        self.__left = node

    @property
    def right(self) -> "TreeNode":
        return self.__right

    @right.setter
    def right(self, node) -> None:
        if not isinstance(node, TreeNode):
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
        self.__root = None

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

    def search(self, value: Any) -> "TreeNode":
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

        def next_node(root: TreeNode) -> None:
            if not root:
                return

            result.append(root.value)
            next_node(root.left)
            next_node(root.right)

        next_node(self.__root)
        return result

    def traverse_inorder(self) -> list[Any]:
        result = []

        def next_node(root: TreeNode) -> None:
            if not root:
                return

            next_node(root.left)
            result.append(root.value)
            next_node(root.right)

        next_node(self.__root)
        return result

    def traverse_postorder(self) -> list[Any]:
        result = []

        def next_node(root: TreeNode) -> None:
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

    def max(self) -> Any:
        if self.is_empty():
            raise ValueError("Дерево пусто")

        node = self.__root
        while node.right:
            node = node.right
        return node.value

    def min(self) -> Any:
        if self.is_empty():
            raise ValueError("Дерево пусто")

        node = self.__root
        while node.left:
            node = node.left
        return node.value

    def size(self) -> int:
        if self.is_empty():
            return 0
        return self.__get_size(self.__root)

    @staticmethod
    def __get_size(node: TreeNode) -> int:
        if not node:
            return 0
        return 1 + BinaryTree.__get_size(node.left) + BinaryTree.__get_size(node.right)

    def display(self) -> None:
        """Простое отображение дерева"""
        def _display(node: TreeNode, level=0):
            if node:
                _display(node.right, level + 1)
                print(' ' * 4 * level + '->', node.value)
                _display(node.left, level + 1)

        _display(self.__root)

    def __iter__(self) -> Iterator:
        return iter(self.traverse_inorder())


def main():
    tree = BinaryTree()

    tree.insert(4)
    tree.insert(2)
    tree.insert(1)
    tree.insert(3)
    tree.insert(6)
    tree.insert(5)
    tree.insert(7)

    tree2 = BinaryTree()

    tree2.insert(10)
    tree2.insert(5)
    tree2.insert(15)
    tree2.insert(20)
    tree2.insert(2)
    tree2.insert(1)
    tree2.insert(3)

    print(tree.display())
    #print(tree2.display())


if __name__ == "__main__":
    main()