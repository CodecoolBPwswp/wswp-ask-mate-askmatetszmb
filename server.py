from flask import Flask, render_template, redirect, request, url_for, session
import datamanager
import utility

app = Flask(__name__)
app.secret_key = 'somethingreallysecret'


@app.route('/')
def index():
    limit = 5
    questions = datamanager.get_questions(limit)
    username = None
    if 'user_name' in session:
        username = session['user_name']
    return render_template('index.html', questions=questions, username=username)


@app.route('/list')
def list_questions():
    questions = datamanager.get_questions()
    return render_template('list.html', questions=questions)


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
        return render_template('display-question.html',
                               question=question,
                               answers=answers,
                               comments=comments)
    else:
        answer_comments = datamanager.get_answer_comment(answer_ids)
        return render_template('display-question.html',
                               question=question,
                               answers=answers,
                               comments=comments,
                               answer_comments=answer_comments)


@app.route('/question/<int:question_id>/new-answer')
def add_answer(question_id=None):
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
def save_edited_answer(answer_id=None):
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
    datamanager.add_answer_comment(answer_id, answer_comment)
    return redirect('/list')


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id=None):
    datamanager.delete_comment(comment_id)
    return redirect('/list')


@app.route('/', methods=['POST'])
def search():
    data = request.form.to_dict()
    search_phrase = data['search_phrase']
    return redirect(url_for('show_search_result', search_phrase=search_phrase))


@app.route('/search?q=<string:search_phrase>')
def show_search_result(search_phrase=None):
    results = datamanager.search(search_phrase)
    return render_template('search-result.html', results=results)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user_name = user_data['user_name']
        user_password = user_data['password']
        hashed_password = utility.hash_password(user_password)
        try:
            datamanager.register_user(user_name, hashed_password)
            return redirect('/')
        except:
            return render_template('registration.html')
    else:
        return render_template('registration.html')


@app.route('/list-registered-users')
def list_registered_users():
    registered_users = datamanager.list_users()
    return render_template('/list-registered-users.html', registered_users=registered_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user_name = user_data['user_name']
        user_password = user_data['password']
        user = datamanager.get_user_data(user_name)
        if user is None:
            return redirect(url_for('login'))
        hashed_password = user['password']
        is_matching = utility.verify_password(user_password, hashed_password)
        if is_matching is True:
            session['user_name'] = user_data['user_name']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
