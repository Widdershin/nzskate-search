from flask import Flask, render_template, request
from store_plugins import (UltimateBoards, HyperRide,
                           BasementSkate, TerrabangSkate)
import json
from fuzzywuzzy import fuzz

app = Flask(__name__)

plugins = [UltimateBoards(), HyperRide(), BasementSkate(), TerrabangSkate()]


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/search')
def search():
    query = request.args["query"]

    results = []
    for plugin in plugins:
        results.extend(plugin.search_shop(query))

    results = sorted(
        results,
        key=lambda x: fuzz.partial_ratio(query, x.name),
        reverse=True
    )

    for listing in results:
        print("{}: {}".format(listing.name.strip(), fuzz.partial_ratio(query, listing.name)))

    return json.dumps([listing.to_dict() for listing in results])

if __name__ == '__main__':
    app.run(debug=True)
