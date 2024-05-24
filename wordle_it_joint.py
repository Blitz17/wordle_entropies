import numpy as np 
from tqdm import tqdm
from collections import Counter
from more_itertools import partition, flatten, chunked
import ast
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
    max_guesses = 14855
    guesses = []
    answer = ""
    possible_words = []
    
    def create(self, possible_words, max_guesses = 6, answer = "cream") :
        self.answer = answer
        self.possible_words = possible_words.copy()
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
        if guess not in self.guesses : 
            self.guesses.append(guess)
            self.possible_words.remove(guess)
        
        results = []

        for guess_letter, actual_letter in zip(guess, self.answer) :
            if guess_letter == actual_letter :
                results.append(letter_result.green)
            elif guess_letter in self.answer :
                results.append(letter_result.yellow)
            else :
                results.append(letter_result.grey)
        
        word_information = []
        for (position, letter) in enumerate(guess) : 
            word_information.append([position, letter, results[position]])
        
        return word_information

class Strategy :
    correct_letters = set()
    possible_letters = []
    all_words = []

    def create(self, all_words) :
        self.correct_letters = set()
        self.possible_letters = [set("abcdefghijklmnopqrstuvwxyz").copy() for i in range(5)]
        self.all_words = all_words
        return self

    def joint_entropy(self, word, counted_results):
        entropy = 0
        total_words = sum(counted_results[word].values())
        for result, counts in counted_results[word].items():
            p = (counts / total_words)
            entropy -= p * np.log(p)
        return entropy

    @lru_cache(100000)
    def generate_cases(self, possible_words):
        cases = {}
        status = 1
        for guess_word in possible_words:
            all_results = []
            print(status)
            status += 1
            for hidden_word in possible_words:
                result = []
                case = Wordle().create(list(possible_words), 6, hidden_word).guess(guess_word) 
                for letter in case:
                    result.append(letter[2])
                all_results.append(''.join(map(str, result)))
            cases[guess_word] = Counter(all_results)  
        if len(possible_words) == 14855:
            with open('cases.txt', 'w') as file:
                    file.write(str(cases) + '\n')
        return cases

    def update(self, updates) :
        for position, letter, result in updates :
            if result == letter_result.grey : 
                for i in range(5) :
                    if letter in self.possible_letters[i] :
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
        
        return False

    def eliminate_words(self, possible_words) :
        return [word for word in possible_words if not self.eliminate_word(word)]

    def make_guess(self, possible_words):
        if len(possible_words) == 1:
            return possible_words[0]

        all_results = self.generate_cases(tuple(possible_words))
        max_entropy_guess = max(possible_words, key=lambda word: self.joint_entropy(word, all_results))
        return max_entropy_guess

class WordleBot :
    possible_words = []
    all_words = []
    def simulate_play(self, words) :
        results = []
        wins = 0
        losses = 0
        self.all_words = words.copy()
        for answer in tqdm(words[0:1], desc = "Guessing") :
            wordle = Wordle().create(self.all_words, 6, answer)
            num_guesses = self.play(wordle)
            results.append([answer, num_guesses, wordle.state(), wordle.guesses])
            if wordle.state() == 1 :
                wins += 1
            else :
                losses += 1
        
        with open('output_joint.txt', 'w') as file:
            for result in results:
                file.write(str(result) + '\n')

        print("Total :" +  str(wins + losses))
        print("Wins :" +  str(wins))
        print("Losses :" +  str(losses))

    def play(self, wordle) :
        strategy = Strategy().create(self.all_words)
        while wordle.state() == State.in_progress :
            self.possible_words = wordle.possible_words
            guess_word = strategy.make_guess(self.possible_words)
            results = wordle.guess(guess_word)
            strategy.update(results)
            wordle.possible_words = strategy.eliminate_words(self.possible_words)
        return len(wordle.guesses)

words = []
with open("words.txt", "r") as file :
    lines = file.readlines()
    for line in lines :
        line_words = line.split()
        words.extend(line_words)
        
Dhanush = WordleBot()
Dhanush.simulate_play(words)