import ast
import pandas as pd

answers = []
with open("Actual/Codes/output_answer_easy.txt", "r", encoding="utf8") as file :
    answers_strings = file.readlines()
    for line in answers_strings:
        answer = ast.literal_eval(line)
        answers.append(answer)

df_answer_guess_pair = pd.read_excel('Actual/Codes/answer_guess_pairs.xlsx')
df_guesses = pd.read_excel('Actual/Codes/guesses.xlsx')

id = 0
columns_answers = []
for word in answers:
    column = []
    step = 1
    answer = word[0]
    for guess in word[3]:
        column = []
        column.append(id)
        column.append(step)
        guess_id = df_guesses.loc[df_guesses['guess'] == guess].iloc[0]['id']
        answer_id = df_guesses.loc[df_guesses['guess'] == answer].iloc[0]['id']
        answer_guess_pair_id = df_answer_guess_pair.loc[(df_answer_guess_pair['answer_id'] == answer_id) & (df_answer_guess_pair['guess_id'] == guess_id)].iloc[0]['id']
        column.append(answer_guess_pair_id)
        column.append(word[7][step - 1])
        column.append(word[5][step - 1])
        column.append(word[6][step - 1])
        id += 1
        step += 1
        columns_answers.append(column)


df_tarse_table = pd.DataFrame(columns_answers, columns=['id', 'step_number', 'answer_guess_pair_id', 'guess_entropy', 'possible_answers', 'remaining_answers'])

df_tarse_table.to_excel('Actual/Codes/tarse_table.xlsx', index=False)