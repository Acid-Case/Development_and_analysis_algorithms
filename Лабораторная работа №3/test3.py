from labrab3 import Queue


def test_1():
    # Тест 1: Базовая работа
    q = Queue()
    q.push(1)
    q.push(2)
    assert q.front() == 1
    assert q.pop() == 1
    assert q.front() == 2
    assert q.size() == 1


def test_2():
    # Тест 2: Очистка
    q = Queue()
    q.push(1)
    q.push(2)

    q.clear()
    assert q.is_empty()
    assert q.size() == 0


def test_3():
    # Тест 3: Pop из пустой
    q = Queue()
    try:
        q.pop()
        assert False, "Должно быть исключение"
    except IndexError:
        pass


def test_4():
    # Тест 4: Один элемент
    q = Queue()
    q.push(42)
    assert q.pop() == 42
    assert q.is_empty()


def test_5():
    # Тест 5: Много элементов
    q = Queue()
    for i in range(100):
        q.push(i)
    assert q.size() == 100
    for i in range(100):
        assert q.pop() == i
    assert q.is_empty()
