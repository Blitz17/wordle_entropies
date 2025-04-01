from collections import Counter
import ast
import re
import pandas as pd

entropies = ""
case_counters = ""
guesses = []
answers = []
with open("Actual/Codes/Data_Code/answer_entropies.txt", "r", encoding="utf8") as file :
    entropies = file.readline()
    entropies = ast.literal_eval(entropies)

with open("Actual/Codes/Data_Code/answer_cases.txt", "r", encoding="utf8") as file :
    lines = file.readlines()
    counter_pattern = re.compile(r"Counter\((\{.*?\})\)")
    modified_string = counter_pattern.sub(r'\1', lines[0])
    cases = ast.literal_eval(modified_string)
    case_counters = {key: Counter(value) for key, value in cases.items()}

with open("Actual/Codes/Data_Code/words.txt", "r", encoding="utf8") as file :
    words = file.readlines()
    for word in words : 
        line_words = word.split()
        guesses.extend(line_words)

with open("Actual/Codes/Data_Code/answers.txt", "r", encoding="utf8") as file :
    words = file.readlines()
    for word in words : 
        line_words = word.split()
        answers.extend(line_words)

guesses.sort()

id = 0
columns_guesses = []
for word in guesses:
    column = []
    column.append(id)
    id += 1
    column.append(word)
    column.append(entropies[word])
    column.append(case_counters[word])
    if word in answers :
        column.append(1)
    else :
        column.append(0)
    columns_guesses.append(column)

df_guesses = pd.DataFrame(columns_guesses, columns=['id', 'guess', 'initial_entropy', 'intial_counter', 'is_answer_flag'])

df_guesses.to_excel('Actual/Codes/guesses.xlsx', index=False)