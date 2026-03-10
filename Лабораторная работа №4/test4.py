import pytest
from labrab4 import BinaryTree, TreeNode


class TestPositiveElementsSearch:
    """Тесты для методов поиска положительных элементов в бинарном дереве"""

    def setup_method(self):
        """Создаем дерево с тестовыми данными перед каждым тестом"""
        self.tree = BinaryTree()
        # Создаем дерево:
        #        10
        #       /  \
        #     -5    20
        #     / \   / \
        #    3  -8 15 -3
        #       /      \
        #      7       25
        values = [10, -5, 20, 3, -8, 15, -3, 7, 25]
        for value in values:
            self.tree.insert(value)
        # Положительные числа: 10, 3, 20, 15, 7, 25

    def test_pos_elements_search_1_basic(self):
        """Базовый тест поиска положительных элементов через обход"""
        result = self.tree.pos_elements_search_1()
        # При inorder обходе: 3, -8, 7, -5, 10, 15, 20, -3, 25
        # Положительные: 3, 7, 10, 15, 20, 25
        assert sorted(result) == [3, 7, 10, 15, 20, 25]
        assert len(result) == 6

    def test_pos_elements_search_2_basic(self):
        """Базовый тест поиска положительных элементов через рекурсивный обход"""
        result = self.tree.pos_elements_search_2()
        # Должен вернуть те же элементы, но в порядке обхода
        expected = [3, 7, 10, 15, 20, 25]  # Положительные числа
        assert sorted(result) == expected
        assert len(result) == 6

    def test_both_methods_return_same_result(self):
        """Проверка, что оба метода возвращают одинаковые результаты"""
        result1 = sorted(self.tree.pos_elements_search_1())
        result2 = sorted(self.tree.pos_elements_search_2())
        assert result1 == result2
        assert result1 == [3, 7, 10, 15, 20, 25]

    def test_search_with_all_positive(self):
        """Тест когда все элементы положительные"""
        tree = BinaryTree()
        values = [5, 3, 8, 1, 4, 7, 9]
        for value in values:
            tree.insert(value)

        result1 = tree.pos_elements_search_1()
        result2 = tree.pos_elements_search_2()

        assert sorted(result1) == sorted(values)
        assert sorted(result2) == sorted(values)
        assert len(result1) == len(values)

    def test_search_with_all_negative(self):
        """Тест когда все элементы отрицательные"""
        tree = BinaryTree()
        values = [-5, -3, -8, -1, -4, -7, -9]
        for value in values:
            tree.insert(value)

        result1 = tree.pos_elements_search_1()
        result2 = tree.pos_elements_search_2()

        assert result1 == []
        assert result2 == []

    def test_search_with_mixed_numbers(self):
        """Тест со смешанными числами (положительные, отрицательные, ноль)"""
        tree = BinaryTree()
        values = [0, -5, 10, -3, 0, 7, -2, 15]
        for value in values:
            tree.insert(value)

        result1 = tree.pos_elements_search_1()
        result2 = tree.pos_elements_search_2()

        # Положительные числа: 10, 7, 15 (0 не считается положительным)
        expected = [7, 10, 15]
        assert sorted(result1) == expected
        assert sorted(result2) == expected

    def test_search_with_floats(self):
        """Тест с числами с плавающей точкой"""
        tree = BinaryTree()
        values = [3.14, -2.5, 1.5, -0.5, 2.7, -1.8]
        for value in values:
            tree.insert(value)

        result1 = tree.pos_elements_search_1()
        result2 = tree.pos_elements_search_2()

        expected = [1.5, 2.7, 3.14]
        assert sorted(result1) == expected
        assert sorted(result2) == expected

    def test_search_empty_tree(self):
        """Тест для пустого дерева"""
        empty_tree = BinaryTree()

        result1 = empty_tree.pos_elements_search_1()
        result2 = empty_tree.pos_elements_search_2()

        assert result1 == []
        assert result2 == []

    def test_search_single_node(self):
        """Тест для дерева с одним узлом"""
        tree = BinaryTree()

        # Положительный узел
        tree.insert(42)
        assert tree.pos_elements_search_1() == [42]
        assert tree.pos_elements_search_2() == [42]

        # Отрицательный узел
        tree = BinaryTree()
        tree.insert(-42)
        assert tree.pos_elements_search_1() == []
        assert tree.pos_elements_search_2() == []

        # Ноль
        tree = BinaryTree()
        tree.insert(0)
        assert tree.pos_elements_search_1() == []
        assert tree.pos_elements_search_2() == []

    def test_search_after_deletions(self):
        """Тест поиска после удаления элементов"""
        tree = BinaryTree()
        values = [10, -5, 20, 3, -8, 15, -3]
        for value in values:
            tree.insert(value)

        # Удаляем положительный элемент
        tree.delete(10)
        result = tree.pos_elements_search_1()
        assert 10 not in result
        assert sorted(result) == [3, 15, 20]

        # Удаляем отрицательный элемент
        tree.delete(-5)
        result = tree.pos_elements_search_1()
        assert sorted(result) == [3, 15, 20]

        # Удаляем все положительные
        tree.delete(3)
        tree.delete(15)
        tree.delete(20)
        assert tree.pos_elements_search_1() == []

    def test_search_with_duplicates(self):
        """Тест с дублирующимися значениями"""
        tree = BinaryTree()
        values = [5, 5, -3, 5, 2, -3]
        for value in values:
            tree.insert(value)

        # В бинарном дереве поиска обычно нет дубликатов,
        # но если алгоритм вставки позволяет, то проверяем
        result = tree.pos_elements_search_1()
        # Все положительные числа: все пятерки и двойка
        assert all(x > 0 for x in result)
        assert len([x for x in result if x == 5]) == 3
        assert 2 in result

    def test_search_preserves_order(self):
        """Проверка порядка элементов в результате"""
        tree = BinaryTree()
        # Вставляем в таком порядке
        insert_order = [5, 3, 7, 2, 4, 6, 8]
        for value in insert_order:
            tree.insert(value)

        # pos_elements_search_1 использует inorder обход
        result1 = tree.pos_elements_search_1()
        # Inorder обход должен дать отсортированный список
        assert result1 == [2, 3, 4, 5, 6, 7, 8]

        # pos_elements_search_2 обходит в другом порядке
        result2 = tree.pos_elements_search_2()
        # Проверяем, что все элементы положительные
        assert all(x > 0 for x in result2)
        assert sorted(result2) == [2, 3, 4, 5, 6, 7, 8]


class TestBinaryTreeBasic:
    """Базовые тесты для бинарного дерева"""

    def test_insert_and_search(self):
        """Тест вставки и поиска элементов"""
        tree = BinaryTree()

        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)

        # Проверка поиска существующих элементов
        assert tree.search(10).value == 10
        assert tree.search(5).value == 5
        assert tree.search(15).value == 15
        assert tree.search(3).value == 3
        assert tree.search(7).value == 7

        # Проверка поиска несуществующего элемента
        with pytest.raises(ValueError, match="Такого значения в дереве нет"):
            tree.search(100)

    def test_contains(self):
        """Тест оператора in"""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)

        assert 10 in tree
        assert 5 in tree
        assert 20 not in tree

    def test_is_empty(self):
        """Тест проверки на пустоту"""
        tree = BinaryTree()
        assert tree.is_empty() is True

        tree.insert(10)
        assert tree.is_empty() is False

        tree.delete(10)
        assert tree.is_empty() is True

    def test_size(self):
        """Тест подсчета количества узлов"""
        tree = BinaryTree()
        assert tree.size() == 0

        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        assert tree.size() == 7

        tree.delete(5)
        assert tree.size() == 6

        tree.delete(10)
        assert tree.size() == 5

    def test_min_max(self):
        """Тест поиска минимального и максимального элементов"""
        tree = BinaryTree()
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        assert tree.min().value == 3
        assert tree.max().value == 18

        # Для пустого дерева
        empty_tree = BinaryTree()
        with pytest.raises(ValueError, match="Дерево пусто"):
            empty_tree.min()

    def test_min_max_with_custom_node(self):
        """Тест min/max для конкретного поддерева"""
        tree = BinaryTree()
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        node_10 = tree.search(10)
        node_15 = tree.search(15)

        # Минимум в поддереве с корнем 10 должен быть 3
        assert tree.min(node_10).value == 3
        # Максимум в поддереве с корнем 10 должен быть 18
        assert tree.max(node_10).value == 18
        # Минимум в поддереве с корнем 15 должен быть 12
        assert tree.min(node_15).value == 12
        # Максимум в поддереве с корнем 15 должен быть 18
        assert tree.max(node_15).value == 18


class TestTreeTraversals:
    """Тесты для методов обхода дерева"""

    def setup_method(self):
        """Создаем дерево для тестов обхода"""
        self.tree = BinaryTree()
        # Создаем дерево:
        #        10
        #       /  \
        #      5    15
        #     / \   / \
        #    3   7 12 18
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            self.tree.insert(value)

    def test_preorder_traversal(self):
        """Тест прямого обхода (корень -> левое -> правое)"""
        # Ожидаемый preorder: 10, 5, 3, 7, 15, 12, 18
        result = self.tree.traverse_preorder()
        assert result == [10, 5, 3, 7, 15, 12, 18]

    def test_inorder_traversal(self):
        """Тест симметричного обхода (левое -> корень -> правое)"""
        # Ожидаемый inorder: 3, 5, 7, 10, 12, 15, 18
        result = self.tree.traverse_inorder()
        assert result == [3, 5, 7, 10, 12, 15, 18]

    def test_postorder_traversal(self):
        """Тест обратного обхода (левое -> правое -> корень)"""
        # Ожидаемый postorder: 3, 7, 5, 12, 18, 15, 10
        result = self.tree.traverse_postorder()
        assert result == [3, 7, 5, 12, 18, 15, 10]

    def test_traversals_empty_tree(self):
        """Тест обходов для пустого дерева"""
        empty_tree = BinaryTree()
        assert empty_tree.traverse_preorder() == []
        assert empty_tree.traverse_inorder() == []
        assert empty_tree.traverse_postorder() == []

    def test_traversals_single_node(self):
        """Тест обходов для дерева с одним узлом"""
        tree = BinaryTree()
        tree.insert(42)

        assert tree.traverse_preorder() == [42]
        assert tree.traverse_inorder() == [42]
        assert tree.traverse_postorder() == [42]


class TestTreeDeletion:
    """Тесты для удаления узлов из дерева"""

    def setup_method(self):
        """Создаем дерево для тестов удаления"""
        self.tree = BinaryTree()
        # Создаем дерево:
        #        10
        #       /  \
        #      5    15
        #     / \   / \
        #    3   7 12 18
        #   / \   \
        #  2   4   8
        values = [10, 5, 15, 3, 7, 12, 18, 2, 4, 8]
        for value in values:
            self.tree.insert(value)

    def test_delete_leaf_node(self):
        """Тест удаления листового узла"""
        # Удаляем лист (8)
        assert self.tree.delete(8) is True
        assert 8 not in self.tree
        assert self.tree.size() == 9

        # Проверяем, что остальные элементы на месте
        assert 7 in self.tree
        # Не можем проверить node.right, так как нет доступа

        # Вместо этого проверим, что дерево все еще валидно,
        # выполнив поиск и проверив связи через find_parent
        parent_of_7 = self.tree.find_parent(7)
        assert parent_of_7 is not None  # У 7 должен быть родитель

        # Проверяем, что 8 действительно удален (не находится ни у какого родителя)
        assert self.tree.find_parent(8) is None

    def test_delete_node_with_one_child(self):
        """Тест удаления узла с одним потомком"""
        # Создаем дерево:
        #        10
        #       /  \
        #      5    15
        #     / \   / \
        #    3   7 12 18
        #         \
        #          8
        tree = BinaryTree()
        values = [10, 5, 15, 3, 7, 12, 18, 8]
        for value in values:
            tree.insert(value)

        # Проверяем, что 7 существует и у него есть потомок 8
        assert 7 in tree
        assert 8 in tree

        # Удаляем узел 7 (имеет одного правого потомка 8)
        assert tree.delete(7) is True
        assert 7 not in tree

        # Проверяем, что 8 все еще в дереве (должен быть перемещен на место 7)
        assert 8 in tree

        # Проверяем, что дерево сохранило корректную структуру,
        # выполнив обход и проверив порядок элементов
        inorder = tree.traverse_inorder()
        # После удаления 7, 8 должен занять его место в inorder обходе
        # Ожидаемый inorder: [3, 5, 8, 10, 12, 15, 18]
        assert inorder == [3, 5, 8, 10, 12, 15, 18]

        # Проверяем размер
        assert tree.size() == 7

        # Проверяем, что все остальные элементы на месте
        for value in [3, 5, 8, 10, 12, 15, 18]:
            assert value in tree

    def test_delete_node_with_two_children(self):
        """Тест удаления узла с двумя потомками"""
        # Создаем дерево:
        #        10
        #       /  \
        #      5    15
        #     / \   / \
        #    3   7 12 18
        #   / \   \
        #  2   4   8
        tree = BinaryTree()
        values = [10, 5, 15, 3, 7, 12, 18, 2, 4, 8]
        for value in values:
            tree.insert(value)

        # Удаляем узел 5 (имеет двух потомков)
        assert tree.delete(5) is True
        assert 5 not in tree

        # Проверяем, что все остальные элементы в дереве
        remaining = [2, 3, 4, 7, 8, 10, 12, 15, 18]
        for value in remaining:
            assert value in tree

        # Проверяем размер
        assert tree.size() == 9

        # Проверяем, что дерево сохранило корректную структуру
        # через inorder обход (должен быть отсортирован)
        inorder = tree.traverse_inorder()
        assert inorder == sorted(remaining)
        assert inorder == [2, 3, 4, 7, 8, 10, 12, 15, 18]

        # Проверяем минимальный и максимальный элементы
        assert tree.min().value == 2
        assert tree.max().value == 18

        # Проверяем связи через find_parent (общая проверка структуры)
        # Находим родителя для ключевых узлов
        parent_of_3 = tree.find_parent(3)
        parent_of_7 = tree.find_parent(7)
        parent_of_8 = tree.find_parent(8)
        parent_of_4 = tree.find_parent(4)
        parent_of_2 = tree.find_parent(2)

        # Все эти узлы должны иметь родителя (не None)
        assert parent_of_3 is not None
        assert parent_of_7 is not None
        assert parent_of_8 is not None
        assert parent_of_4 is not None
        assert parent_of_2 is not None

        # Проверяем, что корень (10) не имеет родителя
        assert tree.find_parent(10) is None

        # Проверяем, что правое поддерево (15) не изменилось
        assert tree.find_parent(12).value == 15
        assert tree.find_parent(18).value == 15
        assert tree.find_parent(15).value == 10

    def test_delete_root(self):
        """Тест удаления корневого узла"""
        assert self.tree.delete(10) is True
        assert 10 not in self.tree
        assert self.tree.size() == 9

        # Новым корнем должен стать 12 (минимальный из правого поддерева)
        # Или другой узел в зависимости от реализации

    def test_delete_nonexistent(self):
        """Тест удаления несуществующего элемента"""
        assert self.tree.delete(100) is False
        assert self.tree.size() == 10

    def test_delete_from_empty_tree(self):
        """Тест удаления из пустого дерева"""
        empty_tree = BinaryTree()
        assert empty_tree.delete(10) is False

    def test_find_parent(self):
        """Тест поиска родительского узла"""
        tree = BinaryTree()
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        parent = tree.find_parent(7)
        assert parent is not None
        assert parent.value == 5

        parent = tree.find_parent(5)
        assert parent.value == 10

        parent = tree.find_parent(10)
        assert parent is None  # У корня нет родителя

        parent = tree.find_parent(100)
        assert parent is None  # Несуществующий узел


class TestTreeNode:
    """Тесты для класса TreeNode"""

    def test_node_creation(self):
        """Тест создания узла"""
        node = TreeNode(42)
        assert node.value == 42
        assert node.left is None
        assert node.right is None

    def test_node_properties(self):
        """Тест свойств узла"""
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        node3 = TreeNode(3)

        node1.left = node2
        node1.right = node3

        assert node1.left is node2
        assert node1.right is node3

        # Проверка is_leaf
        assert node1.is_leaf() is False
        assert node2.is_leaf() is True

    def test_node_setters_invalid(self):
        """Тест ошибок при установке некорректных ссылок"""
        node = TreeNode(1)

        with pytest.raises(ValueError, match="Можно присвоить только объект класса TreeNode"):
            node.left = "not a node"

        with pytest.raises(ValueError, match="Можно присвоить только объект класса TreeNode"):
            node.right = 123

    def test_node_str_repr(self):
        """Тест строковых представлений узла"""
        node = TreeNode(42)
        assert str(node) == "Node: 42"
        assert repr(node) == "Node(42)"

        node = TreeNode("hello")
        assert str(node) == "Node: hello"
        assert repr(node) == "Node('hello')"


class TestBinaryTreeAdvanced:
    """Продвинутые тесты для бинарного дерева"""

    def test_iteration(self):
        """Тест итерации по дереву"""
        tree = BinaryTree()
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        # Итерация должна давать элементы в порядке inorder
        result = list(tree)
        assert result == [3, 5, 7, 10, 12, 15, 18]

    def test_complex_tree_structure(self):
        """Тест сложной структуры дерева"""
        tree = BinaryTree()
        # Создаем несбалансированное дерево
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        for value in values:
            tree.insert(value)

        # Проверяем размер
        assert tree.size() == 15

        # Проверяем min/max
        assert tree.min().value == 10
        assert tree.max().value == 85

        # Проверяем наличие всех элементов
        for value in values:
            assert value in tree

    def test_with_different_types(self):
        """Тест с разными типами данных"""
        tree = BinaryTree()

        # Строки
        tree.insert("banana")
        tree.insert("apple")
        tree.insert("cherry")

        assert "apple" in tree
        assert "banana" in tree
        assert "cherry" in tree
        assert tree.min().value == "apple"
        assert tree.max().value == "cherry"

        # Смешивание типов может вызвать ошибки сравнения,
        # но это зависит от реализации


@pytest.mark.parametrize("values, expected_positive", [
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([-1, -2, -3], []),
    ([0, -1, 5, -2, 10], [5, 10]),
    ([3.14, -2.5, 1.5, -0.5], [1.5, 3.14]),
    ([], []),
])
def test_pos_elements_search_parameterized(values, expected_positive):
    """Параметризованный тест поиска положительных элементов"""
    tree = BinaryTree()
    for value in values:
        tree.insert(value)

    result1 = tree.pos_elements_search_1()
    result2 = tree.pos_elements_search_2()

    assert sorted(result1) == sorted(expected_positive)
    assert sorted(result2) == sorted(expected_positive)


@pytest.mark.parametrize("delete_order", [
    [10, 5, 15],
    [3, 7, 12, 18],
    [2, 8, 4],
    [10],
])
def test_deletion_scenarios(delete_order):
    """Параметризованный тест различных сценариев удаления"""
    tree = BinaryTree()
    initial_values = [10, 5, 15, 3, 7, 12, 18, 2, 4, 8]
    for value in initial_values:
        tree.insert(value)

    initial_size = tree.size()

    for i, value in enumerate(delete_order):
        assert tree.delete(value) is True
        assert value not in tree
        assert tree.size() == initial_size - (i + 1)

    # Проверяем, что оставшиеся элементы все еще в дереве
    remaining = set(initial_values) - set(delete_order)
    for value in remaining:
        assert value in tree


def test_display(capsys):
    """Тест метода display (просто проверяем, что не падает)"""
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)

    # display не возвращает значение, а печатает
    tree.display()
    captured = capsys.readouterr()
    assert "-> 10" in captured.out or "10" in captured.out
