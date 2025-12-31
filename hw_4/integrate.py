import math
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def integrate_part(f, a, b, n_iter):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def worker(args):
    return integrate_part(*args)


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_thread(f, a, b, *, n_jobs=1, n_iter=10000000):
    chunk_size = n_iter // n_jobs
    ranges = [(f, a + i * (b - a) / n_jobs, a + (i + 1) * (b - a) / n_jobs, chunk_size)
              for i in range(n_jobs)]
    
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        results = executor.map(worker, ranges)
    
    return sum(results)


def integrate_process(f, a, b, *, n_jobs=1, n_iter=10000000):
    chunk_size = n_iter // n_jobs
    ranges = [(f, a + i * (b - a) / n_jobs, a + (i + 1) * (b - a) / n_jobs, chunk_size)
              for i in range(n_jobs)]
    
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        results = executor.map(worker, ranges)
    
    return sum(results)


def main():
    cpu_count = multiprocessing.cpu_count()
    max_workers = cpu_count * 2
    
    with open("artifacts/results_2.txt", 'w', encoding='utf-8') as f:
        f.write(f"CPU count: {cpu_count}\n\n")
        
        f.write("ThreadPoolExecutor:\n")
        for n_jobs in range(1, max_workers + 1):
            start = time.time()
            integrate_thread(math.cos, 0, math.pi / 2, n_jobs=n_jobs)
            f.write(f"n_jobs={n_jobs}: {time.time() - start:.4f}s\n")
        
        f.write("\nProcessPoolExecutor:\n")
        for n_jobs in range(1, max_workers + 1):
            start = time.time()
            integrate_process(math.cos, 0, math.pi / 2, n_jobs=n_jobs)
            f.write(f"n_jobs={n_jobs}: {time.time() - start:.4f}s\n")


if __name__ == "__main__":
    main()