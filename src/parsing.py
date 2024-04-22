import os

import requests
from lxml import etree


class Parsing:
    def __init__(self):
        self.response = None
        self.file_path = "temp.xml"
        self.marketplace_tags = []
        self.marketplace = {}

    def get_data(self):
        url = os.getenv("URL")
        headers = {'Accept-Encoding': 'identity'}
        self.response = requests.get(url, stream=True, headers=headers)
        print(f"{self.response.status_code=}")

    def parse_xml(self):
        self.marketplace_tags = ['name', 'company', 'url']
        self.marketplace = {}
        self.get_data()
        context = etree.iterparse(self.response.raw, events=('start',))
        for event, elem in context:
            self.parse_by_tag(elem)
            self._clear_elem(elem)
        del context

    @staticmethod
    def _clear_elem(elem):
        elem.clear()
        while elem.getprevious() is not None:
            if elem.getparent() is not None:
                del elem.getparent()[0]

    def parse_by_tag(self, elem):
        if elem.tag in self.marketplace_tags:
            self.parse_marketplace(elem)
        elif elem.tag == 'category':
            self.parse_category(elem)
        elif elem.tag == 'offer':
            self.parse_offers(elem)

    def parse_marketplace(self, elem):
        self.marketplace[elem.tag] = elem.text
        self.marketplace_tags.remove(elem.tag)
        if not self.marketplace_tags:
            # TODO save self.marketplace to database
            pass

    def parse_category(self, elem):
        pass

    @staticmethod
    def parse_offers(offer):
        offer_data = {
            'barcode': offer.findtext('barcode'),
            'categoryId': offer.findtext('categoryId'),
            'currencyId': offer.findtext('currencyId'),
            'description': offer.findtext('description'),
            'group_id': offer.findtext('group_id'),
            'modified_time': offer.findtext('modified_time'),
            'name': offer.findtext('name'),
            'oldprice': offer.findtext('oldprice'),
            'price': offer.findtext('price'),
            'url': offer.findtext('url'),
            'vendor': offer.findtext('vendor'),
            'pictures': [img.text for img in offer.findall('picture')],
            'params': {param.get('name'): param.text for param in offer.findall('param')}
        }
        # TODO save offer_data to database
        return offer_data
