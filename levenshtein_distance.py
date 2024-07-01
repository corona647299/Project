import streamlit as st


def levenshtein_distance(word, vocab):
    distances = [[0]*(len(vocab)+1) for _ in range(len(word)+1)]

    for t1 in range(len(word) + 1):
        distances[t1][0] = t1

    for t2 in range(len(vocab) + 1):
        distances[0][t2] = t2
    a = 0
    b = 0
    c = 0
    for t1 in range(1, len(word) + 1):
        for t2 in range(1, len(vocab) + 1):
            if (word[t1-1] == vocab[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    return distances[len(word)][len(vocab)]


st.title('Word Correction Using Levenshtein Distance')
word = st.text_input('Input your word: ')


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(file_path=r'D:\Project\vocab.txt')

if st.button("compute"):
    distances = dict()
    for vocab in vocabs:
        distance = levenshtein_distance(word, vocab)
        distances[vocab] = distance
    sorted_distances = dict(
        sorted(distances.items(), key=lambda item: item[1]))
    correct_word = list(sorted_distances.keys())[0]
    st.write("correct: ", correct_word)
    
    col1, col2 = st.columns(2)
    col1.write(vocabs)
    
    col2.write(sorted_distances)
