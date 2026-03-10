# Разработать алгоритм и программу поиска положительных элементов в
# каждой строке матрицы.
from random import randint
from typing import Iterator


class Matrix:
    def __init__(self, row: int, col: int, fill_value: float | int = 0) -> None:
        if not (isinstance(row, int) and row > 0):
            raise ValueError("Некорректное значение для строки")
        if not (isinstance(col, int) and col > 0):
            raise ValueError("Некорректное значение для столбца")
        if not isinstance(fill_value, (int, float)):
            raise ValueError("Некорректное значение для числа заполнения")

        self.__row = row
        self.__col = col
        self.__fill_value = fill_value
        self.__matrix = self.__create_matrix()

    def get_positive_numbers(self) -> list[list[int | float]]:
        return [[x for x in row if x > 0] for row in self.__matrix]

    def print_positive_numbers(self) -> None:
        print(f"Матрица из {self.__row} строк")
        pos_numbers = self.get_positive_numbers()

        for i, row in enumerate(pos_numbers):
            str_row: list[str] = list(map(str, row))
            print(f"В строке №{i + 1} положительных чисел: {len(str_row)}")
            print(", ".join(str_row if str_row else ["Нет"]) + '\n')

    @classmethod
    def create_matrix_random(cls, row: int, col: int, start: int = -50, end: int = 50):
        matrix = Matrix(row, col)
        for i in range(row):
            for j in range(col):
                matrix.__matrix[i][j] = randint(start, end)
        return matrix

    def transpose(self) -> "Matrix":
        result = Matrix(self.__col, self.__row, self.__fill_value)
        for i in range(self.__col):
            for j in range(self.__row):
                result.__matrix[i][j] = self.__matrix[j][i]
        return result

    def copy(self) -> "Matrix":
        new_matrix = Matrix(self.__row, self.__col, self.__fill_value)
        for i in range(self.__row):
            for j in range(self.__col):
                new_matrix[i, j] = self[i, j]
        return new_matrix

    @staticmethod
    def identity(size: int) -> "Matrix":
        result = Matrix(size, size, 0)
        for i in range(size):
            result.__matrix[i][i] = 1
        return result

    def __create_matrix(self) -> list[list[int | float]]:
        return [[self.__fill_value] * self.__col for _ in range(self.__row)]

    def __validate_index(self, row: int, col: int) -> None:
        if not (isinstance(row, int) and 0 <= row < self.__row):
            raise IndexError("Некорректное значение для строки")
        if not (isinstance(col, int) and 0 <= col < self.__col):
            raise IndexError("Некорректное значение для столбца")

    def __add__(self, other: "Matrix") -> "Matrix":
        if isinstance(other, Matrix):
            if self.__row != other.row or self.__col != other.col:
                raise ValueError(
                    f"Несовместимые размеры: {self.__row}x{self.__col} и {other.row}x{other.col} "
                    "Матрицы должны быть равны"
                )

            result = Matrix(self.__row, self.__col)
            for i in range(self.__row):
                for j in range(self.__col):
                    result.__matrix[i][j] = self.__matrix[i][j] + other.__matrix[i][j]
            return result

        raise NotImplementedError("Невозможно сложить с объектом этого типа")

    def __sub__(self, other: "Matrix") -> "Matrix":
        if isinstance(other, Matrix):
            if self.__row != other.row or self.__col != other.col:
                raise ValueError(
                    f"Несовместимые размеры: {self.__row}x{self.__col} и {other.row}x{other.col} "
                    "Матрицы должны быть равны"
                )

            result = Matrix(self.__row, self.__col)
            for i in range(self.__row):
                for j in range(self.__col):
                    result.__matrix[i][j] = self.__matrix[i][j] - other.__matrix[i][j]
            return result

        raise NotImplementedError("Невозможно вычесть объект этого типа")

    def __mul__(self, other: "int | float | Matrix") -> "Matrix":
        if isinstance(other, (int, float)):
            result = Matrix(self.__row, self.__col)
            for i in range(self.__row):
                for j in range(self.__col):
                    result.__matrix[i][j] = self.__matrix[i][j] * other

            return result
        elif isinstance(other, Matrix):
            if self.__col != other.row:
                raise ValueError(
                    f"Несовместимые размеры: {self.__row}x{self.__col} и {other.row}x{other.col} "
                    f"Количество столбцов первой матрицы ({self.__col}) должно быть равно "
                    f"количеству строк второй матрицы ({other.row})"
                )

            result = Matrix(self.__row, other.col)
            for i in range(self.__row):
                for j in range(other.col):
                    total: int | float = 0
                    for k in range(self.__col):
                        total += self.__matrix[i][k] * other.__matrix[k][j]
                    result.__matrix[i][j] = total

            return result

        raise NotImplementedError("Невозможно умножить на объект этого типа")

    def __rmul__(self, other: int | float) -> "Matrix":
        return self.__mul__(other)

    def __getitem__(self, key: tuple[int, int]) -> int | float:
        row, col = key
        self.__validate_index(row, col)
        return self.__matrix[row][col]

    def __setitem__(self, key: tuple[int, int], value: int | float) -> None:
        row, col = key
        self.__validate_index(row, col)
        if not (isinstance(value, (int, float))):
            raise ValueError("Некорректное значение")
        self.__matrix[row][col] = value

    def __iter__(self) -> Iterator:
        return iter(self.__matrix)

    def __len__(self) -> int:
        return self.__row

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col

    @property
    def fill_value(self) -> int | float:
        return self.__fill_value

    def __str__(self) -> str:
        res = f"Matrix  Row: {self.__row}, Col: {self.__col}\n"

        return res + '\n'.join(str(i) for i in self.__matrix) + '\n'

    def __repr__(self) -> str:
        return f"Matrix({self.__row!r}, {self.__col!r}, {self.__fill_value!r})"


def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: необходимо ввести целое число. Попробуйте снова.")


def get_range() -> tuple[int, int]:
    while True:
        try:
            start = int(input("Введите начало диапазона: "))
            end = int(input("Введите конец диапазона: "))

            if start > end:
                print(f"Ошибка: начало диапазона {start} не может быть больше конца {end}.")
                print("Попробуйте снова.")
                continue

            return start, end
        except ValueError:
            print("Ошибка: необходимо ввести целые числа. Попробуйте снова.")


def main():
    row = get_int("Введите кол-во строк: ")
    col = get_int("Введите кол-во столбцов: ")
    start, end = get_range()

    matrix = Matrix.create_matrix_random(row, col, start, end)

    print("\nИсходная матрица:")
    print(matrix)
    matrix.print_positive_numbers()


if __name__ == "__main__":
    main()
