from flask import Flask, render_template, redirect, request
import connection
import datamanager


app = Flask(__name__)


@app.route('/')
def index():
    questions = datamanager.get_last_five_questions()
    return render_template('index.html', questions=questions)


@app.route('/list')
def list_questions():
    id_and_question = datamanager.get_questions()
    print(id_and_question)
    return render_template('list.html', id_and_question=id_and_question)


@app.route('/add-question')
def add_question():
    return render_template('add-question.html')


@app.route('/add-question', methods=['POST'])
def route_save():
    question_title = request.form['Question Title']
    question_message = request.form['Question Message']
    datamanager.write_question('sample_data/question.csv', 4, question_title, question_message)
    return redirect('/list')


@app.route('/question/<int:question_id>')
def display_question(question_id=None):
    question = datamanager.display_question(question_id)
    # answers = connection.get_answers(question_id)
    return render_template('display-question.html', question=question)


@app.route('/question/<int:question_id>/new-answer')
def new_answer(question_id=None):
    return render_template('add-answer.html', id_=question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['POST'])
def save_answer(question_id=None):
    answer = request.form['Answer']
    datamanager.write_answer("sample_data/answer.csv", question_id, answer)
    return redirect('/list')


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
