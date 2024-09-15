#Nombre: Aldo Emiliano Chavez Lares
#Registro: 21310238
#Grupo: 7F1

import matplotlib.pyplot as plt
import networkx as nx

# Nombres de ciudades y distancias reales aproximadas (en kilómetros)
cities = {
    'Nueva York': 'New York',
    'Los Ángeles': 'Los Angeles',
    'Chicago': 'Chicago',
    'Houston': 'Houston',
    'Phoenix': 'Phoenix',
    'Filadelfia': 'Philadelphia',
    'San Antonio': 'San Antonio',
    'San Diego': 'San Diego',
    'Dallas': 'Dallas',
    'San José': 'San Jose'
}

# Distancias aproximadas entre las ciudades (en kilómetros)
distances = {
    ('Nueva York', 'Los Ángeles'): 4500,
    ('Nueva York', 'Chicago'): 1200,
    ('Nueva York', 'Houston'): 2500,
    ('Nueva York', 'Phoenix'): 3700,
    ('Nueva York', 'Filadelfia'): 150,
    ('Nueva York', 'San Antonio'): 2500,
    ('Nueva York', 'San Diego'): 4100,
    ('Nueva York', 'Dallas'): 2200,
    ('Nueva York', 'San José'): 4100,
    ('Los Ángeles', 'Chicago'): 2800,
    ('Los Ángeles', 'Houston'): 2300,
    ('Los Ángeles', 'Phoenix'): 600,
    ('Los Ángeles', 'Filadelfia'): 4000,
    ('Los Ángeles', 'San Antonio'): 2000,
    ('Los Ángeles', 'San Diego'): 200,
    ('Los Ángeles', 'Dallas'): 2200,
    ('Los Ángeles', 'San José'): 80,
    ('Chicago', 'Houston'): 1600,
    ('Chicago', 'Phoenix'): 2400,
    ('Chicago', 'Filadelfia'): 1300,
    ('Chicago', 'San Antonio'): 1700,
    ('Chicago', 'San Diego'): 2400,
    ('Chicago', 'Dallas'): 1300,
    ('Chicago', 'San José'): 2300,
    ('Houston', 'Phoenix'): 1700,
    ('Houston', 'Filadelfia'): 2200,
    ('Houston', 'San Antonio'): 300,
    ('Houston', 'San Diego'): 2200,
    ('Houston', 'Dallas'): 1000,
    ('Houston', 'San José'): 2400,
    ('Phoenix', 'Filadelfia'): 3500,
    ('Phoenix', 'San Antonio'): 1800,
    ('Phoenix', 'San Diego'): 600,
    ('Phoenix', 'Dallas'): 1700,
    ('Phoenix', 'San José'): 1500,
    ('Filadelfia', 'San Antonio'): 2300,
    ('Filadelfia', 'San Diego'): 4000,
    ('Filadelfia', 'Dallas'): 2000,
    ('Filadelfia', 'San José'): 4100,
    ('San Antonio', 'San Diego'): 2000,
    ('San Antonio', 'Dallas'): 300,
    ('San Antonio', 'San José'): 2300,
    ('San Diego', 'Dallas'): 1900,
    ('San Diego', 'San José'): 80,
    ('Dallas', 'San José'): 2300
}

def create_graph(cities, distances):
    graph = nx.Graph()
    for city in cities.keys():
        graph.add_node(city)
    for (city1, city2), dist in distances.items():
        graph.add_edge(city1, city2, weight=dist)
    return graph

def calculate_route_distance(graph, route):
    distance = 0
    for i in range(len(route) - 1):
        distance += graph[route[i]][route[i + 1]]['weight']
    distance += graph[route[-1]][route[0]]['weight']  # Vuelta al inicio
    return distance

def two_opt(graph, initial_route):
    best_route = initial_route
    best_distance = calculate_route_distance(graph, best_route)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route)):
                if j - i == 1: continue
                new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                new_distance = calculate_route_distance(graph, new_route)
                if new_distance < best_distance:
                    best_route, best_distance = new_route, new_distance
                    improved = True
    return best_route, best_distance

def plot_graph_with_route(graph, route, cities, title):
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(12, 10))
    nx.draw(graph, pos, with_labels=True, labels={city: city for city in cities.keys()}, node_color='lightblue', node_size=5000, font_size=12, font_weight='bold')
    edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)] + [(route[-1], route[0])]
    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)
    
    # Añadir explicación textual en el gráfico
    explanation = (
        "Este gráfico muestra la ruta óptima encontrada para entregar productos a las ciudades.\n"
        "La ruta se calcula usando un algoritmo de búsqueda local (2-opt) que intenta mejorar la\n"
        "ruta inicial intercambiando pares de aristas para reducir la distancia total. La ruta en rojo\n"
        "es la más corta encontrada."
    )
    plt.figtext(0.5, -0.1, explanation, wrap=True, horizontalalignment='center', fontsize=12)
    plt.title(title)
    plt.show()

# Main
if __name__ == "__main__":
    graph = create_graph(cities, distances)
    initial_route = list(cities.keys())
    
    # Encontrar la mejor ruta usando búsqueda local
    best_route, best_distance = two_opt(graph, initial_route)
    
    # Mostrar resultados
    print("Mejor ruta encontrada:", best_route)
    print("Distancia de la mejor ruta:", best_distance, "km")
    
    # Graficar el resultado
    plot_graph_with_route(graph, best_route, cities, "Ruta Óptima Encontrada con Búsqueda Local")
