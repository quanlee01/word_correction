import streamlit as st 

def levenshtein_distance(word: str, target: str) -> int:
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
                distance[i-1][j-1] + int(not (word[j-1] == target[i-1]))
            )

    return distance[-1][-1]


def suggest_word(word: str, filepath: str) -> str:
    with open(filepath, "r") as file:
        vocab = file.read().splitlines()
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
if user_input != "":
    prediction = suggest_word(user_input, path)
else:
    prediction = ""
st.write(f"Suggested correction: {prediction}")


