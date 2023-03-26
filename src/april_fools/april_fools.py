import pandas as pd
import random


def create_anagrams(response):
    words = response.split(" ")
    anagrammed_response = []
    punctionation_to_be_exclued = [".", ",", "!", "?", ":", ";", "(", ")"]
    for word in words:
        anagram = ""
        punc_to_replace = {}
        for i, char in enumerate(word):
            if char in punctionation_to_be_exclued:
                punc_to_replace[i] = char
                word = word.replace(char, "")

        while len(word) > 0:
            word = list(word)
            anagram += word.pop(random.randint(0, len(word) - 1))

        for i in punc_to_replace:  # works b/c indices are ordered
            anagram = anagram[:i] + punc_to_replace[i] + anagram[i:]
        anagrammed_response.append(anagram)

    return " ".join(anagrammed_response)

# csv_path = "./data/jersey_devil_S23.csv"
# df = pd.read_csv(csv_path)
# secrets = df[df['Email Address'] == "kavyaa@mit.edu"]

# # print(secrets)
# # for secret in secrets:
#     # print(secrets[secret].item())

# print(secrets["what about your favorite fruit (possibly dehydrated??) "].item())

# print(create_anagrams(secrets["what about your favorite fruit (possibly dehydrated??) "].item()))

# sent = "!!hi this is a test... a test for all the (punctuation) that people may or may not use??? in their responses!!"
# print(sent)
# print(create_anagrams(sent))
