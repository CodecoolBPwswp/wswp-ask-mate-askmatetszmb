from flask import Flask, render_template, redirect, request
import connection


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    id_title = connection.data_maker()
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
    time, view_number, title, message = connection.get_question_data(question_id)
    return render_template('display-question.html', id_=question_id, time=time, view_number=view_number, title=title, message=message)


if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )
