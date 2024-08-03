from collections import Counter
import ast
import re

with open("answers.txt", "r", encoding='utf8') as file :
    lines = file.readlines()
    for line in lines:
        if len(list(enumerate(line))) > 6:
            print(list(enumerate(line)))
    
