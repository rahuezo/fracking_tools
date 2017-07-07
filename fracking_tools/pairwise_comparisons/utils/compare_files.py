from get_cosine_similarity import get_cosine_similarity
from get_jaccard_sim import get_jaccard_similarity
import os


def compare_files(root_dir, file_pairs):
    output = []

    for pair in file_pairs:
        file_1, file_2 = pair[0].replace(' ', '_'), pair[1].replace(' ', '_')
        
        file_1_path = os.path.join(root_dir, file_1)
        file_2_path = os.path.join(root_dir, file_2)
        
        cosim = get_cosine_similarity(file_1_path, file_2_path)
        jasim = get_jaccard_similarity(file_1_path, file_2_path)
        
        print cosim, jasim
        
        if cosim > 0 and jasim > 0:
            output.append([file_1, file_2, cosim, jasim])

    return output

# print compare_files([['a.txt', 'b.txt']])

