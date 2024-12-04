'''Semantic Similarity: corrected code without using re

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary.'''
    sum_of_squares = sum(value * value for value in vec.values())
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    '''Compute the cosine similarity between two vectors stored as dictionaries.'''
    top = sum(vec1.get(key, 0) * vec2.get(key, 0) for key in vec1)
    norm1 = norm(vec1)
    norm2 = norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return -1  # Handle zero-vector cases
    return top / (norm1 * norm2)

def build_semantic_descriptors(sentences):
    '''Build semantic descriptors from a list of sentences.'''
    descriptors = {}
    for sentence in sentences:
        unique_words = set(word.lower() for word in sentence)
        for word in unique_words:
            if word not in descriptors:
                descriptors[word] = {}
            for other_word in unique_words:
                if other_word != word:
                    descriptors[word][other_word] = descriptors[word].get(other_word, 0) + 1
    return descriptors

def build_semantic_descriptors_from_files(filenames):
    '''Build semantic descriptors from text files without using re.'''
    all_sentences = []
    sentence_endings = '.!?'
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as file:
            text = file.read().lower()
            # Replace sentence-ending punctuation with periods
            for char in sentence_endings:
                text = text.replace(char, '.')
            # Split into sentences
            sentences = text.split('.')
            for sentence in sentences:
                # Process the sentence to remove unwanted punctuation
                cleaned_sentence = ''
                i = 0
                while i < len(sentence):
                    char = sentence[i]
                    if char.isalnum() or char.isspace():
                        cleaned_sentence += char
                    elif char == "'":
                        # Keep apostrophes between alphanumeric characters (e.g., don't, Isaac's)
                        if i > 0 and i < len(sentence) - 1:
                            prev_char = sentence[i - 1]
                            next_char = sentence[i + 1]
                            if prev_char.isalnum() and next_char.isalnum():
                                cleaned_sentence += char
                            else:
                                cleaned_sentence += ' '
                        else:
                            cleaned_sentence += ' '
                    else:
                        cleaned_sentence += ' '
                    i += 1
                # Split into words and filter out empty strings
                words = [word for word in cleaned_sentence.split() if word]
                if words:
                    all_sentences.append(words)
    return build_semantic_descriptors(all_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''Find the most semantically similar word from choices to the given word.'''
    word = word.lower()
    choices = [choice.lower() for choice in choices]
    if word not in semantic_descriptors:
        return choices[0]
    max_similarity = float('-inf')
    most_similar = choices[0]
    for choice in choices:
        if choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        else:
            similarity = -1  # Handle cases where the choice is not in descriptors
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = choice
    return most_similar

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''Run a semantic similarity test and return the percentage of correct answers.'''
    correct = 0
    total = 0
    with open(filename, "r", encoding="latin1") as file:
        for line in file:
            words = line.strip().lower().split()
            if len(words) >= 3:
                word, correct_answer = words[0], words[1]
                choices = words[2:]
                answer = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
                if answer == correct_answer:
                    correct += 1
                total += 1
    return (correct / total) * 100 if total > 0 else 0
