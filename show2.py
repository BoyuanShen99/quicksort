import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 删除中文字体设置
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

# 数据集键名和列名翻译
comparison_data = {
    'Optimized QS': [674912, 659849, 659249, 12658034],  # 优化快排
    'Naive QS': [545874, 501756, 513856, 12614218],      # 朴素快排
    'Merge Sort': [299915, 241528, 280910, 282681],      # 归并排序
    'Heap Sort': [504477, 635596, 535878, 602455]        # 堆排序
}
comparison_df = pd.DataFrame(comparison_data).T
comparison_df.columns = ['Random', 'Sorted', 'Part-Sorted', 'Duplicates']  # 数据集类型

swap_data = {
    'Optimized QS': [78377, 52021, 56249, 29774],
    'Naive QS': [73725, 47232, 51913, 29660],
    'Merge Sort': [481017, 467656, 454294, 454294],
    'Heap Sort': [268889, 343085, 288453, 318855]
}
swap_df = pd.DataFrame(swap_data).T
swap_df.columns = ['Random', 'Sorted', 'Part-Sorted', 'Duplicates']

# 热力图标题和标签英化
plt.figure(figsize=(12, 6))
log_comparison = np.log10(comparison_df)
annot_comparison = comparison_df.applymap(lambda x: f"{x:,.0f}")
sns.heatmap(
    log_comparison,
    annot=annot_comparison,
    fmt='',
    cmap='YlGnBu',
    cbar_kws={'label': 'log10 Scale'}  # 颜色条标签
)
plt.title('Comparison Operations by Algorithm\n(Color intensity represents log-scaled complexity)', y=1.02)
plt.ylabel('Sorting Algorithms')
plt.xlabel('Dataset Type')
plt.tight_layout()
plt.savefig('comparison_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(12, 6))
annot_swap = swap_df.applymap(lambda x: f"{x:,.0f}")
sns.heatmap(
    swap_df,
    annot=annot_swap,
    fmt='',
    cmap='YlOrRd',
    cbar_kws={'label': 'Swap Counts'}
)
plt.title('Swap Operations Comparison', y=1.02)
plt.ylabel('Sorting Algorithms')
plt.xlabel('Dataset Type')
plt.tight_layout()
plt.savefig('swap_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
