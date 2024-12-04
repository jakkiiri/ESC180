'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    top = 0
    bottom = 0
    for x in vec1.keys():
        if x in vec2.keys():
            top += vec1.get(x) * vec2.get(x)
    a = 0
    b = 0
    for x, y in zip(vec1.values(), vec2.values()):
        a += x**2
        b += y**2
    bottom = math.sqrt(a * b)
    return top / bottom

def build_semantic_descriptors(sentences):
    pass

def build_semantic_descriptors_from_files(filenames):
    pass



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    pass


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    pass
