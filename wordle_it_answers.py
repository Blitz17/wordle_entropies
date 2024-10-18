from collections import Counter
import ast
import re
from wordle_classes import *

all_words = []
with open("words.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

    for line in lines :
        line_words = line.split()
        all_words.extend(line_words)

answers = []
with open("answers.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

    for line in lines :
        line_words = line.split()
        answers.extend(line_words)

with open("answer_cases.txt", "r") as file :
    lines = file.readlines()
    counter_pattern = re.compile(r"Counter\((\{.*?\})\)")
    modified_string = counter_pattern.sub(r'\1', lines[0])
    cases = ast.literal_eval(modified_string)
    main_cases = {key: Counter(value) for key, value in cases.items()}

with open('answer_entropies.txt', 'r') as file:
    lines = file.readlines()
    entropies = ast.literal_eval(lines[0])
    
best_word = max(entropies, key=entropies.get)

Dhanush = WordleBot()
Dhanush.simulate_play(answers, all_words, best_word)