from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, Wold!<p>"


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/uh-huh/', methods=['GET', 'POST'])
def uh_huh():
    if request.method == 'GET':
        return "The URL /uh-huh can't be accessed directly"
    if request.method == 'POST':
        form_data = request.form
        usr_time = request.form.get('usr_time')
        url = request.form.get('url')
        print("HERE", usr_time, url)
        return render_template('uh_huh.html', form_data=form_data)
