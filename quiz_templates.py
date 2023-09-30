from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'SUPERSEKRETKEY'


@app.route("/")
def hello():
    session['question'] = 1
    return render_template('quiz_templates/index.html')


@app.route("/quiz/")
def quiz():
    q = None

    # dictionary containing the questions and answers for the quiz
    qa = {
        "1": {
            "text": "Which is the best university in Edinburgh?",
            "answer": 1,
            "answers": ["Edinburgh Napier", "University of Edinburgh", "Heriott Watt", "Queen Mary"]
        },
        "2": {
            "text": "Which is the best university in Scotland?",
            "answer": 1,
            "answers": ["Edinburgh Napier", "University of Edinburgh", "Heriott Watt", "Queen Mary"]
        },
        "3": {
            "text": "Which is the best university in the UK?",
            "answer": 1,
            "answers": ["Edinburgh Napier", "University of Edinburgh", "Heriott Watt", "Queen Mary"]
        },
        "4": {
            "text": "Which is the best university in the World?",
            "answer": 1,
            "answers": ["Edinburgh Napier", "University of Edinburgh", "Heriott Watt", "Queen Mary"]
        }
    }

    # checks for valid session and retrieve current question if it exists
    # or else sets current question to 1 if it doesn't
    try:
        if (session['question']):
            q = int(session['question'])
    except KeyError:
        q = 1

    # quiz route uses a URL argument parameter to communicate the players answer number
    # back to the server, this is retrieved here. We then branch depending on if there is an answer or not
    # Note - render_template() calls supply various additional bits of data that
    # Jinja2 directives use to complete the template into a fully formed HTML page
    answer = request.args.get('answer', None)
    if answer is not None:
        correct = qa.get(str(q)).get('answer')
        if str(answer) == str(correct):
            q = q + 1
            session['question'] = q
            if q > len(qa):
                # If answer correct and run out of questions, render template for successful culmination of quiz
                return render_template('quiz_templates/success.html')
            else:
                # If answer is correct and there are more questions, render template for next question
                return render_template('quiz_templates/quiz.html', text=qa[str(q)]["text"],
                                       answers=qa[str(q)]["answers"], number=q)
        else:
            # If answer is wrong, render template for wrong answer and return it
            return render_template('quiz_templates/wrong.html', text="Das ist der wrong answer!!!")
    else:
        # If no answer, display page for current question
        return render_template('quiz_templates/quiz.html', text=qa[str(q)]["text"], answers=qa[str(q)]["answers"],
                               number=q)


@app.route("/success/")
def success():
    return render_template('quiz_templates/success.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
