from pyquery import PyQuery


class UltimateBoards(object):

    """The Shop Plugin for UB"""

    search_url = "http://www.ultimateboards.co.nz/search/products/{query}"\
        .format

    def search_shop(self, query):
        query_url = self.search_url(query=query)
        query = PyQuery(url=query_url)

        results = self.parse_result_html(query(".galleryImageListItem"))

        return results

    def parse_result_html(self, html):
        raise NotImplemented
