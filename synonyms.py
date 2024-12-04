import math

def norm(vec):
    sum_of_squares = sum(value * value for value in vec.values())
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
    for sentence in sentences:
        unique_words = []
        for word in sentence:
            if word.lower() not in unique_words:
                unique_words.append(word.lower())
        
        for i, word in enumerate(unique_words):
            if word not in descriptors:
                descriptors[word] = {}
            
            for other_word in unique_words:
                if other_word != word:
                    descriptors[word][other_word] = descriptors[word].get(other_word, 0) + 1
    
    return descriptors

def build_semantic_descriptors_from_files(filenames):
    all_sentences = []
    sentence_endings = '.!?'
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as file:
            text = file.read().lower()
            for char in sentence_endings:
                text = text.replace(char, '.')
            sentences = text.split('.')
            for sentence in sentences:
                cleaned_sentence = ''
                i = 0
                while i < len(sentence):
                    char = sentence[i]
                    if char.isalnum() or char.isspace():
                        cleaned_sentence += char
                    elif char == "'":
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
                words = [word for word in cleaned_sentence.split() if word]
                if words:
                    all_sentences.append(words)
    return build_semantic_descriptors(all_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
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
            similarity = -1
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar = choice
    return most_similar

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
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
