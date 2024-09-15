#Nombre: Aldo Emiliano Chavez Lares
#Registro: 21310238
#Grupo: 7F1

import matplotlib.pyplot as plt  # Para la visualización del grafo
import networkx as nx  # Para la creación y manipulación de grafos
import random  # Para generar costos aleatorios

# Implementación del algoritmo de Kruskal mediante la estructura Union-Find
class UnionFind:
    def __init__(self, n):
        # Inicializamos un array "parent" para representar los padres de cada nodo
        # y un array "rank" para gestionar las uniones según la profundidad
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        # Función para encontrar el "padre" de un nodo con compresión de caminos
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        # Unir dos subconjuntos (componentes) usando la técnica Union by Rank
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            # Si uno de los conjuntos tiene mayor rango, se convierte en el padre del otro
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                # Si los rangos son iguales, uno se convierte en el padre del otro
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

# Función para generar una lista de componentes y las posibles conexiones entre ellos
def generate_realistic_graph(components):
    edges = []  # Lista donde se almacenarán las conexiones (aristas)
    num_components = len(components)  # Número de componentes seleccionados
    for i in range(num_components):
        for j in range(i + 1, num_components):
            # Se genera un costo aleatorio entre 10 y 100 para conectar dos componentes
            cost = random.randint(10, 100)
            edges.append((i, j, cost))  # Se añade la arista con el costo entre dos nodos
    return components, edges

# Función que visualiza la red de componentes y aplica el algoritmo de Kruskal
def visualize_factory_network(components):
    num_components = len(components)  # Número total de componentes
    components, edges = generate_realistic_graph(components)  # Genera el grafo de la red
    uf = UnionFind(num_components)  # Inicializa la estructura Union-Find para Kruskal
    mst = []  # Lista donde se almacenarán las conexiones del árbol de expansión mínima (MST)
    total_cost = 0  # Almacena el costo total de la red

    # Ordenamos las conexiones por costo (de menor a mayor)
    edges.sort(key=lambda x: x[2])

    # Crear un grafo vacío utilizando NetworkX
    G = nx.Graph()
    G.add_nodes_from(range(num_components))  # Añadir los nodos al grafo

    # Posición de los nodos en el gráfico (layout)
    pos = nx.spring_layout(G)

    # Activar el modo interactivo para actualizar el gráfico en la misma ventana
    plt.ion()
    fig, ax = plt.subplots()

    # Dibujar el grafo inicial con los nodos y sin conexiones
    nx.draw(G, pos, with_labels=True, labels={i: components[i] for i in range(num_components)},
            node_color='lightblue', font_weight='bold', node_size=1000, ax=ax)

    # Establecer el título del grafo inicial
    ax.set_title("Conexiones en la Fábrica: Red Inicial")
    plt.draw()
    plt.pause(2)  # Pausa para que el usuario vea el grafo sin conexiones

    # Aplicar el algoritmo de Kruskal para encontrar el MST
    for u, v, cost in edges:
        # Si los nodos no están en el mismo subconjunto, los unimos
        if uf.find(u) != uf.find(v):
            uf.union(u, v)  # Unir los dos nodos
            mst.append((u, v, cost))  # Añadir la conexión al MST
            total_cost += cost  # Sumar el costo de la conexión al total

            # Añadir la conexión al grafo visual
            G.add_edge(u, v, weight=cost)
            ax.clear()  # Limpiar el gráfico antes de actualizarlo

            # Redibujar el grafo con la nueva conexión añadida
            nx.draw(G, pos, with_labels=True, labels={i: components[i] for i in range(num_components)},
                    node_color='lightblue', font_weight='bold', node_size=1000, ax=ax)

            # Mostrar el costo de cada conexión sobre la línea que la representa
            edge_labels = {(u, v): f"${cost}" for u, v, cost in mst}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)

            # Actualizar el título con la última conexión añadida
            ax.set_title(f"Conexión añadida: {components[u]} - {components[v]} (Costo: ${cost})")
            plt.draw()
            plt.pause(2)  # Pausa para que el usuario observe la nueva conexión

            # Si ya hemos añadido suficientes conexiones para conectar todos los nodos, terminamos
            if len(mst) == num_components - 1:
                break

    # Establecer el título final y mostrar el costo total de la red
    ax.set_title(f"Red final de costo mínimo (Total: ${total_cost})")
    ax.text(0.5, 0.02, f"Costo total de la conexión: ${total_cost}", horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize=10)
    plt.draw()

    # Desactivar el modo interactivo y mostrar el gráfico final
    plt.ioff()
    plt.show()

# Bloque principal donde el usuario selecciona los componentes y se genera el grafo
if __name__ == "__main__":
    print("Seleccione los componentes de la fábrica que desea conectar:")
    
    # Lista de componentes disponibles para la selección del usuario
    available_components = ["Sensor de Temperatura", "Motor Principal", "Cámara de Vigilancia", 
                             "Controlador de Flujo", "Robot de Ensamblaje", "Sensor de Movimiento", 
                             "Actuador Hidráulico", "Válvula de Control", "Sistema de Alarmas"]
    
    # Mostrar los componentes disponibles para que el usuario pueda seleccionarlos
    print("Componentes disponibles:")
    for i, comp in enumerate(available_components):
        print(f"{i+1}. {comp}")

    # Solicitar al usuario que seleccione los componentes
    while True:
        try:
            # Entrada del usuario: números de componentes separados por comas
            component_indices = input("Ingrese los números de los componentes separados por comas (ej: 1,3,5): ")
            indices = list(map(int, component_indices.split(',')))  # Convertir la entrada en una lista de números
            selected_components = [available_components[i-1] for i in indices if 0 < i <= len(available_components)]
            # Verificar que al menos se seleccionen 2 componentes
            if len(selected_components) < 2:
                print("Seleccione al menos 2 componentes.")
            else:
                break
        except ValueError:
            print("Entrada no válida. Intente nuevamente.")

    # Visualizar la red de componentes seleccionados y aplicar Kruskal
    visualize_factory_network(selected_components)
