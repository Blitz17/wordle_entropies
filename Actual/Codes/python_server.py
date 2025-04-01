from Data_Code.wordle_classes_easy import *
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

all_words = []
with open("Actual/Codes/Data_Code/words.txt", "r", encoding="utf8") as file :
    lines = file.readlines()

    for line in lines :
        line_words = line.split()
        all_words.extend(line_words)

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    guess = data.get("guess", "")
    answer = data.get("answer", "")
    print(len(all_words))
    print("Guess:", guess)
    print("Answer:", answer)
    if len(guess) != 5 or len(answer) != 5:
        return jsonify({"error": "Invalid word length"}), 400

    result = Wordle().create(list(all_words), 6, answer).guess(guess)
    print(result)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
