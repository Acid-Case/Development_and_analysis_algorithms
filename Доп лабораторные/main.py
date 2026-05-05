import math
import tkinter as tk
from tkinter import messagebox, scrolledtext

from algorithms import bellman_ford, bfs, connected_components, dfs, get_path


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Операции с графами")
        self.root.geometry("700x800")

        # Настройка grid для адаптивности
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.graph = {}  # Для невзвешенного графа
        self.weighted_graph = {}  # Для взвешенного графа
        self.mode = "weighted"  # Режим: "unweighted" или "weighted"

        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""

        # ===== Выбор режима =====
        frame_mode = tk.LabelFrame(self.root, text="Режим работы", padx=10, pady=10)
        frame_mode.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.mode_var = tk.StringVar(value="weighted")
        tk.Radiobutton(
            frame_mode,
            text="Невзвешенный граф (BFS, DFS, компоненты)",
            variable=self.mode_var,
            value="unweighted",
            command=self.switch_mode,
        ).grid(row=0, column=0, padx=5, sticky="w")

        tk.Radiobutton(
            frame_mode,
            text="Взвешенный граф (Беллман-Форд)",
            variable=self.mode_var,
            value="weighted",
            command=self.switch_mode,
        ).grid(row=1, column=0, padx=5, sticky="w")

        # ===== Добавление ребра =====
        self.frame_edges = tk.LabelFrame(
            self.root, text="Добавление ребра", padx=10, pady=10
        )
        self.frame_edges.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.setup_edge_input()

        # ===== Алгоритмы =====
        self.frame_algo = tk.LabelFrame(self.root, text="Алгоритмы", padx=10, pady=10)
        self.frame_algo.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.setup_algorithms()

        # ===== Управление графом =====
        frame_control = tk.Frame(self.root)
        frame_control.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        frame_control.grid_columnconfigure(0, weight=1)
        frame_control.grid_columnconfigure(1, weight=1)

        tk.Button(
            frame_control,
            text="Очистить граф",
            command=self.clear_graph,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, padx=(0, 5), sticky="ew")

        tk.Button(
            frame_control,
            text="Пример графа",
            command=self.load_example,
            bg="#607D8B",
            fg="white",
            font=("Arial", 10),
        ).grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # ===== Визуализация графа =====
        frame_vis = tk.LabelFrame(
            self.root, text="Визуализация графа", padx=10, pady=10
        )
        frame_vis.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        frame_vis.grid_rowconfigure(0, weight=1)
        frame_vis.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(frame_vis, bg="white", height=350)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # ===== Текстовое представление графа =====
        frame_text = tk.LabelFrame(
            self.root, text="Текстовое представление", padx=10, pady=10
        )
        frame_text.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")
        frame_text.grid_rowconfigure(0, weight=1)
        frame_text.grid_columnconfigure(0, weight=1)

        self.graph_text = scrolledtext.ScrolledText(frame_text, height=5, wrap=tk.WORD)
        self.graph_text.grid(row=0, column=0, sticky="nsew")

        # ===== Вывод результатов =====
        frame_output = tk.LabelFrame(
            self.root, text="Результаты алгоритмов", padx=10, pady=10
        )
        frame_output.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")
        frame_output.grid_rowconfigure(0, weight=1)
        frame_output.grid_columnconfigure(0, weight=1)

        self.output = scrolledtext.ScrolledText(
            frame_output, height=8, wrap=tk.WORD, font=("Courier", 10)
        )
        self.output.grid(row=0, column=0, sticky="nsew")

    def setup_edge_input(self):
        """Настройка ввода ребра в зависимости от режима"""
        # Очищаем frame
        for widget in self.frame_edges.winfo_children():
            widget.destroy()

        if self.mode == "unweighted":
            tk.Label(self.frame_edges, text="Из вершины:").grid(
                row=0, column=0, padx=(0, 5)
            )
            self.entry_u = tk.Entry(self.frame_edges, width=8)
            self.entry_u.grid(row=0, column=1, padx=(0, 10))

            tk.Label(self.frame_edges, text="В вершину:").grid(
                row=0, column=2, padx=(0, 5)
            )
            self.entry_v = tk.Entry(self.frame_edges, width=8)
            self.entry_v.grid(row=0, column=3, padx=(0, 10))

            tk.Button(
                self.frame_edges,
                text="Добавить ребро",
                command=self.add_edge_unweighted,
                bg="#4CAF50",
                fg="white",
            ).grid(row=0, column=4, padx=(10, 0))
        else:
            tk.Label(self.frame_edges, text="Из вершины:").grid(
                row=0, column=0, padx=(0, 5)
            )
            self.entry_u = tk.Entry(self.frame_edges, width=8)
            self.entry_u.grid(row=0, column=1, padx=(0, 10))

            tk.Label(self.frame_edges, text="В вершину:").grid(
                row=0, column=2, padx=(0, 5)
            )
            self.entry_v = tk.Entry(self.frame_edges, width=8)
            self.entry_v.grid(row=0, column=3, padx=(0, 10))

            tk.Label(self.frame_edges, text="Вес:").grid(row=0, column=4, padx=(0, 5))
            self.entry_weight = tk.Entry(self.frame_edges, width=6)
            self.entry_weight.grid(row=0, column=5, padx=(0, 10))

            tk.Button(
                self.frame_edges,
                text="Добавить ребро",
                command=self.add_edge_weighted,
                bg="#4CAF50",
                fg="white",
            ).grid(row=0, column=6, padx=(10, 0))

    def setup_algorithms(self):
        """Настройка кнопок алгоритмов в зависимости от режима"""
        for widget in self.frame_algo.winfo_children():
            widget.destroy()

        if self.mode == "unweighted":
            tk.Label(self.frame_algo, text="Стартовая вершина:").grid(
                row=0, column=0, padx=(0, 5)
            )
            self.entry_start = tk.Entry(self.frame_algo, width=8)
            self.entry_start.grid(row=0, column=1, padx=(0, 10))

            tk.Button(
                self.frame_algo,
                text="BFS",
                command=self.run_bfs,
                bg="#2196F3",
                fg="white",
                width=8,
            ).grid(row=0, column=2, padx=2)

            tk.Button(
                self.frame_algo,
                text="DFS",
                command=self.run_dfs,
                bg="#FF9800",
                fg="white",
                width=8,
            ).grid(row=0, column=3, padx=2)

            tk.Button(
                self.frame_algo,
                text="Компоненты",
                command=self.show_components,
                bg="#9C27B0",
                fg="white",
                width=12,
            ).grid(row=0, column=4, padx=(10, 0))
        else:
            tk.Label(self.frame_algo, text="Стартовая вершина:").grid(
                row=0, column=0, padx=(0, 5)
            )
            self.entry_start = tk.Entry(self.frame_algo, width=8)
            self.entry_start.grid(row=0, column=1, padx=(0, 10))

            tk.Button(
                self.frame_algo,
                text="Беллман-Форд",
                command=self.run_bellman_ford,
                bg="#E91E63",
                fg="white",
                width=15,
            ).grid(row=0, column=2, padx=(10, 0))

    def switch_mode(self):
        """Переключение между режимами"""
        self.mode = self.mode_var.get()
        self.clear_graph()
        self.setup_edge_input()
        self.setup_algorithms()

    def add_edge_unweighted(self):
        """Добавление ребра в невзвешенный граф"""
        try:
            u = int(self.entry_u.get().strip())
            v = int(self.entry_v.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа для вершин!")
            return

        if u == v:
            messagebox.showwarning("Предупреждение", "Петли не добавляются")
            return

        self.graph.setdefault(u, set()).add(v)
        self.graph.setdefault(v, set()).add(u)

        self.entry_u.delete(0, tk.END)
        self.entry_v.delete(0, tk.END)

        self.update_all()

    def add_edge_weighted(self):
        """Добавление ориентированного взвешенного ребра"""
        try:
            u = int(self.entry_u.get().strip())
            v = int(self.entry_v.get().strip())
            weight = float(self.entry_weight.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа! Вес может быть дробным.")
            return

        if u not in self.weighted_graph:
            self.weighted_graph[u] = []
        if v not in self.weighted_graph:
            self.weighted_graph[v] = []

        # Обновляем существующее ориентированное ребро u -> v
        for i, (neighbor, _) in enumerate(self.weighted_graph[u]):
            if neighbor == v:
                self.weighted_graph[u][i] = (v, weight)
                break
        else:
            self.weighted_graph[u].append((v, weight))

        # Для визуализации оставляем обычный граф неориентированным
        self.graph.setdefault(u, set()).add(v)
        self.graph.setdefault(v, set()).add(u)

        self.entry_u.delete(0, tk.END)
        self.entry_v.delete(0, tk.END)
        self.entry_weight.delete(0, tk.END)

        self.update_all()

    def run_bfs(self):
        """Запуск BFS"""
        start = self.get_start_vertex()
        if start is None:
            return

        result = bfs(self.graph, start)
        self.update_output(f"BFS от вершины {start}:\n{result}")

    def run_dfs(self):
        """Запуск DFS"""
        start = self.get_start_vertex()
        if start is None:
            return

        result = dfs(self.graph, start)
        self.update_output(f"DFS от вершины {start}:\n{result}")

    def run_bellman_ford(self):
        """Запуск алгоритма Беллмана-Форда"""
        start = self.get_start_vertex()
        if start is None:
            return

        if not self.weighted_graph:
            self.update_output("Граф пуст. Добавьте рёбра.")
            return

        distances, predecessors, has_negative_cycle, cycle_path, affected_vertices = (
            bellman_ford(self.weighted_graph, start)
        )

        output_text = f"Алгоритм Беллмана-Форда от вершины {start}\n"
        output_text += "=" * 60 + "\n\n"

        if has_negative_cycle:
            output_text += "⚠️  ОБНАРУЖЕН ОТРИЦАТЕЛЬНЫЙ ЦИКЛ!  ⚠️\n\n"

            if cycle_path:
                output_text += f"Цикл: {' → '.join(map(str, cycle_path))}\n"

                # Вычисляем вес цикла
                cycle_weight = 0
                for i in range(len(cycle_path) - 1):
                    u, v = cycle_path[i], cycle_path[i + 1]
                    found = False
                    if u in self.weighted_graph:
                        for neighbor, w in self.weighted_graph[u]:
                            if neighbor == v:
                                cycle_weight += w
                                found = True
                                break
                    if not found:
                        # Пробуем обратное ребро
                        if v in self.weighted_graph:
                            for neighbor, w in self.weighted_graph[v]:
                                if neighbor == u:
                                    cycle_weight += w
                                    break
                output_text += f"Вес цикла: {cycle_weight}\n\n"

            output_text += "Как интерпретировать результаты:\n"
            output_text += "• '-∞' - вершина затронута отрицательным циклом\n"
            output_text += "• '∞' - вершина недостижима из стартовой\n"
            output_text += (
                "• число - кратчайшее расстояние (путь не проходит через цикл)\n\n"
            )

        # Таблица результатов
        output_text += "-" * 70 + "\n"
        output_text += f"{'Вершина':<10} {'Расстояние':<15} {'Путь'}\n"
        output_text += "-" * 70 + "\n"

        for vertex in sorted(distances.keys()):
            if vertex == start:
                output_text += f"{vertex:<10} 0{'':<13} {start}\n"
            elif distances[vertex] == float("-inf"):
                output_text += (
                    f"{vertex:<10} -∞{'':<12} затронута отрицательным циклом\n"
                )
            elif distances[vertex] == float("inf"):
                output_text += f"{vertex:<10} ∞{'':<13} недостижима\n"
            else:
                # Восстанавливаем путь только для незатронутых вершин
                if vertex not in affected_vertices:
                    path = get_path(predecessors, start, vertex)
                    path_str = " → ".join(map(str, path)) if path else "путь не найден"
                else:
                    path_str = "путь не определён (затронута циклом)"
                output_text += f"{vertex:<10} {distances[vertex]:<15} {path_str}\n"

        output_text += "-" * 70 + "\n\n"

        # Статистика
        output_text += "Статистика:\n"
        output_text += f"  Всего вершин в графе: {len(distances)}\n"

        if has_negative_cycle:
            cycle_vertices = set(cycle_path[:-1]) if cycle_path else set()
            cycle_count = len(cycle_vertices)
            affected_count = len(affected_vertices)
            normal_count = sum(
                1
                for v in distances
                if distances[v] not in [float("inf"), float("-inf")] and v != start
            )
            unreachable_count = sum(
                1 for v in distances if distances[v] == float("inf")
            )

            output_text += f"  Вершин в отрицательном цикле: {cycle_count}\n"
            output_text += f"  Вершин с корректными путями: {normal_count}\n"
            output_text += f"  Вершин, затронутых циклом: {affected_count}\n"
            output_text += f"  Недостижимых вершин: {unreachable_count}\n"

            # Добавляем пояснение
            if start not in cycle_vertices and 0 not in affected_vertices:
                output_text += f"\n  ✓ Вершина {start} НЕ затронута циклом\n"
        else:
            reachable = sum(
                1 for v in distances if v != start and distances[v] != float("inf")
            )
            output_text += f"  Достижимых вершин: {reachable}\n"
            if reachable > 0:
                max_dist = max(
                    distances[v]
                    for v in distances
                    if v != start and distances[v] not in [float("inf"), float("-inf")]
                )
                output_text += f"  Максимальное расстояние: {max_dist}\n"

        self.update_output(output_text)

    def get_start_vertex(self):
        """Получение и проверка стартовой вершины"""
        try:
            start = int(self.entry_start.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число для стартовой вершины!")
            return None

        graph_to_check = (
            self.weighted_graph if hasattr(self, "weighted_graph") else self.graph
        )

        if start not in graph_to_check:
            messagebox.showerror("Ошибка", f"Вершина {start} отсутствует в графе!")
            return None

        return start

    def show_components(self):
        """Показать компоненты связности"""
        if not self.graph:
            self.update_output("Граф пуст. Компоненты связности отсутствуют.")
            return

        components = connected_components(self.graph)
        self.update_output(
            f"Найдено компонент связности: {len(components)}\n\n{components}"
        )

    def clear_graph(self):
        """Очистка графа"""
        self.graph.clear()
        self.weighted_graph.clear()
        self.canvas.delete("all")
        self.graph_text.delete(1.0, tk.END)
        self.graph_text.insert(tk.END, "Граф пуст")
        self.output.delete(1.0, tk.END)

    def load_example(self):
        """Загрузка примера графа в зависимости от режима"""
        self.clear_graph()

        if self.mode == "unweighted":
            example_edges = [(1, 2), (1, 3), (2, 4), (3, 4), (5, 6), (6, 7)]
            for u, v in example_edges:
                self.graph.setdefault(u, set()).add(v)
                self.graph.setdefault(v, set()).add(u)
        else:
            example_edges = [
                (1, 2, 4),
                (1, 3, 2),
                (2, 3, -1),
                (2, 4, 3),
                (3, 4, 2),
                (3, 5, 4),
                (4, 5, -3),
                (5, 6, 2),
                (4, 6, 1),
            ]
            for u, v, w in example_edges:
                if u not in self.weighted_graph:
                    self.weighted_graph[u] = []
                if v not in self.weighted_graph:
                    self.weighted_graph[v] = []

                # Только ориентированное ребро u -> v
                self.weighted_graph[u].append((v, w))

                # Для визуализации оставляем неориентированное отображение
                self.graph.setdefault(u, set()).add(v)
                self.graph.setdefault(v, set()).add(u)

        self.update_all()
        self.update_output("Загружен пример графа")

    def update_all(self):
        """Обновление всех представлений графа"""
        self.update_graph_text()
        self.draw_graph()

    def update_graph_text(self):
        """Обновление текстового представления графа"""
        self.graph_text.delete(1.0, tk.END)

        if self.mode == "weighted" and self.weighted_graph:
            text = "Взвешенный граф:\n"
            for u in sorted(self.weighted_graph.keys()):
                edges = self.weighted_graph[u]
                if edges:
                    edges_str = ", ".join([f"{v}({w})" for v, w in sorted(edges)])
                    text += f"  {u}: [{edges_str}]\n"
            self.graph_text.insert(tk.END, text)
        elif self.graph:
            formatted = {k: sorted(list(v)) for k, v in sorted(self.graph.items())}
            self.graph_text.insert(tk.END, f"Невзвешенный граф:\n{formatted}")
        else:
            self.graph_text.insert(tk.END, "Граф пуст")

    def update_output(self, text):
        """Обновление поля вывода результатов"""
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)

    def draw_graph(self):
        """Рисование графа на canvas"""
        self.canvas.delete("all")

        nodes = sorted(set(list(self.graph.keys()) + list(self.weighted_graph.keys())))
        if not nodes:
            return

        # Динамический радиус
        width = self.canvas.winfo_width() or 600
        height = self.canvas.winfo_height() or 350
        cx, cy = width // 2, height // 2
        radius = min(width, height) // 3

        positions = {}

        # Расстановка вершин по кругу
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes) - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            positions[node] = (x, y)

        # Рисуем рёбра
        drawn_edges = {}
        for u in self.graph:
            for v in self.graph[u]:
                edge = tuple(sorted([u, v]))
                if edge not in drawn_edges:
                    x1, y1 = positions[u]
                    x2, y2 = positions[v]

                    # Определяем вес ребра
                    weight_text = ""
                    color = "#666"
                    if self.mode == "weighted" and u in self.weighted_graph:
                        for neighbor, w in self.weighted_graph[u]:
                            if neighbor == v:
                                weight_text = str(w)
                                color = (
                                    "red" if w < 0 else ("green" if w > 0 else "#666")
                                )
                                break

                    # Рисуем линию
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

                    # Рисуем вес ребра (со смещением от линии)
                    if weight_text:
                        mid_x = (x1 + x2) / 2
                        mid_y = (y1 + y2) / 2

                        # Небольшое смещение вверх от линии
                        offset = 15
                        self.canvas.create_text(
                            mid_x,
                            mid_y - offset,
                            text=weight_text,
                            fill=color,
                            font=("Arial", 9, "bold"),
                        )

                    drawn_edges[edge] = True

        # Рисуем вершины
        for node, (x, y) in positions.items():
            r = 20
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r, fill="#4CAF50", outline="#2E7D32", width=2
            )
            self.canvas.create_text(
                x, y, text=str(node), font=("Arial", 10, "bold"), fill="white"
            )


def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
