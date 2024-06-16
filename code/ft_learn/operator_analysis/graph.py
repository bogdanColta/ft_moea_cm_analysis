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
    
    def trace_back(self, ft):
        # operator
        current = self.get_vertex_single(ft)
        data = []
        
        while current is not None:
            data.append([(current.get_ft(), [p for p in current.get_parent()], current.get_generation(), current.get_operator())])
            
            if current.get_parent() == []:
                break
            
            current = self.get_vertex_single(current.get_parent()[0])
            
            for i in current.get_parent():
                parent = self.get_vertex_single(i)
                if parent.get_generation() > current.get_generation():
                    current = parent
            
        return data
                


    # def bfs(self, population_per_generation, filename):
    #     # visited = set()
    #     # queue = []
    #     # data = []
    #     # for x in self.initial_population:
    #     #     v = self.get_vertex_single(x)
    #     #     queue.append(v)
    #     #     visited.add(v)
        
    #     # while queue:
    #     #     vertex = queue.pop(0)
                
    #     #     for i in vertex.get_parent():
    #     #         data.append([vertex.get_ft(), i, vertex.get_metrics(), self.get_vertex_single(i).get_metrics(), vertex.get_operator(), vertex.get_generation()])
                
    #     #     for neighbor in self.graph[vertex]:
    #     #         if neighbor not in visited:
    #     #             queue.append(neighbor)
    #     #             visited.add(neighbor)
        
        
    #     data = []
    #     generations = sorted(population_per_generation.keys())
    #     for i in generations:
    #         vertices = self.generation_to_fts[i]
    #         dominant_generation = population_per_generation[i]
    #         for v in vertices:
    #             first = True
    #             for i in v.get_parent():
    #                 passed = 0
    #                 if v.get_ft() in dominant_generation and v.get_ft() not in v.get_parent() and first:
    #                     first = False
    #                     passed = 1
                    
    #                 data.append([v.get_ft(), i, v.get_metrics(), self.get_vertex_single(i).get_metrics(), v.get_operator(), v.get_generation(), passed])
                        
    #     output_folder = 'ft_learn/operator_analysis/saved_data_frames' + f'/{filename}'
        
    #     if not os.path.exists(output_folder):
    #         os.makedirs(output_folder)
            
    #     df = pd.DataFrame(data, columns=['Child', 'Parent', 'Child_Metrics', 'Parent_Metrics', 'Operator', 'Generation', 'Passed'])
    #     df.to_pickle(output_folder + f'/{filename}' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.pkl')
    
    
    def group_vertices_per_dominant_generation(self, population_per_generation, filename):
        generations = sorted(population_per_generation.keys())
        data = []
        for i in generations:
            vertices = self.generation_to_fts[i]
            dominant_generation = population_per_generation[i]
            temp = []
            for v in vertices:
                if v.get_ft() in dominant_generation and v.get_ft() not in v.get_parent():
                    data.append([v.get_ft(), v.get_operator(), v.get_generation()])
                    temp.append(v.get_ft())
            
            temp = list(set(temp))
            print(len(temp))
        output_folder = 'ft_learn/operator_analysis/saved_data_frames' + f'/{filename}'
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        df = pd.DataFrame(data, columns=['Tree', 'Operator', 'Generation'])
        df.to_pickle(output_folder + f'/{filename}' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.pkl')


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
        