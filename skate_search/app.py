from flask import Flask, render_template, request
from .store_plugins import (UltimateBoards, HyperRide,
                            BasementSkate, TerrabangSkate,
                            TheBoardroom)
import json
from fuzzywuzzy import fuzz
from concurrent import futures
from operator import attrgetter

from urllib.error import URLError

app = Flask(__name__)

plugins = [
    UltimateBoards(),
    HyperRide(),
    BasementSkate(),
    TerrabangSkate(),
]


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/search')
def search():
    query = request.args["query"]

    results = []

    def search_shop(plugin):
        try:
            results.extend(plugin.search_shop(query))
        except URLError:
            print('{} plugin crapped out.'.format(plugin.SHOP_NAME))

    with futures.ThreadPoolExecutor(max_workers=len(plugins)) as pool:
        for thing in pool.map(search_shop, plugins):
            pass

    for result in results:
        result.relevance = fuzz.partial_ratio(query.lower(),
                                              result.name.lower())

    results = sorted(
        results,
        key=attrgetter("relevance"),
        reverse=True
    )

    return json.dumps([listing.to_dict() for listing in results])

if __name__ == '__main__':
    app.run(debug=True)
