import unittest
from feauture_extraction import *


class TestFeautureExtraction(unittest.TestCase):
    URL = "https://stackoverflow.com"
    EXAMPLE_URLS = [
        'https://attraction.example.com/books.php',
        'http://www.example.com/',
        'https://www.example.com/attack/arithmetic',
        'http://www.example.com/',
        'https://account.example.org/?apparel=achiever&bird=bird',
        'https://airplane.example.com/',
        'http://www.example.com/arch/appliance.php',
        'https://example.com/',
        'http://www.example.org/?bells=babies&bed=bike#baseball',
        'https://example.com/books.aspx',
    ]

    feautureExtraction = UrlFeautures(URL)

    def test_has_ip(self):
        ipList = ['1::',
                  '1:2:3:4:5:6:7::',
                  '1::8',
                  '1:2:3:4:5:6::8',
                  '1:2:3:4:5:6::8',
                  '1::7:8',
                  '1:2:3:4:5::7:8',
                  '1:2:3:4:5::8',
                  '1::6:7:8',
                  '1:2:3:4::6:7:8',
                  '1:2:3:4::8',
                  '1::5:6:7:8',
                  '1:2:3::5:6:7:8',
                  '1:2:3::8',
                  '1::4:5:6:7:8',
                  '1:2::4:5:6:7:8',
                  '1:2::8',
                  '1::3:4:5:6:7:8',
                  '1::3:4:5:6:7:8',
                  '1::8',
                  '::2:3:4:5:6:7:8',
                  '::2:3:4:5:6:7:8',
                  '::8',
                  '::',
                  'fe80::7:8%eth0',
                  'fe80::7:8%1',
                  '::255.255.255.255',
                  '::ffff:255.255.255.255',
                  '::ffff:0:255.255.255.255',
                  '2001:db8:3:4::192.0.2.33',
                  '64:ff9b::192.0.2.33',
                  '153.62.233.175',
                  '190.221.197.185',
                  '74.113.230.232',
                  '200.111.165.133',
                  '162.183.161.107',
                  '186.46.169.111',
                  '2.212.33.13',
                  '185.131.172.72',
                  '95.90.247.222',
                  '147.81.126.149',
                  '0:0:0:0:0:0:10.0.0.1'
                  ]

        for ip in ipList:
            self.assertEqual(self.feautureExtraction.has_ip(ip), 1)
        for url in self.EXAMPLE_URLS:
            self.assertEqual(self.feautureExtraction.has_ip(url), 0)

        self.assertEqual(self.feautureExtraction.has_ip(
            'https://stackoverflow.com'), 0)
        self.assertEqual(self.feautureExtraction.has_ip(
            'http://1563:6ae1:4cab:a557:0d6d:af67:6b44:2be1/2/paypal.ca/index.html'), 1)
        self.assertEqual(self.feautureExtraction.has_ip(
            '1563:6ae1:4cab:a557:0d6d:af67:6b44:2be1'), 1)
        self.assertEqual(self.feautureExtraction.has_ip(
            'http://125.98.3.123/fake.html'), 1)

    def test_is_url_short(self):
        shortUrls = [
            'https://t.co/G8QZxw7wS1',
            'https://bit.ly/3M8uKLz',
            'https://tinyurl.com/yckt9f9s',
            'http://tiny.cc/h12puz',
            'shorturl.at/uxMQ6',
        ]
        for url in shortUrls:
            self.assertEqual(self.feautureExtraction.is_url_short(url), 1)

        for example_url in self.EXAMPLE_URLS:
            self.assertEqual(
                self.feautureExtraction.is_url_short(example_url), 0)

    def test_getDotsInHostname(self):
        self.assertEqual(
            self.feautureExtraction.get_dots_in_hostname(self.URL), 1)

    def test_hasAtSign(self):
        URL_WITH_AT_SIGN = 'http://www.legitimate.com@http://www.phishing.com'
        self.assertEqual(
            self.feautureExtraction.has_at_sign(URL_WITH_AT_SIGN), 1)
        self.assertEqual(self.feautureExtraction.has_at_sign(self.URL), 0)

    def test_has_double_slash(self):
        URL_WITH_AT_REDIRECT = 'http://www.legitimate.com//http://www.phishing.com'
        self.assertEqual(
            self.feautureExtraction.has_double_slash(URL_WITH_AT_REDIRECT), 1)
        self.assertEqual(self.feautureExtraction.has_double_slash(self.URL), 0)

    def test_has_hyphen_domain(self):
        self.assertEqual(
            self.feautureExtraction.has_hyphen_domain(self.URL), 0)
        self.assertEqual(self.feautureExtraction.has_hyphen_domain(
            "http://www.confirme-paypal.com/."), 1)
        self.assertEqual(self.feautureExtraction.has_hyphen_domain(
            "http://www.example.com/some-test-path/just-trying."), 0)

    def test_hasHttps(self):
        self.assertEqual(self.feautureExtraction.has_https(self.URL), 1)

    def test_getHostLength(self):
        self.assertEqual(self.feautureExtraction.get_host_length(self.URL), 17)

    def test_hasHyphenOrUnderscore(self):
        self.assertEqual(
            self.feautureExtraction.has_hyphen_or_underscore(self.URL), 0)

    def test_getBaseUrlLength(self):
        self.assertEqual(
            self.feautureExtraction.get_base_url_length(self.URL), 22)

#    def test_feautureExtraction(self):
#        self.assertEqual(self.feautureExtraction.feautures,
#                         [1, 0, 1, 17, 0, 22])
#
#    def test_feautureExtractionWithLabel(self):
#        self.feautureExtraction = UrlFeaturesWithLabel(self.URL, 1)
#        self.assertEqual(self.feautureExtraction.feautures,
#                         [1, 0, 1, 17, 0, 22, 1])


if __name__ == '__main__':
    unittest.main()
