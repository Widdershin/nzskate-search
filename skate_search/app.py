from flask import Flask, render_template, request
from store_plugins import (UltimateBoards, HyperRide,
                           BasementSkate, TerrabangSkate)
import json

app = Flask(__name__)

plugins = [UltimateBoards(), HyperRide(), BasementSkate(), TerrabangSkate()]


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/search')
def search():
    results = []
    for plugin in plugins:
        results.extend(plugin.search_shop(request.args["query"]))

    return json.dumps([listing.to_dict() for listing in results])

if __name__ == '__main__':
    app.run(debug=True)
