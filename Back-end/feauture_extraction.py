
# Helper libraries
import pandas as pd
import time
import re

# libraries for parsing the URLs
import ipaddress
from urllib.parse import urlparse, urlencode
# https://github.com/Chandni97/PhishDetect/blob/master/extract_feature.py
# https://github.com/ESDAUNG/Phishing-URL-Detection/blob/main/Feature_extraction.java
# https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/URL%20Feature%20Extraction.ipynb
# apparently TensorFlow converts capital letters to lower letters, so no camel case
FEAUTURE_NAMES = [
    'number_of_dots_in_hostname',
    'has_at_sign',
    'has_https',
    'host_name_length',
    'has_hyphen_or_underscore',
    'base_url_length',
    'is_phishing',
]


class UrlFeautures():
    url = ''
    feautures = []

    def __init__(self, url: str):
        self.url = url
        self.feautures = self.extractFeautures()

    def has_ip(self, url):
        match = re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
                          # IPv4 in hexadecimal
                          '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
                          '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            return 1
        else:
            return 0

    def getDotsInHostname(self, url):
        return urlparse(url).netloc.count(".")

    def hasAtSign(self, url):
        if "@" in url:
            return 1
        return 0

    def hasHttps(self, url):
        if urlparse(url).scheme == "https":
            return 1
        return 0

    def getHostLength(self, url):
        return len(urlparse(url).netloc)

    def hasHyphenOrUnderscore(self, url):
        if ("_" in url or "-" in url):
            return 1
        return 0

    def getBaseUrlLength(self, url):
        parsedUrl = urlparse(url)
        return len(parsedUrl.scheme) + len(parsedUrl.netloc) + len(parsedUrl.path)

    def extractFeautures(self):
        return [
            self.getDotsInHostname(self.url),
            self.hasAtSign(self.url),
            self.hasHttps(self.url),
            self.getHostLength(self.url),
            self.hasHyphenOrUnderscore(self.url),
            self.getBaseUrlLength(self.url),
        ]


class UrlFeaturesWithLabel(UrlFeautures):
    def __init__(self, url: str, label: int):
        self.url = url
        self.feautures = self.extractFeautures()
        self.feautures.append(label)


class DataSet:
    RANDOM_STATE = 12

    def __init__(self, legitimate_URLs: pd.DataFrame, phishing_URLs: pd.DataFrame, numberOfSamples: int):
        self.legitURLs = legitimate_URLs
        self.phishingURLs = phishing_URLs
        self.numberOfSamples = numberOfSamples
        self.data = self.createDataSet()

    def createPhishingDataFrame(self):
        phishingFeatures = []
        is_phishing = 1

        phishurl = self.phishingURLs.sample(
            n=self.numberOfSamples, random_state=self.RANDOM_STATE).copy()
        phishurl = phishurl.reset_index(drop=True)

        for i in range(0, self.numberOfSamples):
            url = phishurl['url'][i]
            feautureExtraction = UrlFeaturesWithLabel(url, is_phishing)
            phishingFeatures.append(feautureExtraction.feautures)

        return pd.DataFrame(phishingFeatures, columns=FEAUTURE_NAMES)

    def createLegitimateDataFrame(self):
        legi_features = []
        is_phishing = 0

        # the data is asumed to have first column as 'url'
        self.legitURLs.columns = ['url']
        legiurl = self.legitURLs.sample(
            n=self.numberOfSamples, random_state=self.RANDOM_STATE).copy()
        legiurl = legiurl.reset_index(drop=True)

        for i in range(0, self.numberOfSamples):
            url = legiurl['url'][i]
            feautureExtraction = UrlFeaturesWithLabel(url, is_phishing)
            legi_features.append(feautureExtraction.feautures)

        return pd.DataFrame(legi_features, columns=FEAUTURE_NAMES)

    def createDataSet(self):
        # concat both of the sets
        legitimate = self.createLegitimateDataFrame()
        phishing = self.createPhishingDataFrame()
        return pd.concat([legitimate, phishing]).reset_index(drop=True)


# initialising it for colab to be avilable outside of this code block
urldata = pd.DataFrame()
if (__name__ == '__main__'):
    # settings to display all columns, used for debuging
    pd.set_option("display.max_columns", None)
    legitURLs = pd.read_csv("/tmp/legitUrls.csv")
    phishingURLs = pd.read_csv("/tmp/phishingUrls.csv")
    dataSet = DataSet(legitURLs, phishingURLs, 500)
    urldata = dataSet.data
