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
    
    def create(self, possible_words, answer = "cream") :
        self.answer = answer
        self.possible_words = possible_words
        self.guesses = []
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

class WordleBot :
    possible_words = []
    def play(self, wordle) :
        while wordle.state() == State.in_progress :
            self.possible_words = wordle.possible_words
            guess_word = make_guess(self.possible_words)
            results = wordle.guess(guess_word)
        return len(wordle.guesses)

    def simulate_play(self) :
        results = []
        for answer in tqdm(words[0:5], desc = "Guessing"):
            all_words = words.copy()
            wordle_answer = Wordle().create(all_words, answer)
            num_guesses = self.play(wordle_answer)
            results.append([answer, num_guesses])
            # time.sleep(0.001)
        
        with open('output_guesswork.txt', 'w') as file:
            for result in results:
                file.write(str(result) + '\n')

def make_guess(possible_words): 
    guess = np.random.choice(possible_words)
    return guess

words = []
with open("words.txt", "r") as file :
    lines = file.readlines()
    for line in lines :
        line_words = line.split()
        words.extend(line_words)

Dhanush = WordleBot()
Dhanush.simulate_play()