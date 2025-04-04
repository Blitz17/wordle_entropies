import numpy as np 
from tqdm import tqdm
import time

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
    
    def create(self, possible_words, max_guesses, answer = "cream") :
        self.answer = answer
        self.possible_words = possible_words
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
        
        word_information = []
        for (position, letter) in enumerate(guess) : 
            word_information.append([position, letter, results[position]])
        
        return word_information

class Strategy :
    correct_letters = set()
    possible_letters = []

    def create(self):
        self.correct_letters = set()
        self.possible_letters = [set("abcdefghijklmnopqrstuvwxyz").copy() for i in range(5)]
        return self

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

    def make_guess(self, possible_words) : 
        guess = np.random.choice(possible_words)
        return guess
                
class WordleBot :
    possible_words = []
    def simulate_play(self, words) :
        results = []
        wins = 0
        losses = 0
        for answer in tqdm(words, desc = "Guessing") :
            all_words = words.copy()
            wordle = Wordle().create(all_words, 6, answer)
            num_guesses = self.play(wordle)
            results.append([answer, num_guesses, wordle.state(), wordle.guesses])
            if wordle.state() == 1 :
                wins += 1
            else :
                losses += 1
        
        with open('output_guess_updates.txt', 'w') as file:
            for result in results:
                file.write(str(result) + '\n')

        print("Total :" +  str(wins + losses))
        print("Wins :" +  str(wins))
        print("Losses :" +  str(losses))

    def play(self, wordle) :
        strategy = Strategy().create()
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