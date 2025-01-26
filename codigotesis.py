import numpy as np
import matplotlib.pyplot as plt
import random

# Inicializamos la función para ejecutar el experimento
def ejecutar_experimento(T, iteraciones):
    # Inicializamos una rejilla en el toro (T x T) con masa en el origen
    masa = np.zeros((T, T))
    masa[0, 0] = 1

    # Definimos una función para aplicar condiciones de frontera periódicas
    def frontera_periodica(i, j, T):
        return (i % T, j % T)

    # Definir los vecinos de una casilla en una rejilla
    def vecinos(i, j, T):
        return [
            frontera_periodica(i+1, j, T),
            frontera_periodica(i-1, j, T),
            frontera_periodica(i, j+1, T),
            frontera_periodica(i, j-1, T)
        ]

    # Evolución discreta de la masa en (\mathbb{Z}/T\mathbb{Z})^2
    def evolucionar_masa(masa, pasos, T):
        # Inicializamos el conjunto de casillas con masa
        casillas_con_masa = {(0, 0)}

        for paso in range(pasos):
            if not casillas_con_masa:
                print("No queda más masa para distribuir.")
                break

            # Elegimos una casilla al azar entre las que tienen masa
            casilla_aleatoria = random.choice(list(casillas_con_masa))
            i, j = casilla_aleatoria

            # Guardamos la masa actual de la casilla
            masa_actual = masa[i, j]

            # Redistribuimos la masa de esta casilla a sus vecinos
            masa_por_vecino = masa_actual / 4  # Distribuir la masa entre los 4 vecinos
            for vecino in vecinos(i, j, T):
                x, y = vecino
                # La masa puede moverse a cualquier vecino, incluso (0, y) con y != 0, pero estas no redistribuyen más
                masa[x, y] += masa_por_vecino
                # Agregamos los vecinos al conjunto si no son de la forma (0, y) con y != 0
                if not (x == 0 and y != 0):
                    casillas_con_masa.add((x, y))

            # Eliminamos la casilla actual del conjunto y ponemos su masa en 0
            masa[i, j] = 0
            casillas_con_masa.remove((i, j))

        return masa

    # Evolucionamos la masa durante el número de iteraciones especificado
    masa_final = evolucionar_masa(masa, iteraciones, T)

    # Determinamos el límite de las distancias según si T es par o impar
    if T % 2 == 0:
        limite_distancia = T // 2
    else:
        limite_distancia = T // 2  # Parte entera baja

    # Graficar la cantidad de masa en función de la distancia desde el origen
    distancias = []
    cantidades_de_masa = []

    for y in range(1, limite_distancia + 1):
        distancias.append(y)  # La distancia es simplemente el valor absoluto de y
        cantidades_de_masa.append(masa_final[0, y])  # Masa en la casilla (0, y)

    # Primera gráfica: Masa vs distancia
    plt.figure(figsize=(18, 9))  # Aumentar tamaño de la figura a 12x6 pulgadas
    plt.plot(distancias, cantidades_de_masa, marker='o', linestyle='-', color='b')
    plt.xlabel('Distancia al origen')
    plt.ylabel('Cantidad de masa')
    plt.title('Cantidad de masa en función de la distancia desde el origen')
    plt.grid(True)
    plt.show()

    # Segunda gráfica: Log-log plot de la cantidad de masa vs distancia
    log_distancias = np.log(distancias)
    log_masa = np.log(cantidades_de_masa)

    # Tercera gráfica: Pendientes (log(masa)/log(distancia)) vs distancia
    pendientes = log_masa / log_distancias

    plt.figure(figsize=(18, 9))  # Aumentar tamaño de la figura a 12x6 pulgadas
    plt.plot(distancias, pendientes, marker='o', linestyle='-', color='g')
    plt.xlabel('Distancia')
    plt.ylabel('Pendientes (log(masa) / log(distancia))')
    plt.title('Pendientes vs Distancia')
    plt.grid(True)
    plt.show()

# Solicitar valores de T y número de iteraciones al usuario
T = int(input("Introduce el valor de T (tamaño del toro): "))
iteraciones = int(input("Introduce el número de iteraciones: "))

# Ejecutar el experimento
ejecutar_experimento(T, iteraciones)
