import numpy as np

class Graph:
    def __init__(self, initial_population):
        self.graph = {}
        self.vertices = []
        self.initial_population = []
        
        for i in initial_population:
            self.add_vertex(str(i), "", None, 0)
            self.initial_population.append(str(i))

    def add_vertex(self, ft, operator, parent, generation):
        vertex = Vertex(ft, operator, parent, generation)
        self.graph[vertex] = []
        self.vertices.append(vertex)
        return vertex
            
    def getVertex(self, ft):
        for v in self.vertices:
            if ft == v.getFT():
                return v


    def add_edge(self, parent, child):
        v = self.getVertex(parent)
        # operators = v.getOperators().copy()
        # operators.append(operator)
        # self.getVertex(child).setOperators(operator)
        self.graph[self.getVertex(parent)].append(self.getVertex(child))


    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=' ')
        for neighbor in self.graph[start]:
            if neighbor not in visited:
                self.dfs(neighbor, visited)


    def bfs(self):
        visited = set()
        queue = []
        data = []
        for x in self.initial_population:
            queue.append(self.getVertex(x))
            visited.add(self.getVertex(x))
        
        while queue:
            vertex = queue.pop(0)
            parentMetrics = []
            
            if vertex.getParent() is not None:
                parentMetrics = self.getVertex(vertex.getParent()).getMetrics()
                
            data.append([vertex.getFT(), vertex.getParent(), vertex.getMetrics(), parentMetrics, vertex.getOperator(), vertex.getGeneration()])
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    
        return data
    
    
    
    def get_last_generation(self):
        visited = set()
        queue = [self.root]
        visited.add(self.root)
        current_generation = []
        while queue:
            size = len(queue)
            current_generation = []
            while size:
                size -= 1
                vertex = queue.pop(0)
                current_generation.append(vertex)
                
                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        visited.add(neighbor)
                        
        return current_generation
                    

class Vertex:
    def __init__(self, ft, operator, parent, generation):
        self.ft = ft
        self.operator = operator
        self.metrics = []
        self.parent = parent
        self.generation = generation
        
    def setOperator(self, operator):
        self.operator = operator
        
    def setMetrics(self, metrics):
        self.metrics = metrics
        
    def getMetrics(self):
        return self.metrics
        
    def getOperator(self):
        return self.operator
    
    def getFT(self):
        return self.ft
    
    def getParent(self):
        return self.parent
    
    def getGeneration(self):
        return self.generation
        