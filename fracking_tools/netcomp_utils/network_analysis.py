import os
import csv
import time
import networkx as nx
import matplotlib.pyplot as plt

MM_NETWORK_ENV = "mm_network_directory"
N_NETWORK_ENV = "n_network_directory"

class NetworkComparison:
    def __init__(self, municipality, mm_file, n_file, wd='.'):
        f_1 = open(mm_file, 'r')
        f_2 = open(n_file, 'r')
        
        reader_1 = csv.reader(f_1) # handle csv file 1
        reader_2 = csv.reader(f_2) # handle csv file 2       
        
        self.working_directory = wd
        
        self.municipality = municipality.upper()
        
        self.mm_network = [row for row in reader_1] # read the contents of the mm network csv file
        self.n_network = [row for row in reader_2]  # read the contents of the n network csv file
        
        self.mm_hor_names = self.mm_network[0] # horizontal name list of mm network
        self.mm_ver_names = [i[0] for i in self.mm_network] # vertical name list of mm network
        
        self.n_hor_names = self.n_network[0] # horizontal name list of n network
        self.n_ver_names = [i[0] for i in self.n_network] # vertical name list of n network
        
        self.x_size_mm = len(self.mm_hor_names) # x size of mm network
        self.y_size_mm = len(self.mm_ver_names) # y size of mm network
        
        self.x_size_n = len(self.n_hor_names) # x size of n network
        self.y_size_n = len(self.n_ver_names) # y size of n network
        
        self.mm_wd = self.municipality + "_" + MM_NETWORK_ENV # mm working directory
        self.n_wd = self.municipality + "_" + N_NETWORK_ENV # n working directory
        
        # create the working directories
        
        try:
            os.mkdir(self.mm_wd)
            os.mkdir(self.n_wd)
            
            print "\nCreated {0} and {1}\n\n".format(self.mm_wd, self.n_wd)
        except:
            print "\nBoth directories exist!\n\n"
        
    def check_relationship(self):
        all_relationships_mm = [] # holds all the mm relationships
        all_relationships_n = [] # holds all the n relationships 
        
        all_no_relationships_mm = []
        all_no_relationships_n = []
        
        for row in range(self.x_size_mm)[1:]:
            single_person_relationship_mm = [] # holds the relationships of a single mm actor
            
            for col in range(self.y_size_mm)[1:]:
                element = self.mm_network[row][col] # holds the strength of the actor-specific relationship
                
                # only actors who are connected by some strength are considered to be related
                
                if element is not '':
                    single_person_relationship_mm.append({self.mm_hor_names[col].strip():element}) # a single actor has many relationships (person-rel_strength pairs)
                else:
                    all_no_relationships_mm.append(self.mm_hor_names[col].strip())
                    
            all_relationships_mm.append({self.mm_ver_names[row].strip():single_person_relationship_mm}) # holds all the mm network relationships
        
        for row in range(self.x_size_n)[1:]:
            single_person_relationship_n = [] # holds the relationships of a single n actor
            
            for col in range(self.y_size_n)[1:]:
                element = self.n_network[row][col] # holds the strength of the actor-specific relationship
                
                if element is not '':
                    single_person_relationship_n.append({self.n_hor_names[col].strip():element}) # a single actor has many relationships (person-rel_strength pairs)
                else:
                    all_no_relationships_n.append(self.n_hor_names[col].strip())
            all_relationships_n.append({self.n_ver_names[row].strip():single_person_relationship_n}) # holds all the n network relationships
            
        return all_relationships_mm, all_relationships_n, all_no_relationships_mm, all_no_relationships_n
    
    def beautify_relationships(self):
        all_relationships_mm = self.check_relationship()[0]
        all_relationships_n = self.check_relationship()[1]
        
        for mm_rel in all_relationships_mm:
            for main_person in mm_rel:
                main_person_file = open("{0}/{1}.txt".format(self.mm_wd, main_person), "w") # write mm_main_person person-relationship strength pairs
                
                main_person_relationships =  mm_rel[main_person]
                
                for relatives in main_person_relationships:
                    for relative in relatives:
                        main_person_file.write("{0} , {1}\n".format(relative, relatives[relative]))
            main_person_file.close()
            
        for n_rel in all_relationships_n:
            for main_person in n_rel:
                main_person_file = open("{0}/{1}.txt".format(self.n_wd, main_person), "w")
                
                main_person_relationships =  n_rel[main_person]
                
                for relatives in main_person_relationships:
                    for relative in relatives:
                        main_person_file.write("{0} , {1}\n".format(relative, relatives[relative]))
            main_person_file.close()
            
    def get_mm_n_network_actors_overlap(self):
        mm_actors = os.listdir(self.mm_wd)
        n_actors = os.listdir(self.n_wd)
        
        overlap_list = []
        
        for mm_actor in mm_actors:
            for n_actor in n_actors:
                if mm_actor == n_actor:
                    overlap_list.append(mm_actor.replace('.txt', ''))
                    print "{0} and {1} are in both networks".format(mm_actor, n_actor)
        return overlap_list
    
    def get_mm_n_network_relationship_overlap(self):
        mm_actors = os.listdir(self.mm_wd)
        n_actors = os.listdir(self.n_wd)
        
        mm_in_n_overlap = []
        
        for mm_actor in mm_actors:
            mm_actor_rels = open("{0}/{1}".format(self.mm_wd, mm_actor), "r").readlines()
            
            for n_actor in n_actors:
                n_actor_rels = open("{0}/{1}".format(self.n_wd, n_actor), "r").readlines()
        
                
                for mm_actor_rel in mm_actor_rels:
                    
                    if mm_actor_rel.split(',')[0].strip() in [i.split(',')[0].strip() for i in n_actor_rels]:
                        mm_rel_strength = int(mm_actor_rel.split(',')[1].strip())
                        
                        n_rel = [i for i in n_actor_rels if i.split(',')[0].strip() == mm_actor_rel.split(',')[0].strip()][0]
                        n_rel_strength = int(n_rel.split(',')[-1])
                        
                        if mm_rel_strength != n_rel_strength: 
                            mm_in_n_overlap.append("MM_{0} and N_{1} with {2} rel_strength = (MM {3} N {4})".format(mm_actor.replace('.txt', ''), n_actor.replace('.txt', ''), mm_actor_rel.split(',')[0].strip(), mm_rel_strength, n_rel_strength))
                            print "{0} and {1} both have {2} in common\n\n".format(mm_actor, n_actor, mm_actor_rel.split(',')[0].strip())
                        else:
                            mm_in_n_overlap.append("MM_{0} and N_{1} with {2}".format(mm_actor.replace('.txt', ''), n_actor.replace('.txt', ''), mm_actor_rel.split(',')[0].strip()))
                            print "{0} and {1} both have {2} in common\n\n".format(mm_actor, n_actor, mm_actor_rel.split(',')[0].strip())
                
        return mm_in_n_overlap
    
    def get_unique_mm_actors(self):
        mm_actors = os.listdir(self.mm_wd)
        n_actors = os.listdir(self.n_wd)
        
        unique_mm_actors = []
        
        for mm_actor in mm_actors:
            if mm_actor not in n_actors:
                unique_mm_actors.append(mm_actor.replace('.txt', ''))
        return unique_mm_actors
    
    def get_unique_n_actors(self):
        mm_actors = os.listdir(self.mm_wd)
        n_actors = os.listdir(self.n_wd)
        
        unique_n_actors = []
        
        for n_actor in n_actors:
            if n_actor not in mm_actors:
                unique_n_actors.append(n_actor.replace('.txt', ''))
        
        return unique_n_actors
    
    def get_unique_mm_relationships(self):
        mm_actors = os.listdir(self.mm_wd)
        n_actors = os.listdir(self.n_wd)
        
        unique_mm_relationships = []
        
        for mm_actor in mm_actors:
            mm_actor_rels = open("{0}/{1}".format(self.mm_wd, mm_actor), "r").readlines()
            
            for n_actor in n_actors:
                n_actor_rels = open("{0}/{1}".format(self.n_wd, n_actor), "r").readlines()
        
                for mm_actor_rel in mm_actor_rels:
                    if mm_actor_rel.split(',')[0].strip() not in [i.split(',')[0].strip() for i in n_actor_rels]:
                        #unique_mm_relationships.append(mm_actor_rel)
                        unique_mm_relationships.append("{0} and {1}".format(mm_actor.replace('.txt', ''), mm_actor_rel))
                        
        #print unique_mm_relationships
                        #print "{0} and {1} both have {2} in common\n\n".format(mm_actor, n_actor, mm_actor_rel.split(',')[0].strip())
        return list(set(unique_mm_relationships))
        
    
    def get_unique_n_relationships(self):
        mm_actors = os.listdir(self.mm_wd)
        n_actors = os.listdir(self.n_wd)
        
        unique_n_relationships = []
        
        for mm_actor in mm_actors:
            mm_actor_rels = open("{0}/{1}".format(self.mm_wd, mm_actor), "r").readlines()
            
            for n_actor in n_actors:
                n_actor_rels = open("{0}/{1}".format(self.n_wd, n_actor), "r").readlines()
        
                for n_actor_rel in n_actor_rels:
                    if n_actor_rel.split(',')[0].strip() not in [i.split(',')[0].strip() for i in mm_actor_rels]:
                        #unique_n_relationships.append(n_actor_rel)
                        unique_n_relationships.append("{0} and {1}".format(n_actor.replace('.txt', ''), n_actor_rel))
                        
        return list(set(unique_n_relationships))
    
    def comparison_summary(self):

        # get overlapping actors
        
        file_name = self.working_directory + '/' + self.municipality.strip() + " -- MM and N Network Comparison Summary.csv"
        summary_file = open(file_name, 'wb')
        
        summary_file.write("MM and N Actor Overlap,MM and N Relationship Overlap,Unique MM Actors,Unique N Actors,Unique MM Relationships,Unique N Relationships\n")
        
        self.beautify_relationships()
        
        mm_n_actors_overlap = self.get_mm_n_network_actors_overlap()
        mm_n_relationships_overlap = self.get_mm_n_network_relationship_overlap()
        mm_unique_actors = self.get_unique_mm_actors()
        n_unique_actors = self.get_unique_n_actors()
        mm_unique_relationships = self.get_unique_mm_relationships()
        n_unique_relationships = self.get_unique_n_relationships()
        
        max_size = max([len(mm_n_actors_overlap), len(mm_n_relationships_overlap), len(mm_unique_actors), len(n_unique_actors), len(mm_unique_relationships), len(n_unique_relationships)])
        
        items = [mm_n_actors_overlap, mm_n_relationships_overlap, mm_unique_actors, n_unique_actors, mm_unique_relationships, n_unique_relationships]
        new_items = []
        
        
        for item in items:
            if len(item) < max_size:
                diff = max_size - len(item)
                spacer = ['' for i in range(diff)]
                new_items.append(item + spacer)
                
            else:
                new_items.append(item)
                        
        for i in range(max_size):
            summary_file.write("{0},{1},{2},{3},{4},{5}\n".format(new_items[0][i].replace(',',' with strength ').replace('\n', ''), new_items[1][i].replace(',',' with strength ').replace('\n', ''),
                                                                  new_items[2][i].replace(',',' with strength ').replace('\n', ''), new_items[3][i].replace(',',' with strength ').replace('\n', ''),
                                                                  new_items[4][i].replace(',',' with strength ').replace('\n', ''), new_items[5][i].replace(',',' with strength ').replace('\n', '')))
        summary_file.close()
        return file_name
        
    def visualize_comparison(self):
        try:
            mm_actors = os.listdir(self.mm_wd)
            n_actors = os.listdir(self.n_wd)
            
            mm_nodes = []
            mm_edges = []
            
            for mm_actor in mm_actors:
                relatives = [i.split(',')[0].strip() for i in open("{0}/{1}".format(self.mm_wd, mm_actor))]
                
                
                mm_nodes.append(mm_actor.split('.')[0])
                
                for rel in relatives:
                    mm_nodes.append(rel)
                some_edges = [(mm_actor.split('.')[0], i) for i in relatives]
                
                for edge in some_edges:
                    mm_edges.append(edge)
                    
            for loner in self.check_relationship()[2]:                 
                mm_nodes.append(loner)
            
            g = nx.Graph()
            g.add_nodes_from(mm_nodes)
            g.add_edges_from(mm_edges)
            
            
            nx.draw_spring(g, node_size=100, with_labels=False, node_color='r', alpha=0.8, label='MM Network')
            
            n_nodes = []
            n_edges = []
            
            
            for n_actor in n_actors:
                relatives = [i.split(',')[0].strip() for i in open("{0}/{1}".format(self.n_wd, n_actor))]
                
                n_nodes.append(n_actor.split('.')[0].decode('utf8').encode('ascii', 'ignore'))
                
                for rel in relatives:
                    n_nodes.append(rel)
                some_edges = [(n_actor.split('.')[0].decode('utf8').encode('ascii', 'ignore'), i) for i in relatives]
                
                for edge in some_edges:
                    n_edges.append(edge)
                    
            for loner in self.check_relationship()[3]:                 
                n_nodes.append(loner)
                
            nodes = mm_nodes + n_nodes
            edges = mm_edges + n_edges
            
            g = nx.Graph()
            g.add_nodes_from(n_nodes)
            g.add_edges_from(n_edges)
            
            nx.draw_spring(g, node_size=100, with_labels=False, node_color='b', alpha=0.8, label='N Network')
            
            plt.title("MM {0} vs. N {1}\n".format(self.municipality.strip(), self.municipality.strip()))
            # plt.legend()
            plt.savefig('images/N_' + self.municipality + '.png', dpi=1000)
            
            plt.show()
            
        except Exception, e:
            print e
            print mm_actor.split('.')[0]
            print n_actor.split('.')[0]
        
# muni_name = raw_input("Enter Municipality Name: ")
# files_input = raw_input("Enter File Names (separated by commas): ")
# 
# files = (files_input.split(',')[0], files_input.split(',')[1])
# network = NetworkComparison(muni_name, *files )
# network.comparison_summary()
# network.visualize_comparison()
    
    