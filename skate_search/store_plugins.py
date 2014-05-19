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

    SEARCH_URL = "http://www.example.com/search/{query}"
    SHOP_NAME = "Default"
    LISTING_QUERY = None

    def load_search_page(self, query):
        query_url = self.SEARCH_URL.format(query=self.sanitize_query(query))
        query = PyQuery(url=query_url)

        return query

    def search_shop(self, query):
        """Returns an array of listings for the query"""

        query = self.load_search_page(query)

        results = self.parse_result_html(query(self.LISTING_QUERY))

        return results

    def parse_result_html(self, html):

        listings = []

        for raw_listing in html:
            listings.append(self.create_listing(raw_listing))

        return listings

    def create_listing(self, listing_html):
        raise NotImplemented

    def sanitize_query(self, query):
        raise NotImplemented


class UltimateBoards(ShopPlugin):

    """The Shop Plugin for UB"""

    SEARCH_URL = "http://www.ultimateboards.co.nz/search/products/{query}"
    SHOP_NAME = "UB"
    LISTING_QUERY = ".galleryImageListItem"

    def create_listing(self, listing_html):
        title_div = recursive_class_find(listing_html, "titleLarge")[0]
        title_link = title_div.find('a')

        title = title_link.text

        link = title_link.items()[0][1]

        price = recursive_class_find(listing_html, "amount")[0].text

        return Listing(title, link, price, shop_name=self.SHOP_NAME)

    def sanitize_query(self, query):
        return query.replace(" ", "-")


class HyperRide(ShopPlugin):
    # longboard categories:401,843,683,399,402,778,780,792,775,844,845,681

    """The Shop Plugin for Hyper"""

    SEARCH_URL = "http://www.hyperride.co.nz/product/{query}/search#/?size=0"
    SHOP_NAME = "Hyper"
    LISTING_QUERY = "#productsSection .product_item"

    def create_listing(self, listing_html):
        product_description = recursive_class_find(
            listing_html, "product_desc")[0]

        name = (product_description.text_content()
                .title().replace("Mm", "mm"))  # TODO: fix bad hack
        link = "http://www.hyperride.co.nz{url}".format(
            url=product_description.items()[0][1])

        price = recursive_class_find(listing_html, "rrp")[0].text_content()[1:]

        return Listing(name, link, price, shop_name=self.SHOP_NAME)

    def sanitize_query(self, query):
        return query.replace(" ", "%20")

    # TODO: Filter hyper results based on url


class BasementSkate(ShopPlugin):

    SEARCH_URL = "https://www.basementskate.com.au/search.php?"\
                 "mode=search&substring={query}&including=all&by_title=on"
    SHOP_NAME = "BasementSkate"

    def search_shop(self, query):
        query = self.load_search_page(query)

        product_cells = query('.product-title')
        prices = query('.currency')

        raw_listings = zip(product_cells, prices)

        return self.parse_result_html(raw_listings)

    def create_listing(self, listing):
        title_el, price_el = listing

        name = title_el.text
        link = title_el.items()[0][1]
        price = price_el.text_content()[1:]

        return Listing(name, link, price, self.SHOP_NAME)

    def sanitize_query(self, query):
        return query.replace(" ", "+")


def recursive_class_find(element, search_class):
    children = element.getchildren()

    if not children:
        return None

    find_result = element.find_class(search_class)

    if find_result:
        return find_result

    for child in children:
        return recursive_class_find(child, search_class)
