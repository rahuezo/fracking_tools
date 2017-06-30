import networkx as nx
import matplotlib.pyplot as plt
import csv
from matrix_to_network import *

class NetworkComparisonSingle:
    def __init__(self, municipality, networkA, networkB, wd='.'):
        self.working_directory = wd
        self.municipality = municipality
            
        self.networkA = matrix_to_network(networkA)
        self.networkB = matrix_to_network(networkB)
        
    def get_AB_actor_overlap(self):
        actorsA = [' '.join(node.split()) for node in self.networkA.nodes()]
        actorsB = [' '.join(node.split()) for node in self.networkB.nodes()]
        
        self.AB_actor_overlap = list(set(actorsA) & set(actorsB))
        
        return self.AB_actor_overlap
    
    def get_AB_relationship_overlap(self):
        relationshipsA = self.networkA.edges() # [sorted(edge) for edge in self.networkA.edges()]
        relationshipsB = self.networkB.edges() # [sorted(edge) for edge in self.networkB.edges()]
        
        self.AB_relationship_overlap = list(set(relationshipsA) & set(relationshipsB))
        
        return self.AB_relationship_overlap
    
    def get_unique_relationships(self):
        relationshipsA = self.networkA.edges()
        relationshipsB = self.networkB.edges()
        
        self.uniqueA_relationships = [rel for rel in relationshipsA if rel not in relationshipsB]
        self.uniqueB_relationships = [rel for rel in relationshipsB if rel not in relationshipsA]
        
        return [self.uniqueA_relationships, self.uniqueB_relationships]
    
    def get_unique_actors(self):
        actorsA = self.networkA.nodes()
        actorsB = self.networkB.nodes()
        
        self.uniqueA_actors = [actor for actor in actorsA if actor not in actorsB]
        self.uniqueB_actors = [actor for actor in actorsB if actor not in actorsA]
        
        return [self.uniqueA_actors, self.uniqueB_actors]
    
    def get_comparison_summary(self):
        comparison_file_name = self.working_directory + '/' + self.municipality.strip() + " -- MM and N Network Comparison Summary.csv"
        
        header = ["MM and N Actor Overlap", "MM and N Relationship Overlap", "Unique MM Actors", "Unique N Actors", "Unique MM Relationships", "Unique N Relationships"]
        
        AB_actor_overlap = self.get_AB_actor_overlap()
        AB_relationship_overlap = self.get_AB_relationship_overlap()
        
        uniqueA_actors, uniqueB_actors = self.get_unique_actors()
        uniqueA_relationships, uniqueB_relationships = self.get_unique_relationships()
        
        max_size = max([len(AB_actor_overlap), len(AB_relationship_overlap), len(uniqueA_actors), len(uniqueB_actors),
                        len(uniqueA_relationships), len(uniqueB_relationships)])
        
        AB_actor_overlap = self.add_spaces(AB_actor_overlap, max_size)
        AB_relationship_overlap = self.add_spaces(AB_relationship_overlap, max_size)
        
        uniqueA_actors = self.add_spaces(uniqueA_actors, max_size)
        uniqueB_actors = self.add_spaces(uniqueB_actors, max_size)
        
        uniqueA_relationships = self.add_spaces(uniqueA_relationships, max_size)
        uniqueB_relationships = self.add_spaces(uniqueB_relationships, max_size)
        
        
        with open(comparison_file_name, "wb") as comparison_file:
            writer = csv.writer(comparison_file, delimiter=',')
            
            writer.writerow(header)
            
            for i in range(max_size):
                
                row = [AB_actor_overlap[i], AB_relationship_overlap[i], uniqueA_actors[i], uniqueB_actors[i],
                       uniqueA_relationships[i], uniqueB_relationships[i]]
                
                writer.writerow(row)
            
            
    def add_spaces(self, source, target_size):
        if len(source) < target_size:
            spaces = ['' for i in range(target_size - len(source))]
            
            return source + spaces        
        else:
            return source

