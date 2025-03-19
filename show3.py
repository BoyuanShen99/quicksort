import matplotlib.pyplot as plt
import numpy as np

# Dataset and algorithm configuration
datasets = ['Random Data', 'Ordered Data', 'Partially Ordered', 'Repeated Data']
algorithms = ['Optimized Quick Sort', 'Naive Quick Sort', 'Merge Sort', 'Heap Sort']

# Maximum recursion depth data (using 1 for Heap Sort instead of 0 for log scale display)
data = {
    'Optimized Quick Sort': [30, 29, 29, 5007],
    'Naive Quick Sort': [14, 13, 13, 5005],
    'Merge Sort': [15, 15, 15, 15],
    'Heap Sort': [1, 1, 1, 1]  # Actual depth is 0, special handling for display
}

# Plotting parameter settings
x = np.arange(len(datasets))
bar_width = 0.2
offsets = [-0.3, -0.1, 0.1, 0.3]  # Position offsets for bars of each algorithm
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

plt.figure(figsize=(12, 6))

# Draw the bar chart
for idx, (algo, values) in enumerate(data.items()):
    bars = plt.bar(x + offsets[idx], values, width=bar_width,
                   color=colors[idx], label=algo)

    # Add data labels
    for bar in bars:
        height = bar.get_height()
        display_height = 0 if algo == 'Heap Sort' else height  # Display 0 for Heap Sort
        va = 'bottom' if height > 1 else 'top'             # Adjust label position
        color = 'black' if height > 1 else 'white'         # Adjust label color
        plt.text(bar.get_x() + bar.get_width()/2, height,
                 str(display_height), ha='center', va=va,
                 color=color, fontsize=8)

# Chart decoration
plt.xticks(x, datasets)
plt.xlabel('Dataset Type')
plt.ylabel('Maximum Recursion Depth (Log Scale)')
plt.title('Comparison of Maximum Recursion Depths of Different Sorting Algorithms (Actual Depth of Heap Sort is 0)', pad=20)
plt.legend(loc='upper left')
plt.yscale('log')  # Logarithmic axis
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(1, 10000)  # Set the Y-axis range to ensure Heap Sort is visible

plt.tight_layout()
plt.show()