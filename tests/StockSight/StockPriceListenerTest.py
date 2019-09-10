import unittest
from StockSight.StockPriceListener import *
from StockSight.EsMap.StockPrice import mapping


class StockPriceListenerTest(unittest.TestCase):

    symbol = 'tsla'

    def setUp(self):
        config['redis']['db'] = 1
        self.mainClass = StockPriceListener()

    @classmethod
    def setUpClass(cls):
        cls.index_name = "stocksight_price_test_"+cls.symbol
        es.indices.create(index=cls.index_name, body=mapping, ignore=[400, 404])

    @classmethod
    def tearDownClass(cls):
        es.indices.delete(index=cls.index_name, ignore=[400, 404])

    def test_get_price(self):
        config['stock_price']['time_check'] = False
        self.mainClass.index_name = self.index_name
        self.mainClass.get_price(self.symbol)
        logs = es.search(index=self.index_name,body="{}")
        message = logs['hits']['hits'][0]['_source']
        self.assertIsNotNone(message['price_last'], "Price is empty")