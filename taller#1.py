
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
        c = b
        b = a + b
        a = c
    return a

def calcular_fibonacci_secuencial(n_elementos):
    """
    Calcula los números de Fibonacci de forma secuencial
    Se utiliza como referencia para comparar la ganancia en rendimiento
    """

    inicio = time.time()

    results = []

    for i in range(n_elementos + 1):
        results.append(fibonacci(i))

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    return tiempo_ejecucion, results

def calcular_fibonacci_paralelo_map(n_elementos, executor_type, chunksize = 1, max_workers = None):
    """
    Calcula los números de Fibonacci utilizando
    un Executor de Procesos de concurrent.futures. y el método map()
    """

    inicio = time.time()

    """
    Creación de tareas: paralelizable
    fibonacci(i) no depende de fibonacci(j), no leen
    ni escriben estado compartido entre sí. Por eso se puede repartir 
    sin riesgo de condiciones de carrera entre varios workers.
    
    executor.map() además conserva el orden de entrada en la salida;
    resultados[i] siempre corresponde a fibonacci(i), sin importar en qué orden
    terminen los workers, así se evita un orden incorrecto.

    Trampas seriales evitadas:
    No se imprime dentro de los workers. La impresión se hace
    una sola vez al final, en el proceso principal, evitando
    salidas desordenadas y conflictos de acceso.
    """

    with executor_type(max_workers = max_workers) as executor:
        results = executor.map(fibonacci, range(n_elementos + 1), chunksize = chunksize)


    fin = time.time()
    tiempo_ejecucion = fin - inicio

    return tiempo_ejecucion, list(results)

def calcular_fibonacci_paralelo_proc(n_elementos, executor_type):
    """
    Calcula los números de Fibonacci utilizando
    un Executor de Procesos de concurrent.futures.
    Con asignación manual de tareas a procesos
    """

    inicio = time.time()

    """
    Distribución en procesos sin división en chunk.
    Apenas termina una tarea, el procesador se ocupa con otro proceso.
    División de carga de cómputo más equitativa según crecimiento exponencial
    de secuencia de Fibonacci.
    """

    numbers = range(n_elementos + 1)
    with executor_type() as executor:
        futures = {executor.submit(fibonacci, n):n for n in numbers}

        results = []
        results_dict = {}

        for future in concurrent.futures.as_completed(futures):
            results_dict[futures[future]] = future.result()

    results = [results_dict[n] for n in numbers] #Reconstrucción de orden original de resultados

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    return tiempo_ejecucion, list(results)



def print_results(t_paralelo_map, r_paralelo_map, t_paralelo_proc, r_paralelo_proc, t_secuencial, r_secuencial):
    """
    Impresión: serial, hecha una sola vez en el proceso principal,
    después de que todos los resultados ya llegaron evitando salidas corruptas.
    """
    print(f"Fibonacci secuencial ({N}): {r_secuencial}")
    print(f"Fibonacci paralelo con map   ({N}): {r_paralelo_map}")
    print(f"Fibonacci paralelo con procesos   ({N}): {r_paralelo_proc}")
    print(f"Son idénticas las secuencias: {r_secuencial==r_paralelo_map==r_paralelo_proc}")
    print("\n")
    print(f"Tiempo de ejecución paralelo con map: {t_paralelo_map:.4f} segundos")
    print(f"Tiempo de ejecución paralelo con procesos: {t_paralelo_proc:.4f} segundos")
    print(f"Tiempo de ejecución secuencial: {t_secuencial:.4f} segundos")
    print(f"Speedup con map(): {t_secuencial / t_paralelo_map:.2f}x")
    print(f"Speedup con procesos: {t_secuencial / t_paralelo_proc:.2f}x")
    print(f"Tiempo total: {t_paralelo_map+t_secuencial+t_paralelo_proc:.4f} segundos")


if __name__ == "__main__":
    N = 10  # Número de Fibonacci a calcular

    """
    Se emplea ProcessPoolExecutor dado que la división en procesos
    permite sobrepasar el GIL de Python y ejecutar con verdadero paralelismo
    con cada proceso corriendo en núcleos distintos (según disponibilidad de hardware)
    """
    t_paralelo_map, r_paralelo_map = calcular_fibonacci_paralelo_map(
        N, 
        concurrent.futures.ProcessPoolExecutor,
        chunksize=100)
    
    t_paralelo_proc, r_paralelo_proc = calcular_fibonacci_paralelo_proc(
            N, 
            concurrent.futures.ProcessPoolExecutor)
    

    t_secuencial, r_secuencial = calcular_fibonacci_secuencial(N)

    print_results(t_paralelo_map, r_paralelo_map, t_paralelo_proc, r_paralelo_proc, t_secuencial, r_secuencial)
