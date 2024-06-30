import numpy as np
import pandas as pd
import os
import time

class Graph:
    def __init__(self, initial_population):
        self.graph = {}
        self.vertices = {}
        self.vertices_single_key = {}
        self.initial_population = []
        self.generation_to_fts = {}
        
        for i in initial_population:
            self.add_vertex(str(i), "", [], 0)
            self.initial_population.append(str(i))


    def add_vertex(self, ft, operator, parent, generation):        
        if (ft, operator, generation) not in self.vertices:
            vertex = Vertex(ft, operator, parent, generation)
            self.graph[vertex] = []
            self.vertices[(ft, operator, generation)] = vertex
            
            if generation not in self.generation_to_fts:
                self.generation_to_fts[generation] = []
            self.generation_to_fts[generation].append(vertex)
                
            if ft not in self.vertices_single_key:
                self.vertices_single_key[ft] = vertex
                            
            
    def get_vertex(self, ft, operator, generation): 
        return self.vertices[(ft, operator, generation)]
    
    
    def get_vertex_single(self, ft):
        return self.vertices_single_key[ft]


    def add_edge(self, parent, child, operator, generation):
        for i in parent:
            # think later if we want to put the generation for the parent
            self.graph[self.get_vertex_single(i)].append(self.get_vertex(child, operator, generation))
            
            
    def set_metrics_for_all(self, metrics, generation):
        for i in self.generation_to_fts[generation]:
            if i.get_ft() in metrics:
                i.set_metrics(metrics[i.get_ft()])
    
    def get_vertices_by_generation_and_ft(self, generation, ft):
        vertices = []
        for i in self.generation_to_fts[generation]:
            if i.get_ft() == ft:
                vertices.append(i)
        return vertices
    
    
    def group_vertices_per_dominant_generation(self, population_per_generation, filename):
        generations = sorted(population_per_generation.keys())
        data = []
        for i in generations:
            vertices = self.generation_to_fts[i]
            dominant_generation = population_per_generation[i]
            for v in vertices:
                passed = 0
                
                if v.get_ft() in dominant_generation:
                    passed = 1
                    
                if v.get_ft() not in v.get_parent() and v.get_parent() != []:
                    data.append([v.get_ft(), v.get_parent(), v.get_operator(), v.get_generation(), v.get_metrics(), self.get_vertex_single(v.get_parent()[0]).get_metrics(), passed])
                        
        output_folder = 'ft_learn/operator_analysis/saved_data_frames/difference' + f'/{filename}'
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        df = pd.DataFrame(data, columns=['Tree', 'Parent Tree', 'Operator', 'Generation', 'Metrics', 'Parent Metrics', 'Passed'])
        df.to_pickle(output_folder + f'/{filename}' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.pkl')
        
    
    def generate_tensor(self, population_per_generation, filename):
        map = {
            'spec': 6,
            'npv': 8,
            'prec': 5,
            'mcc': 15,
            'acc': 11,
            's': 1,
            'dor': 22
        }
        
        data = []
        generations = sorted(population_per_generation.keys())
        
        for i in generations:            
            for j in range(len(population_per_generation[i])):
                ft = population_per_generation[i][j]
                v = self.get_vertex_single(ft)
                for metric_name, index in map.items():
                    data.append([ft, j, metric_name, i, v.get_metrics()[index]])
                    
                    
        output_folder = 'ft_learn/operator_analysis/saved_data_frames/tensor' + f'/{filename}'
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        df = pd.DataFrame(data, columns=['FT', 'Position of the FT in the generation', 'Metric Name', 'Generation', 'Value'])
        df.to_pickle(output_folder + f'/{filename}' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.pkl')
        with open('output-test_tensor.txt', 'w') as f:
            f.write(df.to_string())
    
    
    def trace_back(self, ft, generation):
        data = []
        current_vertices = self.get_vertices_by_generation_and_ft(generation, ft)
         
        while current_vertices != []:
            current = current_vertices[0]
            operators = []
            
            for i in current_vertices:
                operators.append(i.get_operator())       
                         
            data.append([current.get_ft(), generation, operators])
            
            generation = current.get_generation() - 1
            
            if current.get_parent() == [] or generation == -1:
                break
                
            ft = current.get_parent()[0]
            current_vertices = self.get_vertices_by_generation_and_ft(generation, ft)
            
        return data
            
    
    def get_p_and_d_dataset(self, population_per_generation, filename):
        generations = sorted(self.generation_to_fts.keys())
        last_generation = generations[-1]
        
        map = {
            'ϕ_spec': 6,
            'ϕ_npv': 8,
            'ϕ_prec': 5,
            'ϕ_mcc': 15,
            'ϕ_acc': 11,
            'ϕ_s': 1,
            'ϕ_dor': 22
        }
        
        p_data = []
        d_data = []
        
        for ft in population_per_generation[last_generation]:
            d_data.append([ft, self.trace_back(ft, last_generation)])
            v = self.get_vertex_single(ft)
            metrics = []
            for metric_name, index in map.items():
                metrics.append(v.get_metrics()[index])
            
            result = [v.get_ft()]
            result.extend(metrics)
            p_data.append(result)
        
        p = pd.DataFrame(p_data, columns=['Tree', 'spec', 'npv', 'prec', 'mcc', 'acc', 's', 'dor'])
        d = pd.DataFrame(d_data, columns=['Tree', 'Evolution'])
        
        output_folder = 'ft_learn/operator_analysis/saved_data_frames/d_and_p_dataset' + f'/{filename}' + f'/{filename}' + time.strftime('%Y-%m-%d_%H-%M-%S')
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        p.to_pickle(output_folder + '/p' + '.pkl')
        d.to_pickle(output_folder + '/d' + '.pkl')


class Vertex:
    def __init__(self, ft, operator, parent, generation):
        self.ft = ft
        self.operator = operator
        self.metrics = []
        self.parent = parent
        self.generation = generation
        
    def set_operator(self, operator):
        self.operator = operator
        
    def set_metrics(self, metrics):
        self.metrics = metrics
        
    def get_metrics(self):
        return self.metrics
        
    def get_operator(self):
        return self.operator
    
    def get_ft(self):
        return self.ft
    
    def get_parent(self):
        return self.parent
    
    def get_generation(self):
        return self.generation
        