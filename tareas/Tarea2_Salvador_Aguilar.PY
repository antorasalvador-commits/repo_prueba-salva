
from collections import deque


# ----------------------------------------------------------------------
# Datos iniciales
# ----------------------------------------------------------------------
def cargar_red():
    return {
        "Santiago": ["Mercedes Sur", "Barbacoas", "Candelarita"],
        "Mercedes Sur": ["Santiago", "San Rafael"],
        "Barbacoas": ["Santiago", "Grifo Alto"],
        "San Rafael": ["Mercedes Sur", "Grifo Alto"],
        "Grifo Alto": ["Barbacoas", "San Rafael"],
        "Candelarita": ["Santiago"],
        "Desamparaditos": ["Chires"],
        "Chires": ["Desamparaditos"],
        "Zapatón": [],
    }


def cargar_obras():
    return {
        "Estudio": ["Permisos", "Materiales"],
        "Permisos": ["Excavación"],
        "Materiales": ["Alcantarillado", "Asfaltado"],
        "Excavación": ["Alcantarillado"],
        "Alcantarillado": ["Asfaltado"],
        "Asfaltado": ["Señalización"],
        "Señalización": [],
    }


# GRAFOS: DFS, BFS, componentes conexas, ciclos y orden topológico
def dfs_iterativo(grafo, inicio):

    visitados = []
    marcados = set()
    pila = [inicio]
    while pila:
        actual = pila.pop()
        if actual in marcados:
            continue
        marcados.add(actual)
        visitados.append(actual)
        for vecino in reversed(grafo[actual]):
            if vecino not in marcados:
                pila.append(vecino)
    return visitados


def ruta_mas_corta(grafo, inicio, destino):

    padres = {inicio: None}
    cola = deque([inicio])
    while cola:
        actual = cola.popleft()
        if actual == destino:
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padres[actual]
            ruta.reverse()
            return ruta
        for vecino in grafo[actual]:
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
    return None


def contar_componentes(grafo):
    """Retorna (cantidad de componentes, {comunidad: número de componente}).

    Cada componente se recorre con una pila propia.
    """
    componente_de = {}
    cantidad = 0
    for nodo in grafo:
        if nodo in componente_de:
            continue
        cantidad += 1
        pila = [nodo]
        while pila:
            actual = pila.pop()
            if actual in componente_de:
                continue
            componente_de[actual] = cantidad
            for vecino in grafo[actual]:
                if vecino not in componente_de:
                    pila.append(vecino)
    return cantidad, componente_de


def tiene_ciclo(grafo):
    """DFS recursivo que ignora al padre. Retorna True o False."""
    visitados = set()

    def visitar(nodo, padre):
        visitados.add(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                if visitar(vecino, nodo):
                    return True
            elif vecino != padre:
                return True
        return False

    for nodo in grafo:
        if nodo not in visitados:
            if visitar(nodo, None):
                return True
    return False


def orden_topologico(grafo):
    """Algoritmo de Kahn con grado de entrada y deque.

    Retorna la lista de obras en el orden calculado. Si el resultado no
    incluye todas las obras, existe un ciclo de prerrequisitos.
    """
    grado_entrada = {obra: 0 for obra in grafo}
    for obra in grafo:
        for dependiente in grafo[obra]:
            grado_entrada[dependiente] += 1

    cola = deque(obra for obra in grafo if grado_entrada[obra] == 0)
    orden = []
    while cola:
        actual = cola.popleft()
        orden.append(actual)
        for dependiente in grafo[actual]:
            grado_entrada[dependiente] -= 1
            if grado_entrada[dependiente] == 0:
                cola.append(dependiente)
    return orden


# ----------------------------------------------------------------------
# Programa principal (toda la entrada y salida)
# ----------------------------------------------------------------------
def normalizar(texto):
    return texto.strip().title()


def mostrar_menu():
    print("=== RED VIAL DE PURISCAL ===")
    print("1. Ver la red de caminos")
    print("2. Agregar un camino")
    print("3. Comunidades alcanzables desde una comunidad")
    print("4. Ruta con menos tramos entre dos comunidades")
    print("5. Componentes conexas de la red")
    print("6. Detectar caminos circulares")
    print("7. Orden de ejecución de las obras")
    print("8. Agregar un prerrequisito entre obras")
    print("9. Salir")


def opcion_ver_red(red):
    print("\nRed de caminos de Puriscal")
    total_grados = 0
    for comunidad, vecinos in red.items():
        grado = len(vecinos)
        total_grados += grado
        lista = ", ".join(vecinos) if vecinos else "sin caminos"
        print(f"{comunidad} (grado {grado}): {lista}")
    print(f"Total de caminos: {total_grados // 2}")


def opcion_agregar_camino(red):
    a = normalizar(input("Primera comunidad: "))
    b = normalizar(input("Segunda comunidad: "))
    print()
    if a not in red:
        print(f"No existe la comunidad '{a}'.")
    elif b not in red:
        print(f"No existe la comunidad '{b}'.")
    elif a == b:
        print("Una comunidad no puede conectarse consigo misma.")
    elif b in red[a]:
        print(f"Ya existe un camino entre {a} y {b}.")
    else:
        red[a].append(b)
        red[b].append(a)
        print(f"Camino agregado entre {a} y {b}.")


def opcion_alcanzables(red):
    inicio = normalizar(input("Comunidad de inicio: "))
    print()
    if inicio not in red:
        print(f"No existe la comunidad '{inicio}'.")
        return
    visitados = dfs_iterativo(red, inicio)
    print(f"Comunidades alcanzables desde {inicio}: {len(visitados)}")
    print(" -> ".join(visitados))


def opcion_ruta(red):
    origen = normalizar(input("Comunidad de origen: "))
    destino = normalizar(input("Comunidad de destino: "))
    print()
    if origen not in red:
        print(f"No existe la comunidad '{origen}'.")
    elif destino not in red:
        print(f"No existe la comunidad '{destino}'.")
    elif origen == destino:
        print("El origen y el destino son la misma comunidad.")
    else:
        ruta = ruta_mas_corta(red, origen, destino)
        if ruta is None:
            print(f"No existe una ruta entre {origen} y {destino}.")
        else:
            print("Ruta con menos tramos: " + " -> ".join(ruta))
            print(f"Cantidad de tramos: {len(ruta) - 1}")


def opcion_componentes(red):
    cantidad, componente_de = contar_componentes(red)
    print()
    for numero in range(1, cantidad + 1):
        miembros = [c for c in red if componente_de[c] == numero]
        print(f"Componente {numero}: {', '.join(miembros)}")
    if cantidad == 1:
        print("La red tiene 1 componente conexa y todas las comunidades "
              "están comunicadas.")
    else:
        print(f"La red tiene {cantidad} componentes conexas y no todas las "
              "comunidades están comunicadas.")


def opcion_ciclos(red):
    print()
    hay_ciclo_dfs = tiene_ciclo(red)
    if hay_ciclo_dfs:
        print("Búsqueda con DFS: la red tiene al menos un camino circular.")
    else:
        print("Búsqueda con DFS: la red no tiene caminos circulares.")

    comunidades = len(red)
    caminos = sum(len(v) for v in red.values()) // 2
    cantidad, _ = contar_componentes(red)
    permitidos = comunidades - cantidad
    hay_ciclo_conteo = caminos > permitidos
    print(f"Comprobación por conteo: {caminos} caminos frente a "
          f"{permitidos} permitidos sin ciclos "
          f"({comunidades} comunidades - {cantidad} componentes).")
    if hay_ciclo_dfs == hay_ciclo_conteo:
        print("Los dos métodos coinciden.")
    else:
        print("Los dos métodos no coinciden.")


def opcion_orden_obras(obras):
    print()
    orden = orden_topologico(obras)
    if len(orden) == len(obras):
        print("Orden de ejecución de las obras:")
        print(" -> ".join(orden))
    else:
        bloqueadas = [o for o in obras if o not in orden]
        print("Hay un ciclo de prerrequisitos: no existe un orden válido.")
        print("Obras bloqueadas: " + ", ".join(bloqueadas))


def opcion_agregar_prerrequisito(obras):
    previa = normalizar(input("Obra previa: "))
    dependiente = normalizar(input("Obra que depende de ella: "))
    print()
    if previa not in obras:
        print(f"No existe la obra '{previa}'.")
    elif dependiente not in obras:
        print(f"No existe la obra '{dependiente}'.")
    elif previa == dependiente:
        print("Una obra no puede depender de sí misma.")
    elif dependiente in obras[previa]:
        print(f"Ya existe el prerrequisito: {previa} debe terminar antes "
              f"de {dependiente}.")
    else:
        obras[previa].append(dependiente)
        print(f"Prerrequisito agregado: {previa} debe terminar antes de "
              f"{dependiente}.")


def main():
    red = cargar_red()
    obras = cargar_obras()

    while True:
        mostrar_menu()
        entrada = input("Elija una opción: ")
        try:
            opcion = int(entrada.strip())
        except ValueError:
            opcion = 0

        if opcion == 1:
            opcion_ver_red(red)
        elif opcion == 2:
            opcion_agregar_camino(red)
        elif opcion == 3:
            opcion_alcanzables(red)
        elif opcion == 4:
            opcion_ruta(red)
        elif opcion == 5:
            opcion_componentes(red)
        elif opcion == 6:
            opcion_ciclos(red)
        elif opcion == 7:
            opcion_orden_obras(obras)
        elif opcion == 8:
            opcion_agregar_prerrequisito(obras)
        elif opcion == 9:
            print("\n¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida. Debe digitar un número del 1 al 9.")
        print()


if __name__ == "__main__":
    main()