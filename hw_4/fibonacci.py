import time
import threading
import multiprocessing


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def worker_mp(n, results, index):
    results[index] = fibonacci(n)


def synchronous_execution(n, count=10):
    start_time = time.time()
    results = []
    
    for i in range(count):
        results.append(fibonacci(n))
    
    execution_time = time.time() - start_time
    return execution_time, results


def threading_execution(n, count=10):
    start_time = time.time()
    threads = []
    results = [None] * count
    
    def worker(index):
        results[index] = fibonacci(n)
    
    for i in range(count):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    execution_time = time.time() - start_time
    return execution_time, results


def multiprocessing_execution(n, count=10):
    start_time = time.time()
    processes = []
    manager = multiprocessing.Manager()
    results = manager.list([None] * count)
    
    for i in range(count):
        process = multiprocessing.Process(target=worker_mp, args=(n, results, i))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    execution_time = time.time() - start_time
    return execution_time, list(results)


def main():
    n = 38
    count = 10
        
    sync_time, sync_results = synchronous_execution(n, count)
    
    thread_time, thread_results = threading_execution(n, count)
    
    mp_time, mp_results = multiprocessing_execution(n, count)
    
    with open("artifacts/results.txt", 'w', encoding='utf-8') as f:
        f.write(f"Вычисление fibonacci({n}), запусков: {count}\n\n")
        f.write(f"Синхронное выполнение: {sync_time:.4f} сек\n")
        f.write(f"Threading: {thread_time:.4f} сек (x{sync_time/thread_time:.2f})\n")
        f.write(f"Multiprocessing: {mp_time:.4f} сек (x{sync_time/mp_time:.2f})\n\n")
        f.write(f"Результат: {sync_results[0]}\n")


if __name__ == "__main__":
    main()