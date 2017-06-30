from build_matrix import AdjacencyMatrix
import tkFileDialog as fd
import csv


def get_edges():
    events_file = fd.askopenfilename(title="Choose Relationships File")
    
    adMat = AdjacencyMatrix(events_file)
    
    adMat.build_network()
    
    network = adMat.network
    
    return (network.edges(), events_file)


def save_edges_to_file(edges):
    edges_filename = edges[1].split('/')[-1].replace('network_relationships', 'node_pairs')
    
    header = ['Node A', 'Node B']
    
    with open(edges_filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
        for edge in edges[0]:
            writer.writerow(list(edge))
    
    
edges = get_edges()#'IASC network_relationships.csv')

save_edges_to_file(edges)
