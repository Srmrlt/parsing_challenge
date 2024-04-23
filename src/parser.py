from lxml import etree
from memory_profiler import profile

from database import SKUOperations

from .offer_parser import OfferParser


class Parsing:
    def __init__(self, data_source):
        self.data_source = data_source
        self.marketplace_tags = []
        self.marketplace = {}

    @profile
    def parse_xml(self):
        self.marketplace_tags = ['name', 'company', 'url']
        self.marketplace = {}
        context = etree.iterparse(self.data_source, events=('end',))
        for event, elem in context:
            self.parse_by_tag(elem)
        del context

    def parse_by_tag(self, elem):
        if elem.tag in self.marketplace_tags:
            self.parse_marketplace(elem)
        elif elem.tag == 'category':
            self.parse_category(elem)
        elif elem.tag == 'offer':
            parsed_data = OfferParser(elem).parse()
            SKUOperations.add_sku_data(parsed_data)

    def parse_marketplace(self, elem):
        self.marketplace[elem.tag] = elem.text
        self.marketplace_tags.remove(elem.tag)
        if not self.marketplace_tags:
            # TODO save self.marketplace to database
            pass

    def parse_category(self, elem):
        pass
