from flask import Flask, render_template, redirect, request, url_for
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
def save_question():
    question = request.form.to_dict()
    question_title = question['question_title']
    question_message = question['question_message']
    datamanager.add_question(question_title, question_message)
    return redirect('/list')


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id=None):
    datamanager.view_counter(question_id)
    question = datamanager.display_question(question_id)
    answers = datamanager.get_answers(question_id)
    comments = datamanager.get_question_comment(question_id)
    answer_ids = datamanager.get_answer_id(question_id)
    if answer_ids == []:
        return render_template('display-question.html', question=question, answers=answers, comments=comments)
    else:
        answer_comments = datamanager.get_answer_comment(answer_ids)
        return render_template('display-question.html', question=question, answers=answers,
                               comments=comments, answer_comments=answer_comments)


@app.route('/question/<int:question_id>/new-answer')
def new_answer(question_id=None):
    return render_template('add-answer.html', question_id=question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['POST'])
def save_answer(question_id=None):
    answer = request.form.to_dict()
    answer_message = answer['answer_message']
    datamanager.add_answer(question_id, answer_message)
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
def add_question_comment(question_id=None):
    return render_template('add-query-comment.html', question_id=question_id)


@app.route('/question/<int:question_id>/new-comment', methods=['POST'])
def save_question_comment(question_id=None):
    question_comment_pack = request.form.to_dict()
    question_comment = question_comment_pack['question_comment']
    datamanager.add_question_comment(question_id, question_comment)
    return redirect('/list')


@app.route('/answer/<answer_id>/new-comment')
def add_answer_comment(answer_id=None):
    return render_template('comment-to-answer.html', answer_id=answer_id)


@app.route('/answer/<answer_id>/new-comment', methods=['POST'])
def save_answer_comment(answer_id=None):
    answer_comment_pack = request.form.to_dict()
    answer_comment = answer_comment_pack['new_comment']
    datamanager.add_new_comment(answer_id, answer_comment)
    return redirect('/list')


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id=None):
    datamanager.delete_comment(comment_id)
    return redirect("/list")


@app.route('/', methods=['POST'])
def search():
    data = request.form.to_dict()
    search_phrase = data['search_phrase']
    return redirect(url_for('show_search', search_phrase=search_phrase))


@app.route('/search?q=<string:search_phrase>')
def show_search(search_phrase=None):
    results = datamanager.search(search_phrase)
    return render_template('search-result.html', results=results)


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
