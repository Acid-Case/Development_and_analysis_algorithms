import pytest
from labrab3 import Queue, Node


class TestQueueFindMethods:
    """Тесты для методов find_one и find_all класса Queue"""

    def setup_method(self):
        """Создаем очередь с тестовыми данными перед каждым тестом"""
        self.queue = Queue()
        self.test_data = [10, 20, 30, 40, 50]
        for value in self.test_data:
            self.queue.push(value)

    def test_find_one_basic(self):
        """Базовый тест поиска элемента по индексу"""
        assert self.queue.find_one(0) == 10
        assert self.queue.find_one(1) == 20
        assert self.queue.find_one(2) == 30
        assert self.queue.find_one(3) == 40
        assert self.queue.find_one(4) == 50

    def test_find_one_with_different_types(self):
        """Тест поиска элементов разных типов"""
        queue = Queue()
        test_data = [42, "hello", 3.14, None, [1, 2], {"key": "value"}]
        
        for value in test_data:
            queue.push(value)
        
        assert queue.find_one(0) == 42
        assert queue.find_one(1) == "hello"
        assert queue.find_one(2) == 3.14
        assert queue.find_one(3) is None
        assert queue.find_one(4) == [1, 2]
        assert queue.find_one(5) == {"key": "value"}

    def test_find_one_index_error(self):
        """Тест ошибки при выходе индекса за пределы"""
        with pytest.raises(IndexError, match="Индекс вышел за пределы очереди: 5"):
            self.queue.find_one(5)
        
        with pytest.raises(IndexError, match="Индекс вышел за пределы очереди: 10"):
            self.queue.find_one(10)

    def test_find_one_value_error(self):
        """Тест ошибки при некорректном типе индекса"""
        with pytest.raises(ValueError, match="Индекс должен быть целым положительным числом: -1"):
            self.queue.find_one(-1)
        
        with pytest.raises(ValueError, match="Индекс должен быть целым положительным числом: 1.5"):
            self.queue.find_one(1.5)
        
        with pytest.raises(ValueError, match="Индекс должен быть целым положительным числом: abc"):
            self.queue.find_one("abc")

    def test_find_one_empty_queue(self):
        """Тест поиска в пустой очереди"""
        empty_queue = Queue()
        
        with pytest.raises(IndexError, match="Индекс вышел за пределы очереди: 0"):
            empty_queue.find_one(0)

    def test_find_one_last_element(self):
        """Тест поиска последнего элемента"""
        assert self.queue.find_one(4) == 50
        
        # Добавляем еще элемент и проверяем новый последний
        self.queue.push(60)
        assert self.queue.find_one(5) == 60

    def test_find_one_first_element(self):
        """Тест поиска первого элемента после операций"""
        assert self.queue.find_one(0) == 10
        
        # Удаляем первый элемент и проверяем новый первый
        self.queue.pop()
        assert self.queue.find_one(0) == 20

    def test_find_all_basic(self):
        """Базовый тест поиска нескольких элементов по списку индексов"""
        result = self.queue.find_all([0, 2, 4])
        assert result == [10, 30, 50]

    def test_find_all_with_tuple(self):
        """Тест поиска с кортежем индексов"""
        result = self.queue.find_all((1, 3))
        assert result == [20, 40]

    def test_find_all_with_range(self):
        """Тест поиска с range"""
        result = self.queue.find_all(range(2, 5))
        assert result == [30, 40, 50]

    def test_find_all_with_set(self):
        """Тест поиска с множеством индексов"""
        result = self.queue.find_all({0, 3, 1})
        # Множество неупорядоченное, но результат должен соответствовать порядку перебора
        # В Python множества итерируются в порядке добавления, но для надежности используем sorted
        assert sorted(result) == [10, 20, 40]

    def test_find_all_empty_iterable(self):
        """Тест поиска с пустым итерируемым объектом"""
        result = self.queue.find_all([])
        assert result == []
        
        result = self.queue.find_all(())
        assert result == []
        
        result = self.queue.find_all(range(0))
        assert result == []

    def test_find_all_with_invalid_indices(self):
        """Тест поиска с некорректными индексами"""
        # Один некорректный индекс должен вызвать ошибку
        with pytest.raises(IndexError):
            self.queue.find_all([1, 5, 3])
        
        with pytest.raises(ValueError):
            self.queue.find_all([1, -2, 3])

    def test_find_all_mixed_valid_invalid(self):
        """Тест с перемешанными корректными и некорректными индексами"""
        # Проверяем, что ошибка возникает при любом некорректном индексе
        with pytest.raises(IndexError):
            self.queue.find_all([0, 1, 10, 2])
        
        with pytest.raises(ValueError):
            self.queue.find_all([0, -1, 2])

    def test_find_all_value_error_not_iterable(self):
        """Тест ошибки при передаче неитерируемого объекта"""
        with pytest.raises(ValueError, match="Индексы должны быть итерируемыми"):
            self.queue.find_all(123)
        
        with pytest.raises(ValueError, match="Индексы должны быть итерируемыми"):
            self.queue.find_all(None)

    def test_find_all_value_error_string(self):
        """Тест ошибки при передаче строки (особый случай)"""
        with pytest.raises(ValueError, match="Индексы не могут быть строкой"):
            self.queue.find_all("123")
        
        with pytest.raises(ValueError, match="Индексы не могут быть строкой"):
            self.queue.find_all("0,1,2")

    def test_find_all_after_modifications(self):
        """Тест поиска после изменений в очереди"""
        # Удаляем элемент
        self.queue.pop()  # удаляем 10
        
        # Добавляем новые элементы
        self.queue.push(60)
        self.queue.push(70)
        
        result = self.queue.find_all([0, 2, 4])
        # Ожидаем: [20, 40, 60]
        assert result == [20, 40, 60]
        assert self.queue.find_one(5) == 70

    def test_find_all_with_duplicate_indices(self):
        """Тест поиска с дублирующимися индексами"""
        result = self.queue.find_all([1, 1, 2, 2])
        assert result == [20, 20, 30, 30]

    def test_find_all_out_of_order(self):
        """Тест поиска с индексами не по порядку"""
        result = self.queue.find_all([4, 0, 2])
        assert result == [50, 10, 30]

    def test_find_all_preserves_order(self):
        """Тест сохранения порядка индексов в результате"""
        indices = [3, 1, 4, 0, 2]
        result = self.queue.find_all(indices)
        assert result == [40, 20, 50, 10, 30]
        assert [self.test_data[i] for i in indices] == result


class TestQueueAdditionalMethods:
    """Дополнительные тесты для других методов Queue"""

    def test_push_and_size(self):
        """Тест добавления элементов и размера"""
        queue = Queue()
        assert len(queue) == 0
        assert queue.size() == 0
        
        queue.push(1)
        assert len(queue) == 1
        assert queue.size() == 1
        
        queue.push(2)
        assert len(queue) == 2
        assert queue.size() == 2

    def test_pop(self):
        """Тест удаления элементов"""
        queue = Queue()
        queue.push(1)
        queue.push(2)
        queue.push(3)
        
        assert queue.pop() == 1
        assert queue.pop() == 2
        assert queue.pop() == 3
        
        with pytest.raises(IndexError, match="Очередь пуста"):
            queue.pop()

    def test_front(self):
        """Тест получения первого элемента без удаления"""
        queue = Queue()
        queue.push(1)
        queue.push(2)
        
        assert queue.front() == 1
        assert queue.size() == 2  # Размер не изменился
        
        queue.pop()
        assert queue.front() == 2
        
        queue.pop()
        with pytest.raises(IndexError, match="Очередь пуста"):
            queue.front()

    def test_is_empty(self):
        """Тест проверки на пустоту"""
        queue = Queue()
        assert queue.is_empty() is True
        
        queue.push(1)
        assert queue.is_empty() is False
        
        queue.pop()
        assert queue.is_empty() is True

    def test_clear(self):
        """Тест очистки очереди"""
        queue = Queue()
        for i in range(5):
            queue.push(i)
        
        assert queue.size() == 5
        assert queue.is_empty() is False
        
        queue.clear()
        
        assert queue.size() == 0
        assert queue.is_empty() is True
        
        # После очистки очередь должна работать как новая
        queue.push(42)
        assert queue.front() == 42

    def test_str_and_display(self):
        """Тест строкового представления"""
        queue = Queue()
        assert str(queue) == "Queue(None)"
        
        queue.push(1)
        queue.push(2)
        queue.push(3)
        
        expected = "Queue(1 -> 2 -> 3 -> None)"
        assert str(queue) == expected

    def test_iteration(self):
        """Тест итерации по очереди"""
        queue = Queue()
        test_data = [1, 2, 3, 4, 5]
        
        for value in test_data:
            queue.push(value)
        
        # Проверка итерации
        result = [node.value for node in queue]
        assert result == test_data
        
        # Проверка индексации через enumerate
        for i, node in enumerate(queue):
            assert node.value == test_data[i]

    def test_len(self):
        """Тест магического метода __len__"""
        queue = Queue()
        assert len(queue) == 0
        
        queue.push(1)
        assert len(queue) == 1
        
        queue.push(2)
        assert len(queue) == 2
        
        queue.pop()
        assert len(queue) == 1


class TestNodeClass:
    """Тесты для класса Node"""

    def test_node_creation(self):
        """Тест создания узла"""
        node = Node(42)
        assert node.value == 42
        assert node.next is None

    def test_node_value_setter(self):
        """Тест изменения значения узла"""
        node = Node(42)
        node.value = 100
        assert node.value == 100

    def test_node_next_setter(self):
        """Тест установки ссылки на следующий узел"""
        node1 = Node(1)
        node2 = Node(2)
        
        node1.next = node2
        assert node1.next is node2
        assert node2.next is None

    def test_node_next_setter_invalid(self):
        """Тест ошибки при установке некорректной ссылки"""
        node = Node(1)
        
        with pytest.raises(ValueError, match="Невозможно назначить ссылку на этот объект"):
            node.next = "not a node"
        
        with pytest.raises(ValueError, match="Невозможно назначить ссылку на этот объект"):
            node.next = 123

    def test_node_str_and_repr(self):
        """Тест строковых представлений узла"""
        node = Node(42)
        assert str(node) == "Node: 42"
        assert repr(node) == "Node(42)"
        
        node = Node("hello")
        assert str(node) == "Node: hello"
        assert repr(node) == "Node('hello')"


class TestIntegration:
    """Интеграционные тесты"""

    def test_queue_lifecycle_with_find(self):
        """Тест полного жизненного цикла очереди с поиском"""
        queue = Queue()
        
        # Добавляем элементы
        for i in range(10):
            queue.push(i * 10)
        
        # Проверяем поиск
        assert queue.find_all([0, 5, 9]) == [0, 50, 90]
        
        # Удаляем несколько элементов
        for _ in range(3):
            queue.pop()
        
        # Проверяем после удаления
        assert queue.find_one(0) == 30  # Теперь первый элемент - 30
        assert queue.find_all([0, 3, 5]) == [30, 60, 80]
        
        # Очищаем очередь
        queue.clear()
        
        # Проверяем, что очередь пуста
        with pytest.raises(IndexError):
            queue.find_one(0)

    def test_find_all_with_complex_operations(self):
        """Тест find_all с комплексными операциями"""
        queue = Queue()
        
        # Добавляем разнотипные данные
        queue.push(42)
        queue.push("string")
        queue.push([1, 2, 3])
        queue.push({"a": 1})
        queue.push(None)
        
        # Ищем элементы
        result = queue.find_all([0, 2, 4])
        assert result == [42, [1, 2, 3], None]
        
        # Удаляем средний элемент
        queue.pop()  # удаляем 42
        queue.pop()  # удаляем "string"
        
        # Проверяем оставшиеся
        result = queue.find_all([0, 1, 2])
        assert result == [[1, 2, 3], {"a": 1}, None]


@pytest.mark.parametrize("index, expected", [
    (0, 10),
    (1, 20),
    (2, 30),
    (3, 40),
    (4, 50),
])
def test_find_one_parameterized(index, expected):
    """Параметризованный тест find_one"""
    queue = Queue()
    for value in [10, 20, 30, 40, 50]:
        queue.push(value)
    
    assert queue.find_one(index) == expected


@pytest.mark.parametrize("indices, expected", [
    ([0, 1, 2], [10, 20, 30]),
    ([4, 3, 2], [50, 40, 30]),
    ((0, 2, 4), [10, 30, 50]),
    (range(1, 4), [20, 30, 40]),
])
def test_find_all_parameterized(indices, expected):
    """Параметризованный тест find_all"""
    queue = Queue()
    for value in [10, 20, 30, 40, 50]:
        queue.push(value)
    
    assert queue.find_all(indices) == expected


@pytest.mark.parametrize("invalid_index", [
    -1, 5, 10, "0", 1.5, None
])
def test_find_one_invalid_inputs(invalid_index):
    """Параметризованный тест некорректных входных данных для find_one"""
    queue = Queue()
    for value in [10, 20, 30, 40, 50]:
        queue.push(value)
    
    with pytest.raises((IndexError, ValueError)):
        queue.find_one(invalid_index)


@pytest.mark.parametrize("invalid_indices", [
    [1, -2, 3],
    [0, 5, 2],
    "123",
    123,
    None,
])
def test_find_all_invalid_inputs(invalid_indices):
    """Параметризованный тест некорректных входных данных для find_all"""
    queue = Queue()
    for value in [10, 20, 30, 40, 50]:
        queue.push(value)
    
    with pytest.raises((IndexError, ValueError)):
        queue.find_all(invalid_indices)