from typing import Any, Optional, Iterable


class Node:
    __slots__ = ("__value", "__next")

    def __init__(self, value: Any) -> None:
        self.__value = value
        self.__next: Optional["Node"] = None

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def value(self, value: Any) -> None:
        self.__value = value

    @property
    def next(self) -> Optional["Node"]:
        return self.__next

    @next.setter
    def next(self, next: Optional["Node"]) -> None:
        if isinstance(next, Node) or next is None:
            self.__next = next
        else:
            raise ValueError("Невозможно назначить ссылку на этот объект")

    def __str__(self) -> str:
        return f"Node: {self.__value}"

    def __repr__(self) -> str:
        return f"Node({self.__value!r})"


class Queue:
    def __init__(self) -> None:
        self.__front: Optional[Node] = None
        self.__end: Optional[Node] = None
        self.__size: int = 0

    def find_one(self, p: int) -> Any:
        if not (isinstance(p, int) and p >= 0):
            raise ValueError(f"Индекс должен быть целым положительным числом: {p}")
        if p >= self.__size:
            raise IndexError(f"Индекс вышел за пределы очереди: {p}")

        for ind, node in enumerate(self):
            if ind == p:
                return node.value

    def find_all(self, p: Iterable) -> list[Any]:
        if not (isinstance(p, Iterable)):
            raise ValueError("Индексы должны быть итерируемыми")
        if isinstance(p, str):
            raise ValueError("Индексы не могут быть строкой")

        return [self.find_one(i) for i in p]

    def push(self, value: Any) -> None:
        node = Node(value)

        if self.__front is None:
            self.__front = node
            self.__end = node
        else:
            self.__end.next = node
            self.__end = node
        self.__size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Очередь пуста")

        result = self.__front.value
        self.__front = self.__front.next
        if not self.__front:
            self.__end = None
        self.__size -= 1
        return result

    def is_empty(self) -> bool:
        return self.__size == 0

    def size(self) -> int:
        return self.__size

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.__front.value

    def clear(self) -> None:
        self.__front = None
        self.__end = None
        self.__size = 0

    def display(self) -> None:
        print(f"Queue: {' -> '.join([str(node.value) for node in self])} -> None")

    def __iter__(self):
        node = self.__front
        while node:
            yield node
            node = node.next

    def __len__(self) -> int:
        return self.__size

    def __str__(self) -> str:
        if self.is_empty():
            return "Queue(None)"
        return f"Queue({' -> '.join([str(node.value) for node in self])} -> None)"


def main():
    q = Queue()
    arr = [10, 20, 30, 40, 50]

    for i in arr:
        q.push(i)

    q.pop()

    q.push(60)
    q.push(70)

    print(q.find_all([0, 2, 4]))

    q.clear()


if __name__ == "__main__":
    main()
