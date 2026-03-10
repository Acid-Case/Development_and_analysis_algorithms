import pytest
from io import StringIO
import sys
from labrab import Matrix, get_int, get_range


class TestMatrixPositiveNumbers:
    """Основные тесты для методов get_positive_numbers и print_positive_numbers"""

    def test_get_positive_numbers_basic(self):
        """Базовый тест получения положительных чисел"""
        matrix = Matrix(3, 3)
        test_data = [
            [-5, 10, -3],
            [0, 7, -2],
            [15, -8, 4]
        ]

        for i in range(3):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        expected = [[10], [7], [15, 4]]
        assert matrix.get_positive_numbers() == expected

    def test_get_positive_numbers_edge_cases(self):
        """Тест граничных случаев (все отр, все полож, с нулями)"""
        matrix = Matrix(3, 3)

        # Тест 1: все отрицательные
        for i in range(3):
            for j in range(3):
                matrix[i, j] = -1
        assert matrix.get_positive_numbers() == [[], [], []]

        # Тест 2: все положительные
        for i in range(3):
            for j in range(3):
                matrix[i, j] = 5
        assert matrix.get_positive_numbers() == [[5, 5, 5], [5, 5, 5], [5, 5, 5]]

        # Тест 3: с нулями
        test_data = [[0, 5, 0], [-3, 0, 7], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                matrix[i, j] = test_data[i][j]
        assert matrix.get_positive_numbers() == [[5], [7], []]

    def test_print_positive_numbers_output(self):
        """Тест вывода положительных чисел"""
        matrix = Matrix(2, 2)
        test_data = [[-1, 5], [3, -4]]

        for i in range(2):
            for j in range(2):
                matrix[i, j] = test_data[i][j]

        captured_output = StringIO()
        sys.stdout = captured_output
        matrix.print_positive_numbers()
        sys.stdout = sys.__stdout__

        expected = ("Матрица из 2 строк\n"
                   "В строке №1 положительных чисел: 1\n"
                   "5\n\n"
                   "В строке №2 положительных чисел: 1\n"
                   "3\n\n")

        assert captured_output.getvalue() == expected


class TestSecondaryFunctions:
    """Тесты для второстепенных функций get_int и get_range"""

    def test_get_int_valid_input(self, monkeypatch):
        """Тест get_int с корректным вводом"""
        monkeypatch.setattr('sys.stdin', StringIO('42\n'))
        result = get_int("Введите число: ")
        assert result == 42

    def test_get_int_invalid_then_valid_input(self, monkeypatch):
        """Тест get_int с неверным, затем верным вводом"""
        monkeypatch.setattr('sys.stdin', StringIO('abc\n42\n'))
        result = get_int("Введите число: ")
        assert result == 42

    def test_get_int_negative_number(self, monkeypatch):
        """Тест get_int с отрицательным числом"""
        monkeypatch.setattr('sys.stdin', StringIO('-15\n'))
        result = get_int("Введите число: ")
        assert result == -15

    def test_get_range_valid_input(self, monkeypatch):
        """Тест get_range с корректным вводом"""
        monkeypatch.setattr('sys.stdin', StringIO('1\n10\n'))
        start, end = get_range()
        assert (start, end) == (1, 10)

    def test_get_range_start_greater_than_end(self, monkeypatch):
        """Тест get_range когда start > end (с последующей коррекцией)"""
        monkeypatch.setattr('sys.stdin', StringIO('10\n1\n5\n15\n'))
        start, end = get_range()
        assert (start, end) == (5, 15)

    def test_get_range_invalid_then_valid(self, monkeypatch):
        """Тест get_range с неверным (не числа), затем верным вводом"""
        monkeypatch.setattr('sys.stdin', StringIO('abc\ndef\n1\n10\n'))
        start, end = get_range()
        assert (start, end) == (1, 10)

    def test_get_range_with_negative_numbers(self, monkeypatch):
        """Тест get_range с отрицательными числами"""
        monkeypatch.setattr('sys.stdin', StringIO('-10\n-5\n'))
        start, end = get_range()
        assert (start, end) == (-10, -5)

    def test_get_range_zero_range(self, monkeypatch):
        """Тест get_range с одинаковыми числами (нулевой диапазон)"""
        monkeypatch.setattr('sys.stdin', StringIO('5\n5\n'))
        start, end = get_range()
        assert (start, end) == (5, 5)


class TestMatrixAdditionalFeatures:
    """Дополнительные тесты для других методов Matrix"""

    def test_matrix_creation(self):
        """Тест создания матрицы"""
        # Корректное создание
        matrix = Matrix(2, 3, 5)
        assert matrix.row == 2
        assert matrix.col == 3
        assert matrix.fill_value == 5

        # Проверка заполнения
        for i in range(2):
            for j in range(3):
                assert matrix[i, j] == 5

        # Некорректное создание
        with pytest.raises(IndexError):
            Matrix(0, 3)
        with pytest.raises(IndexError):
            Matrix(2, -1)
        with pytest.raises(ValueError):
            Matrix(2, 3, "string")

    def test_matrix_indexing(self):
        """Тест доступа по индексу"""
        matrix = Matrix(2, 2)

        # Установка значений
        matrix[0, 0] = 10
        matrix[0, 1] = 20
        matrix[1, 0] = 30
        matrix[1, 1] = 40

        # Чтение значений
        assert matrix[0, 0] == 10
        assert matrix[0, 1] == 20
        assert matrix[1, 0] == 30
        assert matrix[1, 1] == 40

        # Проверка выхода за границы
        with pytest.raises(IndexError):
            matrix[2, 0]
        with pytest.raises(IndexError):
            matrix[0, 2]

    def test_matrix_operations(self):
        """Тест арифметических операций с матрицами"""
        m1 = Matrix(2, 2)
        m2 = Matrix(2, 2)

        # Заполняем матрицы
        m1[0, 0], m1[0, 1], m1[1, 0], m1[1, 1] = 1, 2, 3, 4
        m2[0, 0], m2[0, 1], m2[1, 0], m2[1, 1] = 5, 6, 7, 8

        # Сложение
        m3 = m1 + m2
        assert m3[0, 0] == 6
        assert m3[1, 1] == 12

        # Вычитание
        m4 = m1 - m2
        assert m4[0, 0] == -4
        assert m4[1, 1] == -4

        # Умножение на число
        m5 = m1 * 3
        assert m5[0, 0] == 3
        assert m5[1, 1] == 12

    def test_matrix_transpose_and_copy(self):
        """Тест транспонирования и копирования"""
        matrix = Matrix(2, 3)
        test_data = [[1, 2, 3], [4, 5, 6]]

        for i in range(2):
            for j in range(3):
                matrix[i, j] = test_data[i][j]

        # Транспонирование
        transposed = matrix.transpose()
        assert transposed.row == 3
        assert transposed.col == 2
        assert transposed[0, 0] == 1
        assert transposed[1, 0] == 2
        assert transposed[0, 1] == 4

        # Копирование
        copied = matrix.copy()
        assert copied.row == matrix.row
        assert copied.col == matrix.col
        assert copied[0, 0] == matrix[0, 0]

        # Изменение копии не влияет на оригинал
        copied[0, 0] = 100
        assert matrix[0, 0] == 1
        assert copied[0, 0] == 100

    def test_identity_matrix(self):
        """Тест создания единичной матрицы"""
        identity = Matrix.identity(3)

        assert identity.row == 3
        assert identity.col == 3

        # Проверка единичной матрицы
        for i in range(3):
            for j in range(3):
                if i == j:
                    assert identity[i, j] == 1
                else:
                    assert identity[i, j] == 0

    def test_create_matrix_random(self):
        """Тест создания случайной матрицы"""
        matrix = Matrix.create_matrix_random(2, 3, -10, 10)

        assert matrix.row == 2
        assert matrix.col == 3

        # Проверка, что все значения в заданном диапазоне
        for i in range(2):
            for j in range(3):
                assert -10 <= matrix[i, j] <= 10


@pytest.mark.parametrize("row, col, fill_value, expected_row, expected_col", [
    (2, 3, 0, 2, 3),
    (1, 1, 5, 1, 1),
    (3, 2, -10, 3, 2),
])
def test_matrix_parameterized(row, col, fill_value, expected_row, expected_col):
    """Параметризованный тест создания матрицы с разными параметрами"""
    matrix = Matrix(row, col, fill_value)
    assert matrix.row == expected_row
    assert matrix.col == expected_col
    assert matrix.fill_value == fill_value


@pytest.mark.parametrize("test_input, expected", [
    ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
    ([[-1, -2], [-3, -4]], [[], []]),
    ([[0, 5], [-1, 7]], [[5], [7]]),
])
def test_get_positive_numbers_parameterized(test_input, expected):
    """Параметризованный тест для разных случаев положительных чисел"""
    matrix = Matrix(len(test_input), len(test_input[0]))

    for i in range(len(test_input)):
        for j in range(len(test_input[0])):
            matrix[i, j] = test_input[i][j]

    assert matrix.get_positive_numbers() == expected


def test_main_function_exists():
    """Проверка существования функции main"""
    from labrab import main
    assert callable(main)


def test_matrix_string_representation():
    """Тест строкового представления матрицы"""
    matrix = Matrix(2, 2, 5)
    matrix[0, 0] = 1
    matrix[0, 1] = 2
    matrix[1, 0] = 3
    matrix[1, 1] = 4

    str_repr = str(matrix)
    assert "Matrix  Row: 2, Col: 2" in str_repr
    assert "[1, 2]" in str_repr
    assert "[3, 4]" in str_repr

    repr_repr = repr(matrix)
    assert repr_repr == "Matrix(2, 2, 5)"
