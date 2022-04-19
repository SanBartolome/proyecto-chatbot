from flask import Flask, request, jsonify, render_template
import pickle
from chatbot import return_answer

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# endpoint de prueba
@app.route('/hello', methods=['GET'])
def hello():
  return "Hello World!"

@app.route('/send', methods=['POST'])
def send_message():
  message = request.form['message']
  
  count_vectorizer = pickle.load(open("count_vectorizer.pickle", "rb"))
  decision_tree_classifier = pickle.load(open("decision_tree_classifier.pickle", "rb"))
  rules = pickle.load(open("rules.pickle", "rb"))
  utterances_examples = pickle.load(open("utterances_examples.pickle", "rb"))
  
  if message != 'Yakarta':
    answer, intent = return_answer(message, count_vectorizer, decision_tree_classifier, rules, utterances_examples)
  else:
    answer = message
  
  response_text = { "message":  answer }
  return jsonify(response_text)


if __name__ == '__main__':
    app.run(debug=True)