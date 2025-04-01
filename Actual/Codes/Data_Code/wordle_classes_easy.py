import numpy as np 
from tqdm import tqdm
from collections import Counter

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
    correct_letters = []
    possible_letters = []
    all_words = []
    answers = []
    second_guesses = {}
    current_guess = ""
    update_2 = ""
    def create(self, answers, all_words, second_guesses) :
        self.correct_letters = []
        self.possible_letters = [set("abcdefghijklmnopqrstuvwxyz").copy() for i in range(5)]
        self.all_words = all_words
        self.answers = answers
        self.second_guesses = second_guesses
        return self

    def joint_entropy(self, word, counted_results):
        entropy = 0
        total_words = sum(counted_results[word].values())

        for result, counts in counted_results[word].items():
            p = (counts / total_words)
            entropy -= p * np.log(p)

        return float(np.floor(entropy*1000000)/1000000)

    def generate_cases(self, all_words, answers):
        cases = {}
        status = 0
        print(len(all_words))
        print(len(answers))
        for guess_word in all_words:
            all_results = []
            status += 1
            for hidden_word in answers:
                result = []
                case = Wordle().create(list(all_words), 6, hidden_word).guess(guess_word) 
                for letter in case:                        
                    result.append(letter[2])
                all_results.append(''.join(map(str, result)))

            cases[guess_word] = Counter(all_results)             
        return cases

    def update(self, updates) :
        if self.update_2 == "":
            checks = []
            for letter in updates:                        
                checks.append(letter[2])
            self.update_2 = ''.join(map(str, checks))
        letters_checked = []
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
                if letter not in self.correct_letters:
                    self.correct_letters.append(letter)
                elif (letter in self.correct_letters) & (letter in letters_checked) & (self.correct_letters.count(letter) == letters_checked.count(letter)):
                    self.correct_letters.append(letter)
                letters_checked.append(letter)

            else :
                self.possible_letters[position] = [letter]
                if letter not in self.correct_letters:
                    self.correct_letters.append(letter)
                elif (letter in self.correct_letters) & (letter in letters_checked) & (self.correct_letters.count(letter) == letters_checked.count(letter)):
                    self.correct_letters.append(letter)
                letters_checked.append(letter)
            
        print(self.correct_letters)
    
    def eliminate_word(self, word) : 
        def containedInFirst(a, b):
            a_count = Counter(a)
            b_count = Counter(b)
            for key in b_count:
                if key not in a_count.keys():
                    return False
                if b_count[key] > a_count[key]:
                    return False
            return True
        
        for position, letter in enumerate(word) :
            if letter not in self.possible_letters[position] :
                return True
        
        if not containedInFirst(list(word), self.correct_letters) :
            return True
        
        if(word == self.current_guess):
            return True
        
        return False

    def eliminate_words(self, answers) :
        return [word for word in answers if not self.eliminate_word(word)]

    def make_guess(self, all_words, answers, best_word, best_word_entropy, x):
        entropy = 0
        if len(answers) == 2:
            print("Guess : " + answers[0])
            return answers[0], entropy
        
        if len(answers) == 1:
            print("Guess : " + answers[0])
            return answers[0], entropy
        
        if len(all_words) == 1:
            print("Guess : " + all_words[0])
            return all_words[0], entropy

        if x == 0:
            print("Guess : " + best_word)
            return best_word, best_word_entropy
        
        if x == 1:
            print(self.update_2)
            if self.update_2 in self.second_guesses:
                guess, guess_entropy = self.second_guesses[self.update_2]
                print("Guess2 : " + guess)
                return self.second_guesses[self.update_2]

        all_results = self.generate_cases(tuple(all_words), tuple(answers))
        max_entropy_guess = max(all_words, key=lambda word: self.joint_entropy(word, all_results))  
        entropy = self.joint_entropy(max_entropy_guess, all_results)
        self.current_guess = max_entropy_guess
        if x == 1:
            if self.update_2 not in self.second_guesses:
                self.second_guesses[self.update_2] = (max_entropy_guess, entropy)
                print("2nd Guesses : " + str(self.second_guesses))

        print('\n' + "Guess : " + max_entropy_guess)
        return (max_entropy_guess, entropy)

class WordleBot :
    answers = []
    all_words = []
    res = []
    possible_words_count = []
    remaining_words_count = []
    entropies = []
    best_word_entropy = 0
    second_guesses = {}
    def simulate_play(self, answers, all_words, best_word, best_word_entropy) :
        results = []
        wins = 0
        losses = 0
        self.all_words = all_words.copy()
        for answer in tqdm(answers, desc = "Guessing") :
            self.answers = answers.copy()
            self.res = []
            self.possible_words_count = []
            self.remaining_words_count = []
            self.entropies = []
            print('\n' + "Guess Word:" + answer)
            wordle = Wordle().create(self.all_words, 6, answer)
            num_guesses = self.play(wordle, best_word, best_word_entropy)
            results.append([answer, num_guesses, wordle.state(), wordle.guesses, self.res, self.possible_words_count, self.remaining_words_count, self.entropies])
            print(results[-1])
            if wordle.state() == 1 :
                wins += 1
            else :
                losses += 1

        print(results[0:5])

        with open('output_answer_easy2.txt', 'w') as file:
            for result in results:
                file.write(str(result) + '\n')
        
        with open('second_guesses_easy2.txt', 'w') as file:
            file.write(str(self.second_guesses) + '\n')

        print("Total :" +  str(wins + losses))
        print("Wins :" +  str(wins))
        print("Losses :" +  str(losses))

    def play(self, wordle, best_word, best_word_entropy) :
        strategy = Strategy().create(self.answers, self.all_words, self.second_guesses)
        x = 0
        while wordle.state() == State.in_progress :
            guess_word, entropy = strategy.make_guess(wordle.all_words, self.answers, best_word, best_word_entropy, x)
            if x == 0 :
                x = 1
            elif x == 1 :
                x = 2
            results = wordle.guess(guess_word)
            strategy.update(results)
            self.res.append(results)
            self.possible_words_count.append(len(self.answers))
            self.answers = strategy.eliminate_words(self.answers)
            self.remaining_words_count.append(len(self.answers))
            self.entropies.append(entropy)
            print(self.answers)
        self.second_guesses = strategy.second_guesses
        return len(wordle.guesses)