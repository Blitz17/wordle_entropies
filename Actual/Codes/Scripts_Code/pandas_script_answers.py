import ast
import pandas as pd

answers = []
with open("Actual/Codes/Data_Code/output_answer_easy.txt", "r", encoding="utf8") as file :
    answers_strings = file.readlines()
    for line in answers_strings:
        answer = ast.literal_eval(line)
        answers.append(answer)

df_top_25 = pd.read_excel('Actual/Codes/top_25.xlsx')

id = 0
columns_answers = []
for word in answers:
    column = []
    column.append(id)
    id += 1
    column.append(word[0])
    top_25_word = word[3][0]
    top_25_id = df_top_25.loc[df_top_25['top_25_word'] == top_25_word]
    column.append(top_25_id.iloc[0]['id'])
    column.append(word[1])
    column.append(word[2])
    columns_answers.append(column)

df_answers = pd.DataFrame(columns_answers, columns=['id', 'answer', 'top_25_id', 'steps_to_guess', 'solved_flag'])

df_answers.to_excel('Actual/Codes/answers.xlsx', index=False)