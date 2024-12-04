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
    descriptors = {}
    
    # Process each sentence
    for sentence in sentences:
        # Convert words to lowercase and create a set to avoid counting duplicates
        unique_words = []
        for word in sentence:
            if word.lower() not in unique_words:
                unique_words.append(word.lower())
        
        # For each word in the sentence
        for i, word in enumerate(unique_words):
            # Initialize word's descriptor if not already present
            if word not in descriptors:
                descriptors[word] = {}
            
            # Count co-occurrences with other words in same sentence
            for other_word in unique_words:
                if other_word != word:
                    descriptors[word][other_word] = descriptors[word].get(other_word, 0) + 1
    
    return descriptors

def build_semantic_descriptors_from_files(filenames):
    all_sentences = []
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as file:
            # Read file and convert to lowercase
            text = file.read().lower()
            
            # Replace sentence-ending punctuation with periods
            for char in "!?;":
                text = text.replace(char, ".")
                
            # Split into sentences
            sentences = [s.strip() for s in text.split(".")]
            
            for sentence in sentences:
                # Remove all punctuation from words except apostrophes within words
                cleaned_sentence = ""
                for i, char in enumerate(sentence):
                    # Keep apostrophes that are between letters (contractions)
                    if char == "'" and i > 0 and i < len(sentence)-1 and \
                       sentence[i-1].isalnum() and sentence[i+1].isalnum():
                        cleaned_sentence += char
                    # Keep alphanumeric characters and spaces
                    elif char.isalnum() or char.isspace():
                        cleaned_sentence += char
                    # Replace other punctuation with spaces
                    else:
                        cleaned_sentence += " "
                
                # Split into words and filter out empty strings
                words = [word for word in cleaned_sentence.split() if word]
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
