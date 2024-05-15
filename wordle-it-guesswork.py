import numpy as np 

class State :
    in_progress = 0
    win = 1
    loss = -1

class letter_result :
    grey = -1
    yellow = 0
    green = 1

class Wordle :
    max_guesses = 6
    guesses = []
    answer = ""
    
    def create(self, answer = "cream") :
        self.answer = answer
        return self

    def state(self) :
        if len(self.guesses) > self.max_guesses :
            return State.loss
        elif self.answer in guesses : 
            return State.win
        else :
            return State.in_progress
    
    def guess(self, guess) :
        if guess not in guesses : 
            self.guesses.append(guess)
        
        results = []

        for guess_letter, actual_letter in zip(guess, self.answer) :
            if guess_letter == actual_letter :
                results.append(letter_result.green)
            elif guess_letter in self.answer :
                results.append(letter_result.yellow)
            else :
                result.append(letter_result.grey)
        
        word_information = []
        for (position, letter) in enumerate(guess) : 
            word_information.append([position, letter, results[position]])
        
        return word_information

def make_guess(candidates): 
    guess = np.random.choice(candidates)
    return guess

words = []
with open("words.txt", "r") as file :
    lines = file.readlines()
    for line in lines :
        line_words = line.split()
        words.extend(line_words)

print(len(words))
