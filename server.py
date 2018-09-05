from flask import Flask, render_template, redirect, request
import datamanager


app = Flask(__name__)


@app.route('/')
def index():
    questions = datamanager.get_last_five_questions()
    return render_template('index.html', questions=questions)


@app.route('/list')
def list_questions():
    id_and_question = datamanager.get_questions()
    return render_template('list.html', id_and_question=id_and_question)


@app.route('/add-question')
def add_question():
    return render_template('add-question.html')


@app.route('/add-question', methods=['POST'])
def route_save():
    question = request.form.to_dict()
    question_title = question['question_title']
    question_message = question['question_message']
    datamanager.add_question(question_title, question_message)
    return redirect('/list')


@app.route('/question/<int:question_id>')
def display_question(question_id=None):
    datamanager.view_counter(question_id)
    question = datamanager.display_question(question_id)
    answers = datamanager.get_answers(question_id)
    comments =datamanager.get_query_comment(question_id)
    return render_template('display-question.html', question=question, answers=answers, comments=comments)


@app.route('/question/<int:question_id>/new-answer')
def new_answer(question_id=None):
    return render_template('add-answer.html', id_=question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['POST'])
def save_answer(question_id=None):
    answer = request.form.to_dict()
    answer_message = answer['answer_message']
    datamanager.add_answer(answer_message, question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/edit')
def edit_answer(answer_id=None):
    return render_template('edit-answer.html', answer_id=answer_id)


@app.route('/answer/<answer_id>/edit', methods=['POST'])
def save_edit_answer(answer_id=None):
    edited_answer_packed = request.form.to_dict()
    edited_answer = edited_answer_packed['edited_answer']
    datamanager.edit_answer(answer_id, edited_answer)
    return redirect('/list')


@app.route('/question/<int:question_id>/new-comment')
def add_query_comment(question_id=None):
    return render_template('add-query-comment.html', question_id=question_id)


@app.route('/question/<int:question_id>/new-comment', methods=['POST'])
def save_query_comment(question_id=None):
    query_comment_pack = request.form.to_dict()
    query_comment = query_comment_pack['query_comment']
    datamanager.add_query_comment(question_id, query_comment)
    return redirect('/list')


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
