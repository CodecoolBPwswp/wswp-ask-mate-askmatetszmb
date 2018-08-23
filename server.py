from flask import Flask, render_template, redirect, request
from connection import data_maker


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    id_title = data_maker()
    return render_template('list.html', id_title=id_title)


@app.route('/add-question')
def add_question():
    return render_template('add-question.html')


@app.route('/add-question', methods=['POST'])
def route_save():
    question_title = request.form['Question Title']
    question_message = request.form['Question Message']
    return redirect('/')


@app.route('/question/<int:question_id>')
def display_question(question_id=None):
    return render_template('display-question.html', id_=question_id)


@app.route('/question/<int:question_id>/new-answer')
def new_answer(question_id=None):
    return render_template('add-answer.html', id_=question_id)


@app.route('/new-answer', methods=['POST'])
def save_answer():
    answer = request.form['Answer']
    return redirect('/')

if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
