SHINGLE_SIZE = 3


def get_shingles(f, size):
    
    with open(f, 'r') as fh: 
        buff = fh.read()
    
        for i in range(0, len(buff)-size+1):
            output = buff[i:i + size]
            yield output

     
def compute_jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    
    return x / float(y)


def get_jaccard_similarity(file_1, file_2):
    try:
        shingles_1 = set(get_shingles(file_1, size=SHINGLE_SIZE))
        shingles_2 = set(get_shingles(file_2, size=SHINGLE_SIZE))
        
        jasim = compute_jaccard(shingles_1, shingles_2)

        return round(jasim, 4)

    except IOError as msg:
        print msg
        return -1