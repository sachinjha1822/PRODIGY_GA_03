from flask import Flask, render_template, request
import random
from collections import defaultdict

app = Flask(__name__)

def build_markov_chain(text):
    words = text.split()
    markov_chain = defaultdict(list)
    
    for i in range(len(words) - 1):
        markov_chain[words[i]].append(words[i + 1])
    
    return markov_chain

def generate_text(chain, length=10):
    word = random.choice(list(chain.keys()))
    result = [word]
    
    for _ in range(length - 1):
        next_words = chain[word]
        if not next_words:
            break
        word = random.choice(next_words)
        result.append(word)
    
    return ' '.join(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    sample_text = request.form['sample_text']
    try:
        length = int(request.form['length'])
    except ValueError:
        length = 10  # Default length

    markov_chain = build_markov_chain(sample_text)
    generated_text = generate_text(markov_chain, length)

    return render_template('result.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
