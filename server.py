from flask import Flask, render_template, redirect, request


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    return render_template('list.html')


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


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
