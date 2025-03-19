import matplotlib.pyplot as plt
import numpy as np

# Set fonts for English labels
plt.rcParams['font.sans-serif'] = ['Arial']  # Use a common English font
plt.rcParams['axes.unicode_minus'] = False  # Fix negative sign display

# Time data in milliseconds
times = {
    'Random Data': {
        'Optimized QuickSort': 19.31,
        'Naive QuickSort': 12.30,
        'Merge Sort': 24.97,
        'Heap Sort': 37.39
    },
    'Ordered Data': {
        'Optimized QuickSort': 18.24,
        'Naive QuickSort': 12.19,
        'Merge Sort': 24.14,
        'Heap Sort': 37.01
    },
    'Partially Ordered': {
        'Optimized QuickSort': 18.21,
        'Naive QuickSort': 12.21,
        'Merge Sort': 25.46,
        'Heap Sort': 37.82
    },
    'Duplicate Data': {
        'Optimized QuickSort': 1034.99,
        'Naive QuickSort': 1021.33,
        'Merge Sort': 23.90,
        'Heap Sort': 33.86
    }
}

datasets = list(times.keys())
algorithms = list(times['Random Data'].keys())
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
n_datasets = len(datasets)
n_algorithms = len(algorithms)

# Calculate bar positions
width = 0.8 / n_algorithms
offsets = [(i - (n_algorithms-1)/2) * width for i in range(n_algorithms)]

plt.figure(figsize=(12, 6), dpi=100)

# Plot bars
for ds_idx, dataset in enumerate(datasets):
    x = ds_idx
    for algo_idx, algo in enumerate(algorithms):
        x_pos = x + offsets[algo_idx]
        time = times[dataset][algo]
        label = algo if ds_idx == 0 else None
        plt.bar(x_pos, time, width=width, color=colors[algo_idx], label=label)

# Set labels and title
plt.xticks(np.arange(n_datasets), datasets)
plt.xlabel('Dataset Type')
plt.ylabel('Time (ms)')
plt.title('Performance Comparison of Sorting Algorithms')
plt.yscale('log')

# Add legend
plt.legend(title="Algorithms", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
