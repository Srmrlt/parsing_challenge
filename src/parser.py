import logging

from lxml import etree

from .database import SKUOperations
from .offer_parser import OfferParser

logger = logging.getLogger('MainParser')


class Parsing:
    def __init__(self, data_source):
        self.data_source = data_source
        self.marketplace_tags = []
        self.marketplace = {}
        self.operation_count = 0
        self.bulk_offer_data = []

    def parse_xml(self):
        self.marketplace_tags = ['name', 'company', 'url']
        self.marketplace = {}
        context = etree.iterparse(self.data_source, events=('end',))
        for event, elem in context:
            self.parse_by_tag(elem)
        del context
        self._send_to_database(end=True)
        logger.info(f"Total number of parsed elements: {self.operation_count}")

    def parse_by_tag(self, elem):
        if elem.tag in self.marketplace_tags:
            self.parse_marketplace(elem)
        elif elem.tag == 'category':
            self.parse_category(elem)
        elif elem.tag == 'offer':
            parsed_data = OfferParser(elem).parse()
            elem.clear()
            self.bulk_offer_data.append(parsed_data)
            self._send_to_database()
            self._count_success_op()

    def parse_marketplace(self, elem):
        self.marketplace[elem.tag] = elem.text
        self.marketplace_tags.remove(elem.tag)
        if not self.marketplace_tags:
            # TODO save self.marketplace to database
            pass

    def parse_category(self, elem):
        pass

    def _count_success_op(self):
        self.operation_count += 1
        if self.operation_count % 1000 == 0:
            logger.info(f"Number of parsed elements: {self.operation_count}")

    def _send_to_database(self, end=False):
        if len(self.bulk_offer_data) == 850 or end:  # Send when bulk of data is ready
            SKUOperations.add_sku_data(self.bulk_offer_data)
            self.bulk_offer_data = []
