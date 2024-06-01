import numpy as np
import pandas as pd
from scipy.stats import kruskal
from scipy.stats import mannwhitneyu
import itertools
import matplotlib.pyplot as plt
import os
import time


def difference(arr):
    for i in arr:
        if len(i[3]) == 0:
            i[3] = i[2].copy()
    
    df = pd.DataFrame(arr, columns=['Child', 'Parent', 'Child_Metrics', 'Parent_Metrics', 'Operator', 'Generation'])
    # Calculate differences
    metrics = {
        'ϕ_spec': 6,
        'ϕ_npv': 8,
        'ϕ_prec': 5,
        'ϕ_mcc': 15,
        'ϕ_acc': 11,
        'ϕ_s': 1,
        'ϕ_dor': 22
    }
    
    # print(df)
    
    for metric, index in metrics.items():
        df[metric] = df['Child_Metrics'].apply(lambda x: x[index]) - df['Parent_Metrics'].apply(lambda x: x[index])

    
    # grouped_data_by_generation = {metric: df.groupby('Generation', 'Opearator')[metric].apply(list) for metric in metrics}
    # grouped_data = {metric: df.groupby(['Operator', 'Generation'])[metric].mean() for metric in metrics}
    
    # print(grouped_data)
    
    grouped_data = {}
    for metric in metrics:
        grouped = df.groupby(['Operator', 'Generation'])[metric].mean().reset_index(name=f'Mean')
        grouped_data[metric] = grouped
        
    output_folder = 'ft_learn/operator_analysis/plots_' + time.strftime('%Y-%m-%d_%H-%M-%S')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    color_map = {
        'disconnect_be': 'blue',
        'delete_be': 'green',
        'create_gate': 'red',
        'change_gate_type': 'purple',
        'create_be': 'orange',
        'cross_over': 'brown',
        'delete_gate': 'pink',
        'connect_be': 'gray',
        'move_be': 'cyan',
    }
    
    for metric in metrics.keys():
        plt.figure(figsize=(10, 6))
        
        for operator in df['Operator'].unique():
            subset = grouped_data[metric][grouped_data[metric]['Operator'] == operator]
            plt.plot(subset['Generation'], subset['Mean'], label=operator, color=color_map.get(operator, 'black'))
        
        plt.xlabel('Generation')
        plt.ylabel(f'Mean {metric}')
        plt.title(f'Mean {metric} by Generation and Operator')
        plt.legend(title='Operator')
        plt.grid(True)
        
        filename = os.path.join(output_folder, f'{metric}.png')
        plt.savefig(filename)




















    # def all_identical(lst):
    #     return all(x == lst[0] for x in lst)

    # def perform_kruskal_wallis(df, metric, grouped_data):
    #     if not all_identical(df[metric].values):
    #         kruskal_stat, kruskal_p = kruskal(*grouped_data[metric])
    #         # print(f'Kruskal-Wallis test results for {metric}: H-statistic={kruskal_stat}, P-value={kruskal_p}')
    #         return kruskal_p
    #     else:
    #         # print(f'All values are identical for {metric}. Skipping Kruskal-Wallis test.')
    #         return 1

    # def pairwise_mannwhitneyu(groups, alpha=0.05):
    #     pairs = list(itertools.combinations(groups.keys(), 2))
    #     p_values = []
    #     for (op1, op2) in pairs:
    #         u_stat, p_val = mannwhitneyu(groups[op1], groups[op2], alternative='two-sided')
    #         p_values.append((op1, op2, p_val, np.median(groups[op1]), np.median(groups[op2])))
    #     corrected_p_values = [(op1, op2, min(p_val * len(pairs), 1.0), med1, med2) for op1, op2, p_val, med1, med2 in p_values]
    #     return corrected_p_values

    # kruskal_p_values = {}
    # for metric in metrics.keys():
    #     kruskal_p_values[metric] = perform_kruskal_wallis(df, metric, grouped_data)
    
    # print("Mann-Whitney U-----------------------------------------")
    # for metric, p_value in kruskal_p_values.items():
    #     if p_value < 0.05:
    #         print(f'Significant differences found for {metric}. Performing pairwise comparisons:')
    #         comparisons = pairwise_mannwhitneyu(grouped_data[metric])
    #         for op1, op2, p_val, med1, med2 in comparisons:
    #             if p_val < 0.05:
    #                 higher_op = op1 if med1 > med2 else op2
    #                 print(f'{metric}: Mann-Whitney U test between {op1} and {op2}: corrected P-value={p_val}. Higher improvement: {higher_op}')
