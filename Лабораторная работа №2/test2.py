import pytest
from copy import deepcopy
from labrab2 import Matrix


class TestMatrixSorting:
    """Тесты для методов сортировки матрицы"""

    def test_create_flat_list_basic(self):
        """Тест создания плоского списка из матрицы"""
        matrix = Matrix(2, 3)
        test_data = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        flat_list = matrix.create_flat_list()
        assert flat_list == [1, 2, 3, 4, 5, 6]

    def test_create_flat_list_mixed_values(self):
        """Тест создания плоского списка со смешанными значениями"""
        matrix = Matrix(2, 2)
        test_data = [
            [-5, 10],
            [3.14, -8]
        ]

        for i in range(2):
            for j in range(2):
                matrix[i, j] = test_data[i][j]

        flat_list = matrix.create_flat_list()
        assert flat_list == [-5, 10, 3.14, -8]

    def test_binary_search_basic(self):
        """Тест бинарного поиска для определения позиции вставки"""
        matrix = Matrix(1, 1)

        # Тест 1: поиск позиции для вставки 4 в отсортированную часть [1, 3, 5, 7]
        sorted_part = [1, 3, 5, 7]
        index = matrix._Matrix__binary_search(sorted_part, 3, 4)
        assert index == 2

        # Тест 2: вставка в начало
        index = matrix._Matrix__binary_search(sorted_part, 3, 0)
        assert index == 0

        # Тест 3: вставка в конец
        index = matrix._Matrix__binary_search(sorted_part, 3, 8)
        assert index == 4

        # Тест 4: вставка равного элемента
        index = matrix._Matrix__binary_search(sorted_part, 3, 5)
        assert index == 3

    def test_binary_search_edge_cases(self):
        """Тест граничных случаев бинарного поиска"""
        matrix = Matrix(1, 1)

        # Пустой список
        index = matrix._Matrix__binary_search([], -1, 5)
        assert index == 0

        # Список с одним элементом
        index = matrix._Matrix__binary_search([5], 0, 3)
        assert index == 0
        index = matrix._Matrix__binary_search([5], 0, 7)
        assert index == 1

        # Отрицательные числа
        sorted_neg = [-10, -5, -3, 0]
        index = matrix._Matrix__binary_search(sorted_neg, 3, -7)
        assert index == 1

        # Все элементы больше ключа
        index = matrix._Matrix__binary_search([10, 20, 30], 2, 5)
        assert index == 0

        # Все элементы меньше ключа
        index = matrix._Matrix__binary_search([10, 20, 30], 2, 40)
        assert index == 3

    def test_shift_insert_basic(self):
        """Тест сдвига элементов и вставки значения в существующем списке"""
        matrix = Matrix(1, 1)

        # Тест 1: вставка в середину (сдвиг элементов вправо)
        test_list = [1, 2, 4, 5, 3]  # 3 - текущий элемент для вставки в отсортированную часть [1, 2, 4, 5]
        matrix._Matrix__shift_insert(test_list, 3, 3, 2)
        assert test_list == [1, 2, 3, 4, 5]

        # Тест 2: вставка в начало
        test_list = [2, 3, 4, 5, 1]  # 1 - текущий элемент для вставки
        matrix._Matrix__shift_insert(test_list, 3, 1, 0)
        assert test_list == [1, 2, 3, 4, 5]

        # Тест 3: вставка в конец
        test_list = [1, 2, 3, 4, 5]  # 5 уже на месте
        matrix._Matrix__shift_insert(test_list, 3, 5, 4)
        assert test_list == [1, 2, 3, 4, 5]

        # Тест 4: вставка с элементом, который уже стоит на правильной позиции
        test_list = [1, 3, 5, 7, 5]  # Последний элемент 5 должен вставиться между 3 и 5
        matrix._Matrix__shift_insert(test_list, 3, 5, 2)
        assert test_list == [1, 3, 5, 5, 7]

    def test_shift_insert_comprehensive(self):
        """Комплексный тест операции сдвига и вставки"""
        matrix = Matrix(1, 1)

        # Моделируем процесс сортировки вставками с бинарным поиском
        test_list = [5, 2, 4, 1, 3]

        # Шаг 1: i=1, key=2, вставка в начало
        matrix._Matrix__shift_insert(test_list, 0, 2, 0)
        assert test_list == [2, 5, 4, 1, 3]

        # Шаг 2: i=2, key=4, вставка между 2 и 5
        matrix._Matrix__shift_insert(test_list, 1, 4, 1)
        assert test_list == [2, 4, 5, 1, 3]

        # Шаг 3: i=3, key=1, вставка в начало
        matrix._Matrix__shift_insert(test_list, 2, 1, 0)
        assert test_list == [1, 2, 4, 5, 3]

        # Шаг 4: i=4, key=3, вставка между 2 и 4
        matrix._Matrix__shift_insert(test_list, 3, 3, 2)
        assert test_list == [1, 2, 3, 4, 5]

    def test_update_matrix_basic(self):
        """Тест обновления матрицы из плоского списка"""
        matrix = Matrix(2, 3)
        test_data = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        # Создаем отсортированный плоский список
        flat_list = [1, 2, 3, 4, 5, 6]
        matrix._Matrix__update_matrix(flat_list)

        # Проверяем, что матрица обновилась правильно
        assert matrix[0, 0] == 1
        assert matrix[0, 1] == 2
        assert matrix[0, 2] == 3
        assert matrix[1, 0] == 4
        assert matrix[1, 1] == 5
        assert matrix[1, 2] == 6

    def test_update_matrix_reshaped(self):
        """Тест обновления матрицы с измененным порядком элементов"""
        matrix = Matrix(2, 3)
        test_data = [
            [6, 5, 4],
            [3, 2, 1]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        # Обновляем с новым плоским списком
        flat_list = [1, 2, 3, 4, 5, 6]
        matrix._Matrix__update_matrix(flat_list)

        # Проверяем новое расположение
        assert matrix[0, 0] == 1
        assert matrix[0, 1] == 2
        assert matrix[0, 2] == 3
        assert matrix[1, 0] == 4
        assert matrix[1, 1] == 5
        assert matrix[1, 2] == 6

    def test_sort_matrix_basic(self):
        """Базовый тест сортировки матрицы"""
        matrix = Matrix(2, 3)
        test_data = [
            [3, 1, 4],
            [1, 5, 2]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        original_copy = deepcopy(test_data)
        matrix.sort_matrix()

        # Проверяем, что матрица отсортирована по строкам
        expected = [
            [1, 1, 2],
            [3, 4, 5]
        ]

        for i in range(2):
            for j in range(3):
                assert matrix[i, j] == expected[i][j]

        # Проверяем, что элементы те же самые (просто переставлены)
        flat_before = [num for row in original_copy for num in row]
        flat_after = matrix.create_flat_list()
        assert sorted(flat_before) == flat_after

    def test_sort_matrix_algorithm_steps(self):
        """Тест, проверяющий корректность алгоритма сортировки бинарными вставками"""
        matrix = Matrix(2, 2)
        test_data = [
            [4, 1],
            [3, 2]
        ]

        for i in range(2):
            for j in range(2):
                matrix[i, j] = test_data[i][j]

        # Плоский список до сортировки: [4, 1, 3, 2]
        flat_before = matrix.create_flat_list()
        assert flat_before == [4, 1, 3, 2]

        # Выполняем сортировку
        matrix.sort_matrix()

        # Плоский список после сортировки должен быть отсортирован
        flat_after = matrix.create_flat_list()
        assert flat_after == [1, 2, 3, 4]

        # Проверяем структуру матрицы
        expected = [
            [1, 2],
            [3, 4]
        ]

        for i in range(2):
            for j in range(2):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_already_sorted(self):
        """Тест сортировки уже отсортированной матрицы"""
        matrix = Matrix(2, 3)
        test_data = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        # Матрица должна остаться той же
        expected = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        for i in range(2):
            for j in range(3):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_reverse_sorted(self):
        """Тест сортировки обратно отсортированной матрицы"""
        matrix = Matrix(2, 3)
        test_data = [
            [6, 5, 4],
            [3, 2, 1]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        expected = [
            [1, 2, 3],
            [4, 5, 6]
        ]

        for i in range(2):
            for j in range(3):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_with_negatives(self):
        """Тест сортировки матрицы с отрицательными числами"""
        matrix = Matrix(2, 3)
        test_data = [
            [-3, 5, -1],
            [0, -2, 4]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        expected = [
            [-3, -2, -1],
            [0, 4, 5]
        ]

        for i in range(2):
            for j in range(3):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_with_floats(self):
        """Тест сортировки матрицы с числами с плавающей точкой"""
        matrix = Matrix(2, 2)
        test_data = [
            [3.14, 1.5],
            [2.7, 0.5]
        ]

        for i in range(2):
            for j in range(2):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        expected = [
            [0.5, 1.5],
            [2.7, 3.14]
        ]

        for i in range(2):
            for j in range(2):
                assert abs(matrix[i, j] - expected[i][j]) < 0.0001

    def test_sort_matrix_single_row(self):
        """Тест сортировки матрицы с одной строкой"""
        matrix = Matrix(1, 4)
        test_data = [
            [3, 1, 4, 2]
        ]

        for i in range(1):
            for j in range(4):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        expected = [
            [1, 2, 3, 4]
        ]

        for i in range(1):
            for j in range(4):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_single_column(self):
        """Тест сортировки матрицы с одним столбцом"""
        matrix = Matrix(4, 1)
        test_data = [
            [5],
            [2],
            [4],
            [1]
        ]

        for i in range(4):
            for j in range(1):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        expected = [
            [1],
            [2],
            [4],
            [5]
        ]

        for i in range(4):
            for j in range(1):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_1x1(self):
        """Тест сортировки матрицы 1x1"""
        matrix = Matrix(1, 1)
        matrix[0, 0] = 42

        matrix.sort_matrix()
        assert matrix[0, 0] == 42

    def test_sort_matrix_with_duplicates(self):
        """Тест сортировки матрицы с дубликатами"""
        matrix = Matrix(2, 3)
        test_data = [
            [3, 1, 3],
            [2, 1, 2]
        ]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        matrix.sort_matrix()

        expected = [
            [1, 1, 2],
            [2, 3, 3]
        ]

        for i in range(2):
            for j in range(3):
                assert matrix[i, j] == expected[i][j]

    def test_sort_matrix_large(self):
        """Тест сортировки большой матрицы"""
        size = 10
        matrix = Matrix.create_matrix_random(size, size, -100, 100)

        # Сохраняем все элементы до сортировки
        flat_before = matrix.create_flat_list()

        # Сортируем
        matrix.sort_matrix()

        # Получаем элементы после сортировки
        flat_after = matrix.create_flat_list()

        # Проверяем, что элементы те же самые
        assert sorted(flat_before) == flat_after

        # Проверяем, что плоский список отсортирован
        assert flat_after == sorted(flat_before)

        # Проверяем структуру матрицы (размеры не изменились)
        assert matrix.row == size
        assert matrix.col == size

    def test_sort_matrix_preserves_dimensions(self):
        """Тест сохранения размерности матрицы после сортировки"""
        matrix = Matrix(3, 4)
        test_data = [
            [9, 8, 7, 6],
            [5, 4, 3, 2],
            [1, 0, -1, -2]
        ]

        for i in range(3):
            for j in range(4):
                matrix[i, j] = test_data[i][j]

        original_row = matrix.row
        original_col = matrix.col

        matrix.sort_matrix()

        assert matrix.row == original_row
        assert matrix.col == original_col


class TestIntegration:
    """Интеграционные тесты для всего процесса сортировки"""

    def test_sort_matrix_full_process(self):
        """Тест полного процесса сортировки"""
        # Создаем матрицу
        matrix = Matrix(3, 3)
        test_data = [
            [9, 2, 7],
            [4, 6, 5],
            [8, 3, 1]
        ]

        for i in range(3):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        # Сохраняем состояние до сортировки
        flat_before = matrix.create_flat_list()

        # Сортируем
        matrix.sort_matrix()

        # Проверяем по шагам:

        # 1. Плоский список должен быть отсортирован
        flat_after = matrix.create_flat_list()
        assert flat_after == sorted(flat_before)

        # 2. Каждая строка должна быть частью общего отсортированного списка
        all_elements = []
        for i in range(matrix.row):
            for j in range(matrix.col):
                all_elements.append(matrix[i, j])

        assert all_elements == sorted(flat_before)

        # 3. Количество элементов сохранилось
        assert len(all_elements) == matrix.row * matrix.col

    def test_sort_matrix_with_random_values(self):
        """Тест сортировки случайно сгенерированной матрицы"""
        for _ in range(5):  # Проверяем несколько раз для надежности
            rows = pytest.random.randint(1, 5) if hasattr(pytest, 'random') else 3
            cols = pytest.random.randint(1, 5) if hasattr(pytest, 'random') else 4

            matrix = Matrix.create_matrix_random(rows, cols, -20, 20)

            # Сохраняем элементы до сортировки
            elements_before = [matrix[i, j] for i in range(rows) for j in range(cols)]

            # Сортируем
            matrix.sort_matrix()

            # Получаем элементы после сортировки
            elements_after = [matrix[i, j] for i in range(rows) for j in range(cols)]

            # Проверяем, что элементы те же, но отсортированы
            assert sorted(elements_before) == elements_after


@pytest.mark.parametrize("test_input, expected", [
    ([[3, 1, 2]], [[1, 2, 3]]),
    ([[3], [1], [2]], [[1], [2], [3]]),
    ([[5, 4], [3, 2], [1, 0]], [[0, 1], [2, 3], [4, 5]]),
    ([[-3, -1, -2]], [[-3, -2, -1]]),
])
def test_sort_matrix_parameterized(test_input, expected):
    """Параметризованный тест сортировки для разных случаев"""
    rows = len(test_input)
    cols = len(test_input[0]) if rows > 0 else 0

    matrix = Matrix(rows, cols)

    for i in range(rows):
        for j in range(cols):
            matrix[i, j] = test_input[i][j]

    matrix.sort_matrix()

    for i in range(rows):
        for j in range(cols):
            assert matrix[i, j] == expected[i][j]


def test_private_methods_interaction():
    """Тест взаимодействия приватных методов в процессе сортировки"""
    matrix = Matrix(2, 3)
    test_data = [
        [5, 2, 4],
        [1, 3, 6]
    ]

    for i in range(2):
        for j in range(3):
            matrix[i, j] = test_data[i][j]

    # Ручная симуляция процесса сортировки бинарными вставками
    flat_list = matrix.create_flat_list()  # [5, 2, 4, 1, 3, 6]

    # Сортируем вручную используя бинарный поиск и сдвиг
    for i in range(1, len(flat_list)):
        key = flat_list[i]
        right = i - 1
        ind = matrix._Matrix__binary_search(flat_list, right, key)
        matrix._Matrix__shift_insert(flat_list, right, key, ind)

    # Проверяем, что плоский список отсортирован
    assert flat_list == [1, 2, 3, 4, 5, 6]

    # Обновляем матрицу
    matrix._Matrix__update_matrix(flat_list)

    # Проверяем результат
    expected = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    for i in range(2):
        for j in range(3):
            assert matrix[i, j] == expected[i][j]
