from pyquery import PyQuery


class Listing(object):

    def __init__(self, name, link, price, shop_name):
        self.shop_name = shop_name
        self.name = name
        self.link = link
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.link,
            "price": self.price,
            "shop_name": self.shop_name
        }


class ShopPlugin(object):

    """The Shop Plugin parent class"""

    search_url = "http://www.example.com/search/{query}"

    SHOP_NAME = "Default"
    LISTING_QUERY = None

    def search_shop(self, query):
        """Returns an array of listings for the query"""
        query_url = self.search_url.format(query=query)
        query = PyQuery(url=query_url)

        results = self.parse_result_html(query(self.LISTING_QUERY))

        return results

    def parse_result_html(self, html):

        listings = []

        for raw_listing in html:
            listings.append(self.create_listing(raw_listing))

        return listings

    def create_listing(self, listing_html):
        raise NotImplemented


class UltimateBoards(ShopPlugin):

    """The Shop Plugin for UB"""

    search_url = "http://www.ultimateboards.co.nz/search/products/{query}"\

    SHOP_NAME = "UB"
    LISTING_QUERY = ".galleryImageListItem"

    def create_listing(self, listing_html):
        title_div = recursive_class_find(listing_html, "titleLarge")[0]
        title_link = title_div.find('a')

        title = title_link.text

        link = title_link.items()[0][1]

        price = recursive_class_find(listing_html, "amount")[0].text

        return Listing(title, link, price, shop_name=self.SHOP_NAME)


def recursive_class_find(element, search_class):
    children = element.getchildren()

    if not children:
        return None

    find_result = element.find_class(search_class)

    if find_result:
        return find_result

    for child in children:
        return recursive_class_find(child, search_class)
