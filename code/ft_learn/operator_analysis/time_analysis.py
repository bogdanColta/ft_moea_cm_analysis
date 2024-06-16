import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import sys


def graph(list_df, file):  
    data = aggregate(list_df)
      
    output_folder = 'plots/plot_' + file + '_' + time.strftime('%Y-%m-%d_%H-%M-%S')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    plt.figure(figsize=(10, 6))
    
    for generation in df['Operator'].unique():
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
    
def aggregate(list_df):
    data_x = {}
    
    for df in list_df:
        generation = 0
        for index, row in df.iterrows():
            total_time = 0
            total_time += row['generation']
            total_time += row['metrics']
            total_time += row['pareto_sorting']
            if(generation not in data_x):
                data_x[generation] = []
            
            data_x[generation].append(row['metrics'])
            generation += 1
            
    return data_x
    

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

    aggregate(dataframes)