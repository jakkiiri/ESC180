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
    # Initialize dictionary to store semantic descriptors
    descriptors = {}
    
    # Process each sentence
    for sentence in sentences:
        # Convert words to lowercase and create a set to avoid counting duplicates
        words = set(word.lower() for word in sentence)
        
        # For each word in the sentence
        for word in words:
            # Initialize word's descriptor if not already present
            if word not in descriptors:
                descriptors[word] = {}
            
            # Count co-occurrences with other words in same sentence
            for other_word in words:
                if other_word != word:
                    if other_word not in descriptors[word]:
                        descriptors[word][other_word] = 1
                    else:
                        descriptors[word][other_word] += 1
    
    return descriptors

def build_semantic_descriptors_from_files(filenames):
    all_sentences = []
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as file:
            # Read file and replace punctuation with periods
            text = file.read().lower()
            for char in "!?;":
                text = text.replace(char, ".")
            
            # Split into sentences and clean up
            sentences = text.split(".")
            for sentence in sentences:
                # Split sentence into words and remove punctuation
                words = [word.strip(",:;!?()[]{}\"'") for word in sentence.split()]
                # Only add non-empty word lists
                if words:
                    all_sentences.append(words)
    
    return build_semantic_descriptors(all_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]
    
    max_similarity = float('-inf')
    most_similar = choices[0]
    
    for choice in choices:
        if choice not in semantic_descriptors:
            similarity = -1
        else:
            similarity = similarity_fn(semantic_descriptors[word], 
                                    semantic_descriptors[choice])
        
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = choice
    
    return most_similar

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    total = 0
    
    with open(filename, "r") as file:
        for line in file:
            # Split line into words and strip whitespace
            words = line.strip().split()
            if len(words) >= 3:  # Ensure valid test case
                word, correct_answer = words[0], words[1]
                choices = words[2:]
                
                # Run test and check if answer matches
                answer = most_similar_word(word, choices, 
                                        semantic_descriptors, similarity_fn)
                if answer == correct_answer:
                    correct += 1
                total += 1
    
    return (correct / total) * 100 if total > 0 else 0
