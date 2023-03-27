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
