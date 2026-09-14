
"""
Taller 1 - Reto de Programación
Cálculo paralelo de números de Fibonacci con concurrent.futures
 
Curso: Infraestructuras Paralelas y Distribuidas - 750023C
Samuel Banguero Ortega - 2418671
"""

import time
import concurrent.futures

N = 6600 # Número de Fibonacci a calcular

def fibonacci(n):
    """
    Calcula el n-ésimo número de Fibonacci.
    """
    
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def calcular_fibonacci_secuencial(n_elementos):
    """
    Calcula los números de Fibonacci de forma secuencial.
    Se utiliza como referencia para comparar el rendimiento.
    """

    inicio = time.time()

    resultados = [] * n_elementos

    for i in range(n_elementos):
        resultados.append(fibonacci(i))

    fin = time.time()
    tiempo = fin - inicio

    print(f"Fibonacci secuencial ({n_elementos}): {resultados}")
    return tiempo

def calcular_fibonacci_paralelo(n_elementos, executor_type):
    """
    Calcula los números de Fibonacci utilizando
    un Executor de concurrent.futures
    """

    inicio = time.time()

    """
    creación de tareas (paralelizable)
    Cada executor.submit(fibonacci, i) es independiente de las demás:
    Por eso se puede repartir entre varios hilos/procesos sin riesgo.
    """

    resultados = [0] * n_elementos
    with executor_type() as executor:
        futures = [
            executor.submit(fibonacci, i) 
            for i in range(n_elementos)
        ]

        """
        Recolección de resultados
        Este ciclo se mantiene serial porque se encarga de recuperar
        los resultados de los Future y almacenarlos en el orden original.
        Los cálculos de Fibonacci ya fueron ejecutados en paralelo
        por los procesos.
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
    print(f"Fibonacci paralelo ({n_elementos}): {resultados}")
    return tiempo_ejecucion

def tiempos(t_paralelo, t_secuencial):
    print(f"Tiempo de ejecución paralelo: {t_paralelo:.4f} segundos")
    print(f"Tiempo de ejecución secuencial: {t_secuencial:.4f} segundos")
    print(f"Tiempo total: {t_paralelo+t_secuencial:.4f} segundos")


if __name__ == "__main__":
    
    tiempos(
        calcular_fibonacci_paralelo(N,concurrent.futures.ProcessPoolExecutor),
        calcular_fibonacci_secuencial(N)
        )