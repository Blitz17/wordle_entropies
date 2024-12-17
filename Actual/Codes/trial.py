import ast

with open("output_answer_hard.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

sum = 0
count = 0
for line in lines:
    line_list = ast.literal_eval(line)
    if line_list[2] == 1:
        sum += line_list[1]
        count += 1

print(sum)
print(count)
print(sum/count)