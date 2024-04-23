import json
import logging
import uuid
from datetime import datetime

logger = logging.getLogger('OfferParser')


class OfferParser:
    def __init__(self, offer):
        self.offer = offer
        self.offer_data = {}

    def parse(self):
        self._extract_data()
        self._calculate_discount()
        self._parse_params_as_json()
        self._add_metadata()
        return self.offer_data

    def _extract_data(self):
        data_maps = {
            int: {'product_id': 'group_id', 'category_id': 'categoryId', 'barcode': 'barcode'},
            float: {'price_before_discounts': 'oldprice', 'price_after_discounts': 'price'},
            str: {'title': 'name', 'description': 'description', 'seller_name': 'vendor',
                  'first_image_url': 'picture', 'currency': 'currencyId'}
        }
        for data_type, map_dict in data_maps.items():
            self._extract_offer_data(map_dict, data_type)

    def _calculate_discount(self):
        old_price = self.offer_data['price_before_discounts']
        new_price = self.offer_data['price_after_discounts']
        if old_price and new_price:
            self.offer_data['discount'] = old_price - new_price

    def _parse_params_as_json(self):
        params_dict = {param.get('name'): param.text for param in self.offer.findall('param')}
        self.offer_data['features'] = json.dumps(params_dict)

    def _add_metadata(self):
        metadata = {
            'uuid': str(uuid.uuid4()),
            'inserted_at': datetime.now(),
            'updated_at': datetime.now(),
        }
        self.offer_data.update(metadata)

    def _extract_offer_data(self, data_map: dict[str, str], to_type):
        for key, value in data_map.items():
            data = self.offer.findtext(value)
            self.offer_data[key] = self._safe_convert(data, to_type) if data else None

    @staticmethod
    def _safe_convert(value: str, to_type):
        try:
            return to_type(value)
        except (ValueError, TypeError) as e:
            logger.error(f"Conversion error: {e} for value: {value}")
            return None
