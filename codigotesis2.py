import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad

# Parámetros fijos de la función
x0, y0 = 1, 0  # Punto de referencia en el plano Z^2
pi = np.pi

# Definimos la función integranda
def integrand(w, z, x, y, x0, y0):
    numerator = (np.cos(z * (x - x0) + w * (y - y0)) 
                 - np.cos(z * x + w * y)
                 - np.cos(z * x0 + w * y0) + 1)
    denominator = (np.sin(z / 2)**2 + np.sin(w / 2)**2)
    return numerator / denominator if denominator != 0 else 0

# Definimos la función u(x, y) calculando la integral doble
def u(x, y):
    integral_value, _ = dblquad(
        integrand, 0, 2 * pi, lambda z: 0, lambda z: 2 * pi, 
        args=(x, y, x0, y0)
    )
    return integral_value / (4 * pi**2)

# Crear una cuadrícula de puntos enteros
X, Y = np.meshgrid(np.arange(-10, 11, 1), np.arange(-10, 11, 1))
U = np.vectorize(u)(X, Y)  # Evaluar u en cada punto de la cuadrícula

# Graficar en 3D con matplotlib
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, U, cmap='viridis')

# Agregar etiquetas y título
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('u(x, y)')
ax.set_title('Gráfico 3D de la función u(x, y)')

# Mostrar colorbar
fig.colorbar(ax.plot_surface(X, Y, U, cmap='viridis'))

# Mostrar el gráfico
plt.show()
