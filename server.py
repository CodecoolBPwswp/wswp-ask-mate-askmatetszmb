from flask import Flask, flash, render_template, redirect, request, url_for, session
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
    user = None
    if 'user_name' in session:
        user = session['user_name']
    return render_template('list.html', questions=questions, user=user)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = request.form.to_dict()
        question_title = question['question_title']
        question_message = question['question_message']
        user_name = session['user_name']
        user_data = datamanager.get_user_data(user_name)
        user_id = user_data['id']
        datamanager.add_question(question_title, question_message, user_id)
        return redirect('/list')
    else:
        return render_template('add-question.html')


@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def display_question(question_id=None):
    datamanager.view_counter(question_id)
    question = datamanager.display_question(question_id)
    answers = datamanager.get_answers(question_id)
    print(answers)
    comments = datamanager.get_question_comment(question_id)
    answer_ids = datamanager.get_answer_id(question_id)
    user = None
    if 'user_name' in session:
        user = session['user_name']
    if answer_ids == []:
        return render_template('display-question.html',
                               question=question,
                               answers=answers,
                               comments=comments,
                               user=user)
    else:
        answer_comments = datamanager.get_answer_comment(answer_ids)
        return render_template('display-question.html',
                               question=question,
                               answers=answers,
                               comments=comments,
                               answer_comments=answer_comments,
                               user=user)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id=None):
    if request.method == 'POST':
        answer = request.form.to_dict()
        answer_message = answer['answer_message']
        user = session['user_name']
        user_data = datamanager.get_user_data(user)
        user_id = user_data['id']
        datamanager.add_answer(question_id, answer_message, user_id)
        return redirect(url_for('display_question', question_id=question_id))
    else:
        return render_template('add-answer.html', question_id=question_id)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id=None):
    if request.method == 'POST':
        edited_answer_packed = request.form.to_dict()
        edited_answer = edited_answer_packed['edited_answer']
        datamanager.edit_answer(answer_id, edited_answer)
        return redirect('/list')
    else:
        return render_template('edit-answer.html', answer_id=answer_id)


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_question_comment(question_id=None):
    if request.method == 'POST':
        question_comment_pack = request.form.to_dict()
        question_comment = question_comment_pack['question_comment']
        user_name = session['user_name']
        user_data = datamanager.get_user_data(user_name)
        user_id = user_data['id']
        datamanager.add_question_comment(question_id, question_comment, user_id)
        return redirect(url_for('display_question', question_id=question_id))
    else:
        return render_template('add-question-comment.html', question_id=question_id)


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_answer_comment(answer_id=None):
    if request.method == 'POST':
        answer_comment_pack = request.form.to_dict()
        answer_comment = answer_comment_pack['answer_comment']
        user_name = session['user_name']
        user_data = datamanager.get_user_data(user_name)
        user_id = user_data['id']
        datamanager.add_answer_comment(answer_id, answer_comment, user_id)
        return redirect('/list')
    else:
        return render_template('add-answer-comment.html', answer_id=answer_id)


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
            error = 'Username already in use. Please try again!'
            return render_template('registration.html', error=error)
    else:
        return render_template('registration.html')


@app.route('/list-registered-users')
def list_registered_users():
    registered_users = datamanager.list_users()
    return render_template('list-registered-users.html', registered_users=registered_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user_name = user_data['user_name']
        user_password = user_data['password']
        user = datamanager.get_user_data(user_name)

        if user is None:
            error = 'Invalid username or password. Please try again!'
            return render_template('login.html', error=error)

        hashed_password = user['password']
        is_matching = utility.verify_password(user_password, hashed_password)

        if is_matching is True:
            session['user_name'] = user_data['user_name']
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password. Please try again!'
            return render_template('login.html', error=error)
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
