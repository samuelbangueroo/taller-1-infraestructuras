
"""
Taller 1 - Reto de Programación
Cálculo paralelo de números de Fibonacci con concurrent.futures
 
Curso: Infraestructuras Paralelas y Distribuidas - 750023C
Samuel Banguero Ortega
"""

import time
import concurrent.futures

N = 20  # Número de Fibonacci a calcular

def fibonacci(n):
    """
    Calcula el n-ésimo número de Fibonacci de forma recursiva y secuencial.
    """
    
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def calcular_fibonacci_paralelo(n_elementos, executor_type):
    inicio = time.time()

    """
    creación de tareas (PARALELIZABLE)
    Cada executor.submit(fibonacci, i) es independiente de las demás:
    Por eso se puede repartir entre varios hilos sin riesgo.
    """

    resultados = [0] * n_elementos
    with executor_type() as executor:
        futures = [
            executor.submit(fibonacci, i) 
            for i in range(n_elementos)
        ]

        """
        Trampa serial
        si se paralelizara esta instruccion el orden de fibonacci no seria el correcto 
        """
        for i, future in enumerate(futures):
            resultados[i] = future.result()

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    """
    Impresion
    Siempre serial, se hace una sola despues de que todos los futures hayan terminado
    evitando conflictos de acceso 
    """
    print(f"Fibonacci ({n_elementos}): {resultados}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")


if __name__ == "__main__":
    calcular_fibonacci_paralelo(
        N,
        concurrent.futures.ThreadPoolExecutor
    )