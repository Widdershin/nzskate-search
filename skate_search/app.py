from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/search')
def search():
    print(request.data)
    return "Heyo you searched"

if __name__ == '__main__':
    app.run(debug=True)
