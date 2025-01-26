import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import dblquad
import warnings

# Definir la función integranda
def integrand(z, w, x0, epsilon=1e-10):
    numerator = 2 - 2 * np.cos(z * x0)
    denominator = np.sin(z / 2)**2 + np.sin(w / 2)**2
    denominator = np.maximum(denominator, epsilon)  # Evitar divisiones problemáticas
    return numerator / denominator

# Integración con subdivisión adaptativa
def calculate_integral(x0, max_intervals=10, epsilon=1e-10):
    for num_intervals in range(4, max_intervals + 1, 2):
        z_intervals = np.linspace(0, 2 * np.pi, num_intervals + 1)
        w_intervals = np.linspace(0, 2 * np.pi, num_intervals + 1)

        total_result = 0
        failed = False

        for i in range(num_intervals):
            for j in range(num_intervals):
                z_start, z_end = z_intervals[i], z_intervals[i + 1]
                w_start, w_end = w_intervals[j], w_intervals[j + 1]

                try:
                    sub_result, error = dblquad(
                        integrand,
                        w_start, w_end,
                        lambda _: z_start, lambda _: z_end,
                        args=(x0, epsilon)
                    )
                    total_result += sub_result
                except:
                    failed = True
                    break

            if failed:
                break

        if not failed:
            return total_result / (4 * np.pi**2)

    return None  # Si no se pudo calcular

# Ignorar warnings de integración
warnings.simplefilter("ignore")

# Valores de x0 desde 1 hasta 2^10
x_values = [2**i for i in range(11)]
integral_values = []

# Calcular la integral para cada x0
for x0 in x_values:
    result = calculate_integral(x0, max_intervals=20)
    integral_values.append(result if result is not None else np.nan)

# Graficar los resultados
plt.figure(figsize=(8, 5))
plt.plot(x_values, integral_values, marker='o', linestyle='-')
plt.xscale("log")  # Escala logarítmica en el eje x
plt.xlabel(r'$x_0$')
plt.ylabel(r'Valor de la integral')
plt.title(r'Integral en función de $x_0$ con $y_0 = 0$')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
