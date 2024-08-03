import numpy as np 
from tqdm import tqdm
from collections import Counter
from more_itertools import partition, flatten, chunked
import ast
import re
from functools import lru_cache

class State :
    in_progress = 0
    win = 1
    loss = -1


class letter_result :
    grey = -1
    yellow = 0
    green = 1


class Wordle :
    max_guesses = 0
    guesses = []
    answer = ""
    all_words = []
    
    def create(self, all_words, max_guesses = 6, answer = "cream") :
        self.answer = answer
        self.all_words = all_words.copy()
        self.guesses = []
        self.max_guesses = max_guesses
        return self

    def state(self) :
        if self.answer in self.guesses :
            return State.win
        elif len(self.guesses) >= self.max_guesses : 
            return State.loss
        else :
            return State.in_progress
    
    def guess(self, guess) :
        results = [letter_result.grey] * len(guess)
        answer_letter_count = {}   

        for i in range(len(guess)):
            if guess[i] == self.answer[i]:
                results[i] = letter_result.green
            else:
                if self.answer[i] in answer_letter_count:
                    answer_letter_count[self.answer[i]] += 1
                else:
                    answer_letter_count[self.answer[i]] = 1
        
        for i in range(len(guess)):
            if results[i] != letter_result.green:  # Only check non-green letters
                if guess[i] in answer_letter_count and answer_letter_count[guess[i]] > 0:
                    results[i] = letter_result.yellow
                    answer_letter_count[guess[i]] -= 1
        
        self.guesses.append(guess)
        word_information = []

        for (position, letter) in enumerate(guess) : 
            word_information.append([position, letter, results[position]])
        
        return word_information


class Strategy :
    correct_letters = set()
    possible_letters = []
    all_words = []
    answers = []
    current_guess = ""

    def create(self, possible_words, all_words) :
        self.correct_letters = set()
        self.possible_letters = [set("abcdefghijklmnopqrstuvwxyz").copy() for i in range(5)]
        self.all_words = all_words
        self.answers = possible_words
        return self

    def joint_entropy(self, word, counted_results):
        entropy = 0
        total_words = sum(counted_results[word].values())

        for result, counts in counted_results[word].items():
            p = (counts / total_words)
            entropy -= p * np.log(p)

        return entropy

    def generate_cases(self, possible_words, answers):
        cases = {}
        status = 0

        for guess_word in possible_words:
            all_results = []
            status += 1

            for hidden_word in answers:
                result = []
                case = Wordle().create(list(possible_words), 6, hidden_word).guess(guess_word) 
                for letter in case:                        
                    result.append(letter[2])
                all_results.append(''.join(map(str, result)))

            cases[guess_word] = Counter(all_results)  
            print(status)
            
        return cases

    def update(self, updates) :
        for position, letter, result in updates :
            if result == letter_result.grey : 
                if letter in self.correct_letters:
                    if letter in self.possible_letters[position]:
                        self.possible_letters[position].remove(letter)
                else:
                    for i in range(5) :
                        if letter in self.possible_letters[i]:
                            self.possible_letters[i].remove(letter)
            elif result == letter_result.yellow :
                if letter in self.possible_letters[position] :
                    self.possible_letters[position].remove(letter)
                self.correct_letters.add(letter)
            else :
                self.possible_letters[position] = [letter]
                self.correct_letters.add(letter)
    
    def eliminate_word(self, word) : 
        for position, letter in enumerate(word) :
            if letter not in self.possible_letters[position] :
                return True
        
        if not self.correct_letters.issubset(set(word)) :
            return True
        
        if(word == self.current_guess):
            return True
        
        return False

    def eliminate_words(self, possible_words) :
        return [word for word in possible_words if not self.eliminate_word(word)]

    def make_guess(self, possible_words, answers):
        if len(answers) == 1:
            return answers[0]
        
        if len(possible_words) == 1:
            return possible_words[0]

        if len(possible_words) == 14855:
            return best_word

        all_results = self.generate_cases(tuple(possible_words), tuple(answers))
        max_entropy_guess = max(possible_words, key=lambda word: self.joint_entropy(word, all_results))  
        self.current_guess = max_entropy_guess
        return max_entropy_guess

class WordleBot :
    possible_words = []
    all_words = []
    res = []
    def simulate_play(self, answers, all_words) :
        results = []
        wins = 0
        losses = 0
        self.all_words = all_words.copy()

        for answer in tqdm(answers, desc = "Guessing") :
            self.possible_words = answers.copy()
            self.res = []
            print('\n' + answer)
            wordle = Wordle().create(self.all_words, 6, answer)
            num_guesses = self.play(wordle)
            results.append([answer, num_guesses, wordle.state(), wordle.guesses, self.res])

            if wordle.state() == 1 :
                wins += 1
            else :
                losses += 1
        
        with open('output_answer.txt', 'w') as file:
            for result in results:
                file.write(str(result) + '\n')

        print("Total :" +  str(wins + losses))
        print("Wins :" +  str(wins))
        print("Losses :" +  str(losses))

    def play(self, wordle) :
        strategy = Strategy().create(self.possible_words, self.all_words)

        while wordle.state() == State.in_progress :
            guess_word = strategy.make_guess(wordle.all_words, self.possible_words)
            results = wordle.guess(guess_word)
            strategy.update(results)
            self.res.append(results)
            wordle.all_words = strategy.eliminate_words(wordle.all_words)
            self.possible_words = strategy.eliminate_words(self.possible_words)

        return len(wordle.guesses)



all_words = []
with open("words.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

    for line in lines :
        line_words = line.split()
        all_words.extend(line_words)

answers = []
with open("answers.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

    for line in lines :
        line_words = line.split()
        answers.extend(line_words)

with open("answer_cases.txt", "r") as file :
    lines = file.readlines()
    counter_pattern = re.compile(r"Counter\((\{.*?\})\)")
    modified_string = counter_pattern.sub(r'\1', lines[0])
    cases = ast.literal_eval(modified_string)
    main_cases = {key: Counter(value) for key, value in cases.items()}

with open('answer_entropies.txt', 'r') as file:
    lines = file.readlines()
    entropies = ast.literal_eval(lines[0])
    
best_word = max(entropies, key=entropies.get)

Dhanush = WordleBot()
Dhanush.simulate_play(answers, all_words)