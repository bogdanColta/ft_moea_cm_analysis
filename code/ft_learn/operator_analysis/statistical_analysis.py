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
        'do_nothing' : 'black'
    } 
    
    
    # for metric in metrics.keys():
    #     plt.figure(figsize=(10, 6))
        
    #     for operator in df['Operator'].unique():
    #         subset = df[df['Operator'] == operator]
    #         subset = subset[subset['Passed'] == 1]
    #         generations = subset['Generation'].unique()
    #         generations.sort()
            
    #         x = []
    #         mean = []
            
    #         for i in range(len(generations)):
    #             x.append(generations[i])
    #             mean.append(subset[subset['Generation'] == generations[i]][metric].mean())
                    
    #         # Plot mean line
    #         plt.plot(x, mean, label=f'{operator}', color=color_map.get(operator, 'black'))
        
    #     plt.xlabel('Generation')
    #     plt.ylabel(f'Mean of difference between child and parent {metric}')
    #     plt.title(f'Mean of difference between child and parent {metric} by Generation and Operator')
    #     plt.legend(title='Operator')
    #     plt.grid(True)
        
    #     filename = os.path.join(output_folder, f'{metric}.png')
    #     plt.savefig(filename)
    #     plt.close()
        
    
    plt.figure(figsize=(10, 6))
    generations = df['Generation'].unique()
    generations.sort()
    
    for operator in df['Operator'].unique():
        x = []
        y = []
        
        for i in range(len(generations)):
            subset_of_generation = df[df['Generation'] == i]
            # subset_of_generation = subset_of_generation[subset_of_generation['Passed'] == 1]
            x.append(generations[i])
            y.append(len(subset_of_generation[subset_of_generation['Operator'] == operator])/400)
   
        plt.plot(x, y, label=f'{operator}', color=color_map.get(operator, 'black'))
    
    plt.xlabel('Generation')
    plt.ylabel(f'Percentage of successful operators')
    plt.title(f'Percentage of successful operators by Generation and Operator')
    plt.legend(title='Operator')
    plt.grid(True)
    
    filename = os.path.join(output_folder, f'successful_operators.png')
    plt.savefig(filename)
    
    plt.close()
    
    # --------------------------------------------------------
    
    
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

def all_dataframes(list_df):
    data_x = {}
    data_y = {}
    
    for df in list_df:
        generations = df['Generation'].unique()
        generations.sort()
        
        for operator in df['Operator'].unique():
            x = []
            y = []
            
            for i in range(len(generations)):
                subset_of_generation = df[df['Generation'] == i]
                x.append(generations[i])
                y.append(len(subset_of_generation[subset_of_generation['Operator'] == operator])/400)

            if operator not in data_x:
                data_x[operator] = []
                data_y[operator] = []
                
            data_x[operator].append(x)
            data_y[operator].append(y)
            
                
    data_agg_x = {}
    data_agg_y = {}
                
    for operator in data_x.keys():
        x_list = data_x[operator]
        y_list = data_y[operator]
            
        intersection = set(x_list[0])
        for x in x_list[1:]:
            intersection.intersection_update(x)

        data_agg_x[operator] = list(intersection)
        
        y_agg = []
        for x in data_agg_x[operator]:
            agg = []
            
            for y in y_list:
                agg.append(y[x])
                
            y_agg.append(agg)
            
        data_agg_y[operator] = y_agg
    
    return data_agg_x , data_agg_y
    
def graph(list_df, file):
    data_agg_x , data_agg_y = all_dataframes(list_df)
    
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
        'do_nothing' : 'black'
    } 
    
    plt.figure(figsize=(10, 6))
    
    for operator in df['Operator'].unique():
        x = []
        generations = data_agg_x[operator]
        mean = []
        median = []
        std = []
        
        for i in range(len(generations)):
            x.append(generations[i])
            mean.append(np.mean(data_agg_y[operator][generations[i]]))
            median.append(np.median(data_agg_y[operator][generations[i]]))
            std.append(np.std(data_agg_y[operator][generations[i]]))
   
        # Plot mean line
        plt.plot(x, mean, label=f'{operator} Mean', color=color_map.get(operator, 'black'))
        
        # Plot shaded area for std deviation
        plt.fill_between(x, np.array(mean) - np.array(std), np.array(mean) + np.array(std), 
                        color=color_map.get(operator, 'black'), alpha=0.2)
        
        # Plot median line with dotted style
        plt.plot(x, median, label=f'{operator} Median', color=color_map.get(operator, 'black'), linestyle=':')
    
            
    plt.xlabel('Generation')
    plt.ylabel(f'Percentage of successful operators')
    plt.title(f'Percentage of successful operators by Generation and Operator (x5)')
    plt.legend(title='Operator')
    plt.grid(True)
    
    filename = os.path.join(output_folder, 'successful operators.png')
    plt.savefig(filename)
    
    plt.close()
    

if __name__ == "__main__":
    folder_path = sys.argv[1]
    file_list = os.listdir(folder_path)
    dataframes = []
    filename = os.path.basename(os.path.normpath(folder_path))
    for file_name in file_list:
        if file_name.endswith('.pkl'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_pickle(file_path)
            dataframes.append(df)

    graph(dataframes, filename)
    
    # Perform operations on the dataframes
    # for df in dataframes:
    #     print(df)
    
    # df = pd.read_pickle(file)
    # file, file_extension = os.path.splitext(os.path.basename(file))
    
    # # Convert the DataFrame to a string
    # df_string = df.to_string()

    # # Write the string to a file
    # with open('output-test.txt', 'w') as f:
    #     f.write(df_string)
        
    # difference(df)