import ast
import pandas as pd

with open("Actual/Codes/answer_entropies.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

x = ast.literal_eval(lines[0])
list = sorted(x.items(), key=lambda item: item[1], reverse=True)

top_25 = list[0:25]

df_guesses = pd.read_excel('Actual/Codes/guesses.xlsx')

id = 0
columns_top_25 = []
for word, entropy in top_25:
    column = []
    column.append(id)
    id += 1
    column.append(word)
    guess_id = df_guesses.loc[df_guesses['guess'] == word]
    column.append(guess_id.iloc[0]['id'])
    column.append(entropy)
    columns_top_25.append(column)

df_top_25 = pd.DataFrame(columns_top_25, columns=['id', 'top_25_word', 'guess_id', 'intial_entropy'])

print(df_top_25)

df_top_25.to_excel('Actual/Codes/top_25.xlsx', index=False)