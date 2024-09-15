#Nombre: Aldo Emiliano Chavez Lares
#Registro: 21310238
#Grupo: 7F1

import heapq
import matplotlib.pyplot as plt
import networkx as nx

# Definir el grafo con nodos y aristas (ubicaciones y distancias realistas)
graph = {
    'Proveedor de Materia Prima': [('Recepción', 12)],
    'Recepción': [('Proveedor de Materia Prima', 12), ('Procesado', 9), ('Almacenamiento Intermedio', 10)],
    'Procesado': [('Recepción', 9), ('Almacenamiento Intermedio', 5), ('Ensamblaje', 8)],
    'Almacenamiento Intermedio': [('Recepción', 10), ('Procesado', 5), ('Ensamblaje', 7), ('Control de Calidad', 6)],
    'Ensamblaje': [('Procesado', 8), ('Almacenamiento Intermedio', 7), ('Control de Calidad', 4)],
    'Control de Calidad': [('Almacenamiento Intermedio', 6), ('Ensamblaje', 4), ('Distribución', 9)],
    'Distribución': [('Control de Calidad', 9), ('Almacén de Productos Terminados', 5)],
    'Almacén de Productos Terminados': [('Distribución', 5)]
}

# Implementación del algoritmo de Prim
def prim(graph):
    start_node = list(graph.keys())[0]  # Iniciar desde el primer nodo en el grafo
    visited = set([start_node])  # Conjunto de nodos visitados
    edges = [(weight, start_node, to) for to, weight in graph[start_node]]  # Aristas conectadas al nodo inicial
    heapq.heapify(edges)  # Convertir las aristas en una cola de prioridad (heap)
    mst = []  # Lista donde se almacenará el MST
    total_cost = 0  # Variable para calcular el costo total del MST
    
    # Mientras haya aristas, seguimos construyendo el MST
    while edges:
        weight, frm, to = heapq.heappop(edges)  # Extraemos la arista con menor peso
        if to not in visited:  # Si el nodo de destino aún no fue visitado
            visited.add(to)  # Lo marcamos como visitado
            mst.append((frm, to, weight))  # Añadimos la arista al MST
            total_cost += weight  # Acumulamos el costo
            
            # Añadimos nuevas aristas que conectan el nuevo nodo a los nodos no visitados
            for to_next, weight_next in graph[to]:
                if to_next not in visited:
                    heapq.heappush(edges, (weight_next, to, to_next))
    
    return mst, total_cost

# Aplicar el algoritmo de Prim
mst, total_cost = prim(graph)

# Mostrar el MST
print("Árbol de Expansión Mínimo:", mst)
print(f"Costo total del Árbol de Expansión Mínimo: ${total_cost}")

# Posiciones fijas de los nodos para visualización
pos = {
    'Proveedor de Materia Prima': (0, 0), 
    'Recepción': (1, 2), 
    'Procesado': (2, 1), 
    'Almacenamiento Intermedio': (3, 3), 
    'Ensamblaje': (4, 1), 
    'Control de Calidad': (5, 2), 
    'Distribución': (6, 3), 
    'Almacén de Productos Terminados': (7, 1)
}

# Crear el grafo usando NetworkX
G = nx.Graph()
for frm in graph:
    for to, weight in graph[frm]:
        G.add_edge(frm, to, weight=weight)  # Añadimos las aristas al grafo

# Crear una visualización interactiva
def display_mst(mst, total_cost):
    # Crear figuras y ejes para subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Dibujar el grafo original con todas las aristas y sus pesos
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightgreen", font_size=10, font_weight='bold', ax=ax1)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10, font_weight='bold', ax=ax1)

    # Dibujar el MST resultante, resaltando las aristas en rojo
    mst_edges = [(frm, to) for frm, to, weight in mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=2, edge_color='r', ax=ax1)

    # Mostrar la explicación en el segundo subplot
    explanation_text = (
        f"Este gráfico muestra la disposición óptima de las áreas de trabajo en una cadena de suministro industrial, "
        f"minimizando la longitud total de las conexiones necesarias.\n\n"
        f"Nodos:\n"
        f" - Proveedor de Materia Prima\n"
        f" - Recepción\n"
        f" - Procesado\n"
        f" - Almacenamiento Intermedio\n"
        f" - Ensamblaje\n"
        f" - Control de Calidad\n"
        f" - Distribución\n"
        f" - Almacén de Productos Terminados\n\n"
        f"Aristas y Pesos: Las conexiones entre las áreas y sus distancias respectivas.\n\n"
        f"Aristas en Rojo: Conexiones seleccionadas para formar el Árbol de Expansión Mínimo (MST), "
        f"indicando la ruta más eficiente para conectar todas las áreas minimizando la longitud total.\n\n"
        f"El Árbol de Expansión Mínimo conecta todas las áreas con el costo total más bajo posible, "
        f"que en este caso es de ${total_cost}.\n\n"
        f"Interpretación paso a paso:\n"
        f"1. Inicia desde 'Proveedor de Materia Prima' y selecciona la conexión más barata.\n"
        f"2. Conecta con 'Recepción' (costo: 12).\n"
        f"3. Luego, sigue conectando áreas para minimizar costos: 'Procesado', 'Almacenamiento Intermedio', 'Ensamblaje', etc.\n"
        f"Cada conexión minimiza el costo total del sistema, generando una red eficiente."
    )

    ax2.text(0, 1, explanation_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.8), ha='left', va='top', wrap=True)
    ax2.axis('off')  # Deshabilitar los ejes

    # Mostrar los subplots
    plt.show()

# Mostrar el MST de manera interactiva con una explicación más detallada
display_mst(mst, total_cost)
