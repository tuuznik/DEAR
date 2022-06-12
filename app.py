from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        pass
        # if valid_login(request.form['username'],
        #                request.form['password']):
        #     return log_the_user_in(request.form['username'])
        # else:
        #     error = 'Invalid username/password'
    return render_template("index.html")


@app.route("/sign_up", methods=["GET"])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')


if __name__ == "__main__":
    app.run(debug=True)