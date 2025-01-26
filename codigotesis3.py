import numpy as np
from scipy.integrate import dblquad, IntegrationWarning
import warnings

# Definir la función que será integrada
def integrand(z, w, x0, y0, epsilon=1e-10):
    numerator = 2 - 2 * np.cos(z * x0 + w * y0)
    denominator = np.sin(z / 2)**2 + np.sin(w / 2)**2
    denominator = np.maximum(denominator, epsilon)  # Evitar división por valores muy pequeños
    return numerator / denominator

# Función para integrar en un subintervalo específico
def integrate_subinterval(z_start, z_end, w_start, w_end, x0, y0, epsilon):
    try:
        result, error = dblquad(
            integrand, 
            w_start, w_end,  # Límites para w
            lambda _: z_start, lambda _: z_end,  # Límites para z
            args=(x0, y0, epsilon)
        )
        return result
    except IntegrationWarning:
        return None  # Si falla, devolvemos None para intentar otra estrategia

# Función principal para dividir en subintervalos e integrar en cada uno
def calculate_integral(x0, y0, max_intervals=10, epsilon=1e-10):
    for num_intervals in range(4, max_intervals + 1, 2):  # Aumentamos adaptativamente
        z_intervals = np.linspace(0, 2 * np.pi, num_intervals + 1)
        w_intervals = np.linspace(0, 2 * np.pi, num_intervals + 1)

        total_result = 0
        failed = False  # Para saber si hay problemas en algún subintervalo

        for i in range(num_intervals):
            for j in range(num_intervals):
                # Definir los límites para el subintervalo actual
                z_start, z_end = z_intervals[i], z_intervals[i + 1]
                w_start, w_end = w_intervals[j], w_intervals[j + 1]

                # Integrar en el subintervalo
                sub_result = integrate_subinterval(z_start, z_end, w_start, w_end, x0, y0, epsilon)

                if sub_result is None:  # Si hubo un problema, intentamos con más subdivisiones
                    failed = True
                    break  # Salimos del bucle y probamos con más intervalos

                total_result += sub_result
        
        if not failed:  # Si todo fue bien, devolvemos el resultado
            return total_result / (4 * np.pi**2)

    # Si después de todos los intentos sigue fallando, devolvemos un mensaje de error
    return "No se pudo calcular la integral con suficiente precisión."

# Parámetros que el usuario puede modificar
x0 = 1024  # Cambia x0 por el valor deseado
y0 = 0  # Cambia y0 por el valor deseado

# Ignorar warnings de integración para manejar errores manualmente
warnings.simplefilter("ignore", IntegrationWarning)

# Calcular el valor de la integral
integral_value = calculate_integral(x0, y0, max_intervals=20)
print(f"El valor de la integral para x0={x0} y y0={y0} es: {integral_value}")
