import ast
import pandas as pd

answers = []
with open("Actual/Codes/output_answer_easy.txt", "r", encoding="utf8") as file :
    answers_strings = file.readlines()
    for line in answers_strings:
        answer = ast.literal_eval(line)
        answers.append(answer)

df_guesses = pd.read_excel('Actual/Codes/guesses.xlsx')

id = 0
columns_answers = []
for word in answers:
    column = []
    column.append(id)
    id += 1
    answers_id = df_guesses.loc[df_guesses['guess'] == word[0]]
    column.append(answers_id.iloc[0]['id'])
    for guess in word[3]:
        guess_column = column.copy()
        guess_id = df_guesses.loc[df_guesses['guess'] == guess]
        guess_column.append(guess_id.iloc[0]['id'])
        guess_column.append(word[4][word[3].index(guess)])
        columns_answers.append(guess_column)

df_answer_guess_pair = pd.DataFrame(columns_answers, columns=['id', 'answer_id', 'guess_id', 'result'])

df_answer_guess_pair.to_excel('Actual/Codes/answer_guess_pairs.xlsx', index=False)