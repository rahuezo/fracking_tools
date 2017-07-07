from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_cosine_similarity(file_1, file_2):
    try:
        with open(file_1, 'r') as text_1, open(file_2, 'r') as text_2:
            documents = (text_1.read(), text_2.read())

            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

            cosim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0][-1]

        return round(cosim, 4)

    except IOError as msg:
        print msg
        return -1
