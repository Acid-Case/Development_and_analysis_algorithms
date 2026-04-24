from algorithms import dfs, bfs, connected_components
import tkinter as tk
from tkinter import messagebox


graph = {}


def add_edge(entry_u, entry_v, graph_text):
    try:
        u = int(entry_u.get())
        v = int(entry_v.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа")
        return

    graph.setdefault(u, set()).add(v)
    graph.setdefault(v, set()).add(u)

    entry_u.delete(0, tk.END)
    entry_v.delete(0, tk.END)

    update_text(graph_text)


def run_bfs(entry_start, output):
    try:
        start = int(entry_start.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число")
        return

    if start not in graph:
        messagebox.showerror("Ошибка", "Такой вершины нет в графе")
        return

    result = bfs(graph, start)
    output.delete(1.0, tk.END)
    output.insert(tk.END, f"BFS: {result}")


def run_dfs(entry_start, output):
    try:
        start = int(entry_start.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число")
        return

    if start not in graph:
        messagebox.showerror("Ошибка", "Такой вершины нет в графе")
        return

    result = dfs(graph, start)
    output.delete(1.0, tk.END)
    output.insert(tk.END, f"DFS: {result}")


def show_components(output):
    comps = connected_components(graph)
    output.delete(1.0, tk.END)
    output.insert(tk.END, f"Компоненты: {comps}")


def update_text(graph_text):
    graph_text.delete(1.0, tk.END)
    graph_text.insert(tk.END, str({k: list(v) for k, v in graph.items()} if graph else "Пустой граф"))


def clear_graph(graph_text, output):
    graph.clear()
    update_text(graph_text)
    output.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    root.title("Операции с графами")
    root.geometry("500x500")

    graph_text = tk.Text(root, height=5)
    output = tk.Text(root, height=5)

    # ===== Добавление ребра =====
    frame_edges = tk.LabelFrame(root, text="Добавление ребра")
    frame_edges.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(frame_edges, text="u:").grid(row=0, column=0)
    entry_u = tk.Entry(frame_edges, width=10)
    entry_u.grid(row=0, column=1)

    tk.Label(frame_edges, text="v:").grid(row=0, column=2)
    entry_v = tk.Entry(frame_edges, width=10)
    entry_v.grid(row=0, column=3)

    tk.Button(
        frame_edges,
        text="Добавить",
        command=lambda: add_edge(entry_u, entry_v, graph_text)
    ).grid(row=0, column=4)

    # ===== Алгоритмы =====
    frame_algo = tk.LabelFrame(root, text="Обход графа")
    frame_algo.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    tk.Label(frame_algo, text="Старт:").grid(row=0, column=0)
    entry_start = tk.Entry(frame_algo, width=10)
    entry_start.grid(row=0, column=1)

    tk.Button(
        frame_algo,
        text="BFS",
        command=lambda: run_bfs(entry_start, output)
    ).grid(row=0, column=2)

    tk.Button(
        frame_algo,
        text="DFS",
        command=lambda: run_dfs(entry_start, output)
    ).grid(row=0, column=3)

    tk.Button(
        frame_algo,
        text="Компоненты",
        command=lambda: show_components(output)
    ).grid(row=0, column=4)

    # ===== Очистка =====
    tk.Button(
        root,
        text="Очистить граф",
        command=lambda: clear_graph(graph_text, output)
    ).grid(row=2, column=0)

    # ===== Граф =====
    frame_graph = tk.LabelFrame(root, text="Граф")
    frame_graph.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

    graph_text = tk.Text(frame_graph, height=5)
    graph_text.grid(row=0, column=0, sticky="nsew")

    # ===== Вывод =====
    frame_output = tk.LabelFrame(root, text="Результат")
    frame_output.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

    output = tk.Text(frame_output, height=5)
    output.grid(row=0, column=0, sticky="nsew")

    root.mainloop()


if __name__ == "__main__":
    main()
