import unittest
from feauture_extraction import *


class TestFeautureExtraction(unittest.TestCase):
    def setUp(self):
        self.URL = 'https://stackoverflow.com'
        self.feautureExtraction = UrlFeautures(self.URL)

    def test_has_ip(self):
        self.assertEqual(self.feautureExtraction.has_ip(
            'https://stackoverflow.com'), 0)
        self.assertEqual(self.feautureExtraction.has_ip(
            'http://1563:6ae1:4cab:a557:0d6d:af67:6b44:2be1/2/paypal.ca/index.html'), 1)
        self.assertEqual(self.feautureExtraction.has_ip(
            'http://125.98.3.123/fake.html'), 1)

    def test_getDotsInHostname(self):
        self.assertEqual(
            self.feautureExtraction.getDotsInHostname(self.URL), 1)

    def test_hasAtSign(self):
        self.assertEqual(self.feautureExtraction.hasAtSign(self.URL), 0)

    def test_hasHttps(self):
        self.assertEqual(self.feautureExtraction.hasHttps(self.URL), 1)

    def test_getHostLength(self):
        self.assertEqual(self.feautureExtraction.getHostLength(self.URL), 17)

    def test_hasHyphenOrUnderscore(self):
        self.assertEqual(
            self.feautureExtraction.hasHyphenOrUnderscore(self.URL), 0)

    def test_getBaseUrlLength(self):
        self.assertEqual(
            self.feautureExtraction.getBaseUrlLength(self.URL), 22)

    def test_feautureExtraction(self):
        self.assertEqual(self.feautureExtraction.feautures,
                         [1, 0, 1, 17, 0, 22])

    def test_feautureExtractionWithLabel(self):
        self.feautureExtraction = UrlFeaturesWithLabel(self.URL, 1)
        self.assertEqual(self.feautureExtraction.feautures,
                         [1, 0, 1, 17, 0, 22, 1])


if __name__ == '__main__':
    unittest.main()
