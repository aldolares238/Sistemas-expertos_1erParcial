#Nombre: Aldo Emiliano Chavez Lares
#Registro: 21310238
#Grupo: 7F1

import heapq
import matplotlib.pyplot as plt
import networkx as nx

# Definimos el grafo con los tiempos de desplazamiento en minutos entre centros de telecomunicaciones y el lugar de emergencia
grafo = {
    'Centro de Telecomunicaciones A': {'Centro de Control': 12, 'Estación de Repetidores': 25},
    'Centro de Telecomunicaciones B': {'Centro de Control': 18, 'Estación de Repetidores': 20},
    'Centro de Telecomunicaciones C': {'Centro de Control': 25, 'Estación de Repetidores': 15},
    'Centro de Control': {'Estación de Repetidores': 10},
    'Estación de Repetidores': {}  # Nodo de destino sin vecinos
}

def dijkstra(grafo, inicio, fin):
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[inicio] = 0
    padres = {nodo: None for nodo in grafo}
    
    cola_prioridad = [(0, inicio)]
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual == fin:
            break
        
        if distancia_actual > distancias[nodo_actual]:
            continue
        
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
            
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                padres[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia, vecino))
    
    camino = []
    nodo = fin
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()
    
    return distancias[fin], camino

def mostrar_grafo(grafo, ruta, peso_total, emergencia):
    G = nx.Graph()
    
    for nodo in grafo:
        for vecino, peso in grafo[nodo].items():
            G.add_edge(nodo, vecino, weight=peso)
    
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(12, 10))
    
    # Dibujar el grafo
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_size=12)
    
    # Resaltar la ruta más corta
    if ruta:
        path_edges = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=ruta, node_color='r', node_size=700)
    
    ruta_texto = " -> ".join(ruta)
    plt.title(f"Ruta más corta para la emergencia '{emergencia}': {ruta_texto}\nPeso total: {peso_total} minutos", fontsize=15)
    
    # Añadir el peso total y la emergencia en el gráfico
    plt.text(0.5, 0.03, f'Peso total de la ruta: {peso_total} minutos', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    plt.text(0.5, 0.08, f'La mejor cuadrilla para atender la emergencia es {mejor_cuadrilla[1]}', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.6))
    plt.text(0.5, 0.13, f'Descripción de la emergencia: {emergencia}', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='lightyellow', alpha=0.6))

    # Explicación general del proceso en un cuadro en la esquina superior derecha
    plt.text(.42, 1, 'Explicación:\n\n'
                        'Este gráfico muestra cómo se determina la mejor cuadrilla para atender una emergencia.\n'
                        'Utilizamos el algoritmo de Dijkstra para encontrar la ruta más corta en términos de tiempo de desplazamiento\n'
                        'desde varios centros de telecomunicaciones hasta el lugar de emergencia.\n\n'
                        'Los centros de telecomunicaciones se muestran como nodos en el gráfico y las conexiones entre ellos tienen\n'
                        'un peso que representa el tiempo en minutos necesario para desplazarse entre ellos. La ruta más corta en rojo indica\n'
                        'el camino más eficiente para la cuadrilla más cercana al lugar de emergencia.',
             horizontalalignment='left', verticalalignment='top', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='lightgrey', alpha=0.9))
    
    # Ajuste de márgenes para el texto en la esquina superior derecha
    plt.subplots_adjust(right=0.75)
    
    plt.show()

# Definimos los nodos de inicio y fin
inicio1 = 'Centro de Telecomunicaciones A'
inicio2 = 'Centro de Telecomunicaciones B'
inicio3 = 'Centro de Telecomunicaciones C'
fin = 'Centro de Control'

# Definimos la emergencia
emergencia = "Falla en el sistema de comunicaciones"

# Ejecución del algoritmo desde cada centro de telecomunicaciones hasta el centro de control
peso_total1, ruta1 = dijkstra(grafo, inicio1, fin)
peso_total2, ruta2 = dijkstra(grafo, inicio2, fin)
peso_total3, ruta3 = dijkstra(grafo, inicio3, fin)

# Determinar el centro de telecomunicaciones más rápido
mejor_cuadrilla = min([(peso_total1, 'Centro de Telecomunicaciones A', ruta1), 
                       (peso_total2, 'Centro de Telecomunicaciones B', ruta2), 
                       (peso_total3, 'Centro de Telecomunicaciones C', ruta3)])
print(f"La mejor cuadrilla es {mejor_cuadrilla[1]} con un tiempo de {mejor_cuadrilla[0]} minutos")

# Visualización del grafo y la ruta más corta para la mejor cuadrilla
mostrar_grafo(grafo, mejor_cuadrilla[2], mejor_cuadrilla[0], emergencia)
