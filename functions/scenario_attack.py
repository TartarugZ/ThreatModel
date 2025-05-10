import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict

from data_base import db_model
from data_base.db_controller import get_all_some


def find_all_paths(edges, start, end):
    # Создаем словарь смежности для представления графа
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # Для неориентированного графа

    def dfs(current, end, visited, path, all_paths):
        if current == end:
            all_paths.append(path[:])
            return
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, end, visited, path, all_paths)
                path.pop()
                visited.remove(neighbor)

    all_paths = []
    visited = {start}
    path = [start]
    dfs(start, end, visited, path, all_paths)
    return all_paths


# def save_paths_to_file(paths, start, end, filename="functions/scenario_attack_output/paths.txt"):
#     with open(filename, 'w') as f:
#         if not paths:
#             f.write(f"No paths found from {start} to {end}.\n")
#         else:
#             f.write(f"All paths from {start} to {end}:\n")
#             for i, path in enumerate(paths, 1):
#                 f.write(f"Path {i}: {' -> '.join(map(str, path))}\n")


def visualize_graph(edges, start, end, output_file, node_labels, highlight_path=None):
    # Создаем граф с помощью networkx
    G = nx.Graph()
    G.add_edges_from(edges)

    # Позиции вершин для визуализации
    pos = nx.spring_layout(G)

    # Рисуем граф
    plt.figure(figsize=(8, 6))

    # Рисуем все ребра (серый цвет)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1)

    # Рисуем выделенный маршрут (красный цвет), если он есть
    if highlight_path:
        highlight_edges = [(highlight_path[i], highlight_path[i + 1]) for i in range(len(highlight_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='red', width=2)

    # Рисуем вершины
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)

    # Рисуем метки вершин
    labels = node_labels if node_labels else {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    # Подписи для начальной и конечной вершин
    nx.draw_networkx_nodes(G, pos, nodelist=[start, end], node_color=['green', 'orange'], node_size=500)

    plt.title(f"Отображение сценария (путь от устройства {start} до устройства {end})")
    plt.axis('off')
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    # plt.show()


def do_scenario(connected_devices, first, second):
    matplotlib.use('Agg')
    # Пример использования

    edges = connected_devices
    start = first
    end = second
    node_labels = {
        1: "Информационная\nбезопасность\nПК",
        4: "Сервер\nдля\nвнутренних\nсервисов",
        5: "Системный\nадминистратор\nПК",
        7: "Сервер\nдля\nобслуживания\nклиентов"
    }

    # Находим все маршруты
    paths = find_all_paths(edges, start, end)

    # Сохраняем маршруты в файл
    # save_paths_to_file(paths, start, end)

    # Выводим маршруты в консоль
    if paths:
        print(f"All paths from {start} to {end}:")
        for i, path in enumerate(paths, 1):
            print(f"Path {i}: {path}")
    else:
        print(f"No paths from {start} to {end}.")

    # Визуализируем граф (если он есть)
    if paths:
        for i in paths:
            visualize_graph(edges, start, end, highlight_path=i, node_labels=node_labels, output_file=f"functions/scenario_attack_output/graph{i}.png")
