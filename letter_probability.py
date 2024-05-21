import string

alphabet_keys = {}
for letter in string.ascii_lowercase:
    alphabet_keys[letter] = 0

print(alphabet_keys)

words = []
with open("words.txt", "r") as file :
    lines = file.readlines()
    for line in lines :
        line_words = line.split()
        words.extend(line_words)

for word in words:
    letters = [letter for letter in word]
    unique_letters = list(set(letters))
    for letter in unique_letters:
        alphabet_keys[letter] += 1

print(alphabet_keys)

with open('letter_prob.txt', 'w') as file:
    file.write(str(alphabet_keys) + '\n')
    for letter in alphabet_keys.keys():
        print(str(letter) + " : " + str(alphabet_keys[letter]/14855*100))
        file.write(str(letter) + " : " + str(alphabet_keys[letter]/14855*100) + '\n')

