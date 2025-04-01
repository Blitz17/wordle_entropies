import ast
import pandas as pd

answers = []
with open("Actual/Codes/Data_Code/output_answer_easy.txt", "r", encoding="utf8") as file :
    answers_strings = file.readlines()
    for line in answers_strings:
        answer = ast.literal_eval(line)
        answers.append(answer)

df_guesses = pd.read_excel('Actual/Codes/guesses.xlsx')

id = 0
columns_answers = []
for word in answers:
    column = []
    for guess in word[3]:
        column = []
        column.append(id)
        answers_id = df_guesses.loc[df_guesses['guess'] == word[0]]
        column.append(answers_id.iloc[0]['id'])
        guess_id = df_guesses.loc[df_guesses['guess'] == guess]
        column.append(guess_id.iloc[0]['id'])
        column.append(word[4][word[3].index(guess)])
        id += 1
        columns_answers.append(column)

df_answer_guess_pair = pd.DataFrame(columns_answers, columns=['id', 'answer_id', 'guess_id', 'result'])

df_answer_guess_pair.to_excel('Actual/Codes/answer_guess_pairs.xlsx', index=False)