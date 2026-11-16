import streamlit as st 

def replace_cost(x, y):
    if x == y:
        return 0 
    return 1

def levenshtein_distance(word: str, target: str):
    n, m = len(word), len(target)
    distance = [[0] * (n+1) for _ in range(m+1)]

    for i in range(n+1):
        distance[0][i] = i
    for i in range(m+1):
        distance[i][0] = i

    
    for i in range(1, m+1):
        for j in range(1, n+1): 
            distance[i][j] = min(
                distance[i][j-1] + 1, distance[i-1][j] + 1,
                distance[i-1][j-1] + replace_cost(word[j-1], target[i-1])
            )

    return distance[-1][-1]

def suggest_word(word: str, filepath: str):
    file = open(filepath, "r")
    vocab = file.read().split('\n')
    vocab_size = len(vocab)
    result = ""
    min_distance = 2**31

    for i in range(vocab_size):
        distance = levenshtein_distance(word, vocab[i])
        if distance < min_distance:
            min_distance = distance
            result = vocab[i]

    return result


path = "words_alpha.txt"


st.title("Simple word correction")

user_input = st.text_input("Type your word")
prediction = suggest_word(user_input,path)
with st.echo():
    st.write(f"Suggested correction: {prediction}")


