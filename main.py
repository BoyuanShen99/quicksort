import random
import time
import copy
import sys
import psutil
import os
from memory_profiler import memory_usage

class SortStats:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.max_depth = 0
        self.time_taken = 0.0
        self.peak_memory = 0

# 数据生成函数
def generate_random(n):
    return [random.randint(0, n*10) for _ in range(n)]

def generate_sorted(n):
    return list(range(n))

def generate_partially_sorted(n, perturbation=0.1):
    arr = list(range(n))
    num_perturbations = int(n * perturbation)
    for _ in range(num_perturbations):
        i, j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def generate_repeated(n, repeat_ratio=0.5):
    repeated_value = random.randint(0, n*10)
    arr = [repeated_value] * int(n * repeat_ratio)
    arr += [random.randint(0, n*10) for _ in range(n - len(arr))]
    random.shuffle(arr)
    return arr

# 快速排序优化版（随机枢轴+尾递归优化）
def quicksort_optimized(arr, stats):
    stack = [(0, len(arr)-1, 1)]
    max_depth = 0
    while stack:
        low, high, depth = stack.pop()
        if low >= high:
            continue
        if depth > max_depth:
            max_depth = depth

        # 随机选择枢轴
        pivot_idx = random.randint(low, high)
        arr[low], arr[pivot_idx] = arr[pivot_idx], arr[low]
        pivot = arr[low]
        stats.swaps += 1

        # 分区操作
        i = low + 1
        j = high
        while i <= j:
            stats.comparisons += 1
            while i <= j and arr[i] <= pivot:
                stats.comparisons += 1
                i += 1

            stats.comparisons += 1
            while i <= j and arr[j] > pivot:
                stats.comparisons += 1
                j -= 1

            if i < j:
                arr[i], arr[j] = arr[j], arr[i]
                stats.swaps += 1
                i += 1
                j -= 1

        # 放置枢轴
        arr[low], arr[j] = arr[j], arr[low]
        stats.swaps += 1

        # 优先处理较小的子数组
        if (j - low) > (high - j):
            stack.append((j+1, high, depth+1))
            stack.append((low, j-1, depth+1))
        else:
            stack.append((low, j-1, depth+1))
            stack.append((j+1, high, depth+1))

    stats.max_depth = max_depth

# 朴素快速排序（固定枢轴）
def quicksort_naive(arr, stats):
    stack = [(0, len(arr)-1, 1)]
    max_depth = 0
    while stack:
        low, high, depth = stack.pop()
        if low >= high:
            continue
        if depth > max_depth:
            max_depth = depth

        # 固定中间枢轴
        mid = (low + high) // 2
        arr[low], arr[mid] = arr[mid], arr[low]
        pivot = arr[low]
        stats.swaps += 1

        # 分区操作
        i = low + 1
        j = high
        while i <= j:
            stats.comparisons += 1
            while i <= j and arr[i] <= pivot:
                stats.comparisons += 1
                i += 1

            stats.comparisons += 1
            while i <= j and arr[j] > pivot:
                stats.comparisons += 1
                j -= 1

            if i < j:
                arr[i], arr[j] = arr[j], arr[i]
                stats.swaps += 1
                i += 1
                j -= 1

        arr[low], arr[j] = arr[j], arr[low]
        stats.swaps += 1

        stack.append((low, j-1, depth+1))
        stack.append((j+1, high, depth+1))

    stats.max_depth = max_depth

# 归并排序
def mergesort(arr, stats):
    def _mergesort(l, r, depth):
        nonlocal max_depth
        if depth > max_depth:
            max_depth = depth
        if l >= r:
            return

        mid = (l + r) // 2
        _mergesort(l, mid, depth+1)
        _mergesort(mid+1, r, depth+1)
        merge(l, mid, r)

    def merge(l, mid, r):
        left = arr[l:mid+1]
        right = arr[mid+1:r+1]
        i = j = 0
        k = l

        while i < len(left) and j < len(right):
            stats.comparisons += 1
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            stats.swaps += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            stats.swaps += 1
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            stats.swaps += 1
            j += 1
            k += 1

    max_depth = 0
    _mergesort(0, len(arr)-1, 1)
    stats.max_depth = max_depth

# 堆排序
def heapsort(arr, stats):
    def heapify(n, root):
        current = root
        while True:
            largest = current
            left = 2*current + 1
            right = 2*current + 2

            if left < n:
                stats.comparisons += 1
                if arr[left] > arr[largest]:
                    largest = left

            if right < n:
                stats.comparisons += 1
                if arr[right] > arr[largest]:
                    largest = right

            if largest == current:
                break

            arr[current], arr[largest] = arr[largest], arr[current]
            stats.swaps += 1
            current = largest

    n = len(arr)

    # 建堆
    for i in range(n//2-1, -1, -1):
        heapify(n, i)

    # 排序
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        stats.swaps += 1
        heapify(i, 0)

# 测试框架

def run_experiment(datasets, algorithms, runs=10):
    results = {}

    for data_name, data in datasets.items():
        results[data_name] = {}
        print(f"\n=== 正在测试数据集: {data_name} ===")

        for algo_name, algo in algorithms.items():
            print(f"\n正在运行算法: {algo_name}...")
            stats_list = []

            for _ in range(runs):
                test_data = copy.deepcopy(data)
                stats = SortStats()

                # 定义包装函数以同时测量时间和内存
                def sort_wrapper():
                    start_time = time.perf_counter()  # 记录开始时间
                    algo(test_data, stats)           # 实际排序逻辑
                    end_time = time.perf_counter()    # 记录结束时间
                    stats.time_taken = (end_time - start_time) * 1000  # 转换为毫秒

                # 执行并测量内存
                mem_usage = memory_usage(sort_wrapper, interval=0.1, max_usage=True)

                # 记录峰值内存（此处 mem_usage 已为浮点数）
                stats.peak_memory = mem_usage if mem_usage else 0

                # 验证排序结果
                assert test_data == sorted(data), "排序结果验证失败"

                stats_list.append(stats)
            # 计算平均指标
            avg_stats = SortStats()
            for key in ["comparisons", "swaps", "max_depth", "time_taken", "peak_memory"]:
                setattr(avg_stats, key, sum(getattr(s, key) for s in stats_list) / runs)

            results[data_name][algo_name] = avg_stats

    return results

# 结果展示
def print_results(results):
    for data_name, algorithms in results.items():
        print(f"\n\n=== 数据集: {data_name} ===")
        print(f"{'算法':<20} | {'时间(ms)':<10} | {'内存(MB)':<10} | {'比较次数':<12} | {'交换次数':<12} | {'最大深度'}")
        print("-"*80)

        for algo_name, stats in algorithms.items():
            print(f"{algo_name:<20} | {stats.time_taken:>9.2f} | {stats.peak_memory:>9.2f} | "
                  f"{int(stats.comparisons):>12} | {int(stats.swaps):>12} | {int(stats.max_depth)}")

if __name__ == "__main__":
    # 配置参数
    data_size = 10000  # 可调整测试规模
    algorithms = {
        "优化快排": quicksort_optimized,
        "朴素快排": quicksort_naive,
        "归并排序": mergesort,
        "堆排序": heapsort
    }

    # 生成测试数据
    datasets = {
        "随机数据": generate_random(data_size),
        "有序数据": generate_sorted(data_size),
        "部分有序": generate_partially_sorted(data_size),
        "重复数据": generate_repeated(data_size)
    }

    # 运行实验
    results = run_experiment(datasets, algorithms)

    # 打印结果
    print_results(results)