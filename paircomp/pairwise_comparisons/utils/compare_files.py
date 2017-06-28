from get_cosine_similarity import get_cosine_similarity


def compare_files(root_dir, file_pairs):
    output = []

    for pair in file_pairs:
        file_1, file_2 = pair[0], pair[1]

        cosim = get_cosine_similarity(root_dir + '/' + file_1, root_dir + '/' + file_2)

        if cosim > 0:
            output.append([file_1, file_2, cosim])

    return output

# print compare_files([['a.txt', 'b.txt']])

