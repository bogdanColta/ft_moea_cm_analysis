import numpy as np
import pandas as pd
from scipy.stats import kruskal
from scipy.stats import mannwhitneyu
import itertools
import matplotlib.pyplot as plt
import os
import time
import sys

file = ""

def difference(df):
    metrics = {
        'ϕ_spec': 6,
        'ϕ_npv': 8,
        'ϕ_prec': 5,
        'ϕ_mcc': 15,
        'ϕ_acc': 11,
        'ϕ_s': 1,
        'ϕ_dor': 22
    }
        
    for metric, index in metrics.items():
        df[metric] = df['Child_Metrics'].apply(lambda x: x[index]) - df['Parent_Metrics'].apply(lambda x: x[index])

    output_folder = 'plots/plot_' + file + '_' + time.strftime('%Y-%m-%d_%H-%M-%S')

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
            subset = df[df['Operator'] == operator]
            generations = subset['Generation'].unique()
            generations.sort()
            
            x = []
            mean = []
            
            for i in range(len(generations)):
                x.append(generations[i])
                mean.append(subset[subset['Generation'] == generations[i]][metric].mean())
                    
            # Plot mean line
            plt.plot(x, mean, label=f'{operator} Mean', color=color_map.get(operator, 'black'))
        
        plt.xlabel('Generation')
        plt.ylabel(f'Mean of difference between child and parent {metric}')
        plt.title(f'Mean of difference between child and parent {metric} by Generation and Operator')
        plt.legend(title='Operator')
        plt.grid(True)
        
        filename = os.path.join(output_folder, f'{metric}.png')
        plt.savefig(filename)
        plt.close()
    
    
    # output_folder_metrics_operator = output_folder + '/std_median_per_metric_and_operator'
    # if not os.path.exists(output_folder_metrics_operator):
    #     os.makedirs(output_folder_metrics_operator)
    
    # for metric in metrics.keys():
    #     for operator in df['Operator'].unique():
    #         plt.figure(figsize=(10, 6))
    #         subset = df[df['Operator'] == operator]
    #         generations = subset['Generation'].unique()
    #         generations.sort()
            
    #         x = []
    #         mean = []
    #         std = []
    #         median = []
            
    #         for i in range(len(generations)):
    #             x.append(generations[i])
    #             mean.append(subset[subset['Generation'] == generations[i]][metric].mean())
    #             std.append(subset[subset['Generation'] == generations[i]][metric].std())
    #             median.append(subset[subset['Generation'] == generations[i]][metric].median())
                    
    #         # Plot mean line
    #         plt.plot(x, mean, label=f'{operator} Mean', color=color_map.get(operator, 'black'))
            
    #         # Plot shaded area for std deviation
    #         plt.fill_between(x, np.array(mean) - np.array(std), np.array(mean) + np.array(std), 
    #                         color=color_map.get(operator, 'black'), alpha=0.2)
            
    #         # Plot median line with dotted style
    #         plt.plot(x, median, label=f'{operator} Median', color=color_map.get(operator, 'black'), linestyle=':')
        
        
    #         plt.xlabel('Generation')
    #         plt.ylabel(f'Mean of difference between child and parent {metric}')
    #         plt.title(f'Mean of difference between child and parent {metric} by Generation and Operator')
    #         plt.legend(title='Operator')
    #         plt.grid(True)
            
    #         filename = os.path.join(output_folder_metrics_operator, f'{metric} for operator {operator}.png')
    #         plt.savefig(filename)
    #         plt.close()
        
    # output_folder_u = output_folder + '/u_tests'
    # if not os.path.exists(output_folder_u):
    #     os.makedirs(output_folder_u)    
        
    # for metric in metrics.keys():
    #     plt.figure(figsize=(10, 6))
        
    #     for operator in df['Operator'].unique():
    #         subset = df[df['Operator'] == operator]
    #         generations = subset['Generation'].unique()
    #         generations.sort()
            
    #         x = []
    #         y = []
            
    #         for i in range(len(generations) - 1):
    #             gen1 = generations[i]
    #             gen2 = generations[i + 1]
                
    #             data1 = subset[subset['Generation'] == gen1][metric]
    #             data2 = subset[subset['Generation'] == gen2][metric]
                
    #             if len(data1) > 0 and len(data2) > 0:
    #                 u, p = mannwhitneyu(data1, data2, alternative='two-sided')
                    
    #                 # if(p < 0.05):
    #                 #     print(f'P-value for {operator} between generations {gen1} and {gen2} is {p}')
                        
    #                 x.append((gen1 + gen2) / 2)  # Middle point between generations
    #                 y.append(p)

    #         plt.plot(x, y, label=operator, color=color_map.get(operator, 'black'))
        
    #     plt.axhline(y=0.05, color='red', linestyle='--', linewidth=1, label='Significance Level (0.05)')
    #     plt.xlabel('Generation')
    #     plt.ylabel(f'P-value of Mann-Whitney U Test for {metric}')
    #     plt.title(f'Mann-Whitney U Test P-values for {metric} by Generation and Operator')
    #     plt.legend(title='Operator')
    #     plt.grid(True)
        
    #     filename = os.path.join(output_folder_u, f'{metric}_U-Test.png')
    #     plt.savefig(filename)
        

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


if __name__ == "__main__":
    file = sys.argv[1]
    df = pd.read_pickle(file)
    file, file_extension = os.path.splitext(os.path.basename(file))
    # Convert the DataFrame to a string
    df_string = df.to_string()

    # Write the string to a file
    with open('output-test.txt', 'w') as f:
        f.write(df_string)
        
    difference(df)