nodos = ["E", "C", "J", "R", "T", "S"]

nombres = {
    "E": "Entrada",
    "C": "Exposición de ciencias",
    "J": "Zona de juegos",
    "R": "Robótica",
    "T": "Talleres",
    "S": "Salida",
}

# Mapa
mapa = {
    "E": ["C", "J"],
    "C": ["E", "R", "T"],
    "J": ["E", "S"],
    "R": ["C", "S"],
    "T": ["C", "S"],
    "S": ["J", "R", "T"],
}


def construir_matriz(mapa, nodos):
    """Construye la matriz de adyacencia a partir de la lista de adyacencia."""
    n = len(nodos)
    matriz = [[0] * n for _ in range(n)]
    for i, origen in enumerate(nodos):
        for vecino in mapa[origen]:
            j = nodos.index(vecino)
            matriz[i][j] = 1
    return matriz


def dfs_recursivo(mapa, inicio):
    """DFS recursivo con conjunto visitados. Retorna el orden de visita."""
    visitados = set()
    orden = []

    def visitar(nodo):
        visitados.add(nodo)  # se marca antes de explorar vecinos
        orden.append(nodo)
        for vecino in mapa[nodo]:
            if vecino not in visitados:
                visitar(vecino)

    visitar(inicio)
    return orden


def dfs_iterativo(mapa, inicio):
    """DFS iterativo con pila explícita. Retorna el orden de visita."""
    visitados = set()
    orden = []
    pila = [inicio]
    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue  # se descarta sin volver a agregarlo al recorrido
        visitados.add(nodo)
        orden.append(nodo)
        for vecino in reversed(mapa[nodo]):
            if vecino not in visitados:
                pila.append(vecino)
    return orden


def pedir_nodo(mensaje):
    """Pide un nodo y lo valida sin importar mayúsculas/minúsculas. Retorna None si no existe."""
    nodo = input(mensaje).strip().upper()
    if nodo not in mapa:
        print("Ese espacio no existe en el mapa.")
        return None
    return nodo


def mostrar_menu():
    print("\n=== MAPA DE LA FERIA CIENTÍFICA ===")
    print("1. Ver conexiones de un espacio")
    print("2. Ver matriz de adyacencia")
    print("3. Recorrer con DFS recursivo")
    print("4. Recorrer con DFS iterativo")
    print("5. Consultar si hay un pasillo directo")
    print("6. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nodo = pedir_nodo("Espacio: ")
            if nodo:
                vecinos = ", ".join(mapa[nodo])
                print(f"{nodo} · {nombres[nodo]} se conecta con: {vecinos}")

        elif opcion == "2":
            matriz = construir_matriz(mapa, nodos)
            print("\n  " + " ".join(nodos))
            for nodo, fila in zip(nodos, matriz):
                print(nodo + " " + " ".join(str(x) for x in fila))

        elif opcion == "3":
            nodo = pedir_nodo("Espacio inicial: ")
            if nodo:
                print(" -> ".join(dfs_recursivo(mapa, nodo)))

        elif opcion == "4":
            nodo = pedir_nodo("Espacio inicial: ")
            if nodo:
                print(" -> ".join(dfs_iterativo(mapa, nodo)))

        elif opcion == "5":
            origen = pedir_nodo("Espacio de origen: ")
            if not origen:
                continue
            destino = pedir_nodo("Espacio de destino: ")
            if not destino:
                continue
            matriz = construir_matriz(mapa, nodos)
            if matriz[nodos.index(origen)][nodos.index(destino)] == 1:
                print(f"Sí existe un pasillo directo entre {origen} y {destino}.")
            else:
                print(f"No existe un pasillo directo entre {origen} y {destino}.")

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()