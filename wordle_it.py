from collections import Counter
import ast
import re

with open("answer_cases.txt", "r") as file :
    lines = file.readlines()
    print(type(lines[0]))
    counter_pattern = re.compile(r"Counter\((\{.*?\})\)")
    modified_string = counter_pattern.sub(r'\1', lines[0])
    cases = ast.literal_eval(modified_string)
    print(type(cases))
    cases = {key: Counter(value) for key, value in cases.items()}
    print(type(cases))

print(len(cases.keys()))
print(len(cases.values()))