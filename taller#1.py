
"""
Taller 1 - Reto de Programación
Cálculo paralelo de números de Fibonacci con concurrent.futures
 
Curso: Infraestructuras Paralelas y Distribuidas - 750023C
Samuel Banguero Ortega - 2418671
Juan Diego Cárdenas Mejía - 2416437
"""

import time
import concurrent.futures

def fibonacci(n):
    """
    Calcula el n-ésimo número en la secuencia de Fibonacci.

    Este ciclo no es paralelizable: el cálculo al interior
    de cada iteración depende del resultad inmediatamente
    anterior (a, b se van actualizando en cadena), así que no hay
    forma de repartir sus pasos entre varios hilos/procesos.
    """
    
    a, b = 0, 1
    for _ in range(n):
        a = b
        b = a + b
    return a

def calcular_fibonacci_secuencial(n_elementos):
    """
    Calcula los números de Fibonacci de forma secuencial
    Se utiliza como referencia para comparar la ganancia en rendimiento
    """

    inicio = time.time()

    results = []

    for i in range(n_elementos):
        results.append(fibonacci(i))

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    return tiempo_ejecucion, results

def calcular_fibonacci_paralelo(n_elementos, executor_type, chunksize = 1, max_workers = None):
    """
    Calcula los números de Fibonacci utilizando
    un Executor de Procesos de concurrent.futures.
    """

    inicio = time.time()

    """
    Creación de tareas: paralelizable
    fibonacci(i) no depende de fibonacci(j), no leen
    ni escriben estado compartido entre sí. Por eso se puede repartir 
    sin riesgo entre varios workers.
    
    executor.map() además conserva el orden de entrada en la salida;
    resultados[i] siempre corresponde a fibonacci(i), sin importar en qué orden
    terminen los workers, así se evita un orden incorrecto.

    Trampas seriales evitadas:
    No se imprime dentro de los workers. La impresión se hace
    una sola vez al final, en el proceso principal, evitando
    salidas desordenadas y conflictos de acceso.
    """

    with executor_type(max_workers = max_workers) as executor:

        results = executor.map(fibonacci, range(n_elementos), chunksize = chunksize)


    fin = time.time()
    tiempo_ejecucion = fin - inicio

    return tiempo_ejecucion, list(results)



def print_results(t_paralelo, r_paralelo, t_secuencial, r_secuencial):
    """
    Impresión: serial, hecha una sola vez en el proceso principal,
    después de que todos los resultados ya llegaron evitando salidas corruptas.
    """
    print(f"Fibonacci secuencial ({N}): {r_secuencial}")
    print(f"Fibonacci paralelo   ({N}): {r_paralelo}")
    print(f"Son idénticas las secuencias: {r_secuencial==r_paralelo}")
    print(f"\nTiempo de ejecución paralelo: {t_paralelo:.4f} segundos")
    print(f"Tiempo de ejecución secuencial: {t_secuencial:.4f} segundos")
    print(f"Speedup: {t_secuencial / t_paralelo:.2f}x")
    print(f"Tiempo total: {t_paralelo+t_secuencial:.4f} segundos")


if __name__ == "__main__":
    N = 8000  # Número de Fibonacci a calcular

    t_paralelo, r_paralelo = calcular_fibonacci_paralelo(
        N, 
        concurrent.futures.ProcessPoolExecutor,
        chunksize=8)

    t_secuencial, r_secuencial = calcular_fibonacci_secuencial(N)

    print_results(t_paralelo, r_paralelo, t_secuencial, r_secuencial)
