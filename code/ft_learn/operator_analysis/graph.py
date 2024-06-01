import numpy as np

class Graph:
    def __init__(self, initial_population):
        self.graph = {}
        self.vertices = {}
        self.initial_population = []
        
        for i in initial_population:
            self.add_vertex(str(i), "", [], 0)
            self.initial_population.append(str(i))


    def add_vertex(self, ft, operator, parent, generation):        
        if ft not in self.vertices:
            vertex = Vertex(ft, operator, parent, generation)
            self.graph[vertex] = []
            self.vertices[ft] = vertex
            
            
    def get_vertex(self, ft): 
        return self.vertices[ft]


    def add_edge(self, parent, child):
        for i in parent:
            self.graph[self.get_vertex(i)].append(self.get_vertex(child))
            
    
    def find_route(self, end):
        all_paths = []
        stack = []
        
        for start in self.initial_population:
            start_vertex = self.get_vertex(start)
            stack.append(start_vertex, [], {start_vertex})  # stack of tuples (current node, current path, visited nodes set)
            
        while stack:
            current, path, visited = stack.pop()
            
            # Create a new path for the current state
            new_path = path + [(current.get_ft(), [p for p in current.get_parent()], current.get_generation(), current.get_operator())]

            if current.get_ft() == end:
                all_paths.append(new_path)
            else:
                for neighbour in self.graph[current]:
                    if neighbour not in visited:
                        # Create a new visited set that includes the neighbour
                        new_visited = visited | {neighbour}
                        stack.append((neighbour, new_path, new_visited))
                        
        return all_paths

    
    def trace_back(self, ft):
        current = self.get_vertex(ft)
        data = []
        
        while current is not None:
            data.append([(current.get_ft(), [p for p in current.get_parent()], current.get_generation(), current.get_operator())])
            
            if current.get_parent() == []:
                break
            
            current = self.get_vertex(current.get_parent()[0])
            
            for i in current.get_parent():
                parent = self.get_vertex(i)
                if parent.get_generation() > current.get_generation():
                    current = parent
            
        return data
                


    def bfs(self):
        visited = set()
        queue = []
        data = []
        for x in self.initial_population:
            v = self.get_vertex(x)
            queue.append(v)
            visited.add(v)
        
        while queue:
            vertex = queue.pop(0)
                
            for i in vertex.get_parent():
                data.append([vertex.get_ft(), i, vertex.get_metrics(), self.get_vertex(i).get_metrics(), vertex.get_operator(), vertex.get_generation()])
                
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    
        return data
    

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
        