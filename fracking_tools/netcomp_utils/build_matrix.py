import os
import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import re

class AdjacencyMatrix:
	def __init__(self, events_file, output_dir='.',  attributes=None):
		self.events_file = events_file.replace('\\', '/')
		self.output_file_name = self.events_file.replace('network_relationships', 'adjacency_matrix') #'/' + events_file.split('/')[-1].split('_')[0] + '_adjacency_matrix.csv'
		self.att_output_file_name = '/' + events_file.split('/')[-1].split(' ')[0] + 'attribute_adjacency_matrix.csv'
				
		self.out_dir = output_dir
		
		self.output_file = self.output_file_name.lower()
		self.att_output_file = self.out_dir + self.att_output_file_name.lower()
		
		self.attributes = attributes
			
	def build_network(self):
		self.network = nx.Graph()
		
		self.events = self.get_events()
		
		for e in self.events:
			for i in range(len(e)):
				for j in range(i + 1, len(e)):				
					actorA = ' '.join(re.findall(r'[aA0-zZ9]+', e[i]))
					actorB = ' '.join(re.findall(r'[aA0-zZ9]+', e[j]))
					
					self.network.add_edge(actorA, actorB)
		
		if self.attributes != None:
			
			with open(self.attributes, 'rb') as f:
				reader = csv.reader(f)
				
				all_rows = [row for row in reader]
				
				attribute_labels = [' '.join(i.split()).lower() for i in all_rows[0]][1:]
				actors = all_rows[1:]
				
				attributes = {}
				
				for actor in actors:
					name = actor[0]
					
					attributes[name] = {}
					
					for i in range(len(attribute_labels)):
						attributes[name][attribute_labels[i]] = actor[i + 1].lower()
					
			for node in attributes:
				for att in attributes[node]:
					if att.lower() == 'stance':
						
						
						stance = attributes[node][att]
						
						if stance == 'pro':
							# print "PRO"
							stance = 1
						elif stance == 'anti':
							stance = -1
							# print "ANTI"
							
						self.network.node[node][att] = stance
					else: 
						self.network.node[node][att] = attributes[node][att]

		self.labels = sorted(self.network.nodes())
		self.pos = nx.spring_layout(self.network)

		

	def get_events(self):		
		with open(self.events_file, 'rb') as f:
			reader = csv.reader(f, delimiter=',')
			
			events = [filter(None, list(col)[1:]) for col in zip(*reader)]
				
		return events
	
	def save_matrix(self):
		adj_mat_from_graph = nx.adjacency_matrix(self.network, nodelist=self.labels).todense() # ma
		
		adj_mat_from_graph = np.vstack([self.labels, adj_mat_from_graph])
		
		vertical_labels = [''] + self.labels
		
		rows = []
		
		for i in range(len(adj_mat_from_graph)):
			rows.append(np.insert(adj_mat_from_graph[i], 0, vertical_labels[i])[0])
		
		with open(self.output_file, 'wb') as f: 	
			writer = csv.writer(f, delimiter=',')
			
			for row in rows:
				writer.writerow(row.tolist()[0])
				
		return self.output_file
				
	def save_attr_matrix(self):
		
		self.add_attributes()
		
		adj_mat_from_graph = nx.attr_matrix(self.network, edge_attr='stance')[0]#, rc_order=self.network.nodes())
		
		labels = nx.attr_matrix(self.network, edge_attr='stance')[1]
		
		adj_mat_from_graph = np.vstack([labels, adj_mat_from_graph])
		
		vertical_labels = [''] + labels
		
		rows = []
		
		for i in range(len(adj_mat_from_graph)):
			rows.append(np.insert(adj_mat_from_graph[i], 0, vertical_labels[i])[0])
		
		with open(self.att_output_file, 'wb') as f: 	
			writer = csv.writer(f, delimiter=',')
			
			for row in rows:
				writer.writerow(row.tolist()[0])
	
	def add_attributes(self):
		all_nodes = self.network.nodes()

		
		for edge in self.network.edges():	
			node_A = edge[0]
			node_B = edge[1]
			
			self.network[node_A][node_B]['stance'] = int(self.network.node[node_A]['stance'])*int(self.network.node[node_B]['stance'])
		
	def run(self):
		self.build_network()
		matfile = self.save_matrix()
		
		if self.attributes != None: 
			self.save_attr_matrix()
		
		return matfile
# wd = r"D:\Dropbox\Fracking Networks Data Collection 2015\POLNET POSTER\MEETING MINUTES RELATIONSHIPS\Greenville done.csv"
# 
# adj = AdjacencyMatrix(wd, '.')
# adj.run()


