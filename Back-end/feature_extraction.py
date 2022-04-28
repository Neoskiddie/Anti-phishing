"""
This file contains the feature extraction class that is used by the API to process
each request and to create the dataset. If this file is run on its own, it creates
the training_dataset.csv and testing_dataset.csv from  Benign_list_big_final.csv and merged.csv

based on:
https://github.com/Chandni97/PhishDetect/blob/master/extract_feature.py
https://github.com/ESDAUNG/Phishing-URL-Detection/blob/main/Feature_extraction.java
https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/URL%20Feature%20Extraction.ipynb
"""
# Helper libraries
import pandas as pd
import re
import csv
import numpy as np

# libraries for parsing the URLs
from urllib.parse import urlparse

class UrlFeatures():
    features = []

    def __init__(self, url: str):
        self.set_features_list(url)

    def has_ip(self, url):
        '''
        Code from https://gist.github.com/dfee/6ed3a4b05cfe7a6faf40a2102408d5d8
        slightly modified to detect IPv4 on it's own. Because it's enough to detect IPv4 on it's own, the embedded cases were deleted, as they are detected anyway.
        https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
        '''
        IPV4SEG = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
        IPV4ADDR = r'(?:(?:' + IPV4SEG + r'\.){3,3}' + IPV4SEG + r')'
        IPV6SEG = r'(?:(?:[0-9a-fA-F]){1,4})'
        IPV6GROUPS = (
            r'(?:' + IPV6SEG + r':){7,7}' + IPV6SEG,
            # 1::                                 1:2:3:4:5:6:7::
            r'(?:' + IPV6SEG + r':){1,7}:',
            # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
            r'(?:' + IPV6SEG + r':){1,6}:' + IPV6SEG,
            # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
            r'(?:' + IPV6SEG + r':){1,5}(?::' + IPV6SEG + r'){1,2}',
            # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
            r'(?:' + IPV6SEG + r':){1,4}(?::' + IPV6SEG + r'){1,3}',
            # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
            r'(?:' + IPV6SEG + r':){1,3}(?::' + IPV6SEG + r'){1,4}',
            # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
            r'(?:' + IPV6SEG + r':){1,2}(?::' + IPV6SEG + r'){1,5}',
            # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
            IPV6SEG + r':(?:(?::' + IPV6SEG + r'){1,6})',
            # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
            r':(?:(?::' + IPV6SEG + r'){1,7}|:)',
            # fe80::7:8%eth0     fe80::7:8%1  (link-local IPv6 addresses with zone index)
            r'fe80:(?::' + IPV6SEG + r'){0,4}%[0-9a-zA-Z]{1,}',
            IPV4ADDR
        )
        # Reverse rows for greedy match
        IPV6ADDR = '|'.join(['(?:{})'.format(g) for g in IPV6GROUPS[::-1]])
        match = re.search(IPV6ADDR, url)  # Ipv6
        if match:
            return 1
        else:
            return 0

    def is_url_short(self, url):
        """Simple method that does regex search for a list of URL shortening domains
        The basic list was taken from https://github.com/Chandni97/PhishDetect/blob/master/extract_feature.py
        combined with list from https://meta.stackoverflow.com/questions/313621/blacklist-the-use-of-common-link-shorteners-in-posts
        there are likely duplicates form both lists"""
        match = re.search(
            'zi\.mu|zi\.ma|yhoo\.it|yfrog\.com|yep\.it|y\.ahoo\.it|xurl\.es|xrl\.us|'
            'xrl\.in|wp\.me|url\.ie|url\.co\.uk|url\.az|ur1\.ca|u\.nu|twurl\.nl|twurl\.cc|'
            'tr\.im|to\.ly|tnij\.org|tinyurl\.com|tinylink\.in|tiny\.pl|tiny\.ly|tiny\.cc|'
            'tcrn\.ch|ta\.gd|t\.co|t\.cn|su\.pr|sp2\.ro|snurl\.com|snipurl\.com|snipr\.com|'
            'shrt\.st|shorturl\.com|short\.ie|shorl\.com|shar\.es|sameurl\.com|safe\.mn|post\.ly|'
            'ping\.fm|ow\.ly|om\.ly|nyti\.ms|nsfw\.in|moby\.to|migre\.me|lnkd\.in|linkbun\.ch|'
            'linkbee\.com|liip\.to|krunchd\.com|korta\.nu|j\.mp|is\.gd|hurl\.me|huff\.to|goo\.gl|'
            'fwd4\.me|fff\.to|ff\.im|fb\.me|fav\.me|eepurl\.com|doiop\.com|dlvr\.it|disq\.us|'
            'digg\.com|digbig\.com|decenturl\.com|cutt\.us|cot\.ag|cli\.gs|clck\.ru|cl\.ly|'
            'chilp\.it|budurl\.com|bit\.ly|binged\.it|bacn\.me|arst\.ch|alturl\.com|afx\.cc|'
            'adjix\.com|adf\.ly|4sq\.com|3\.ly|0rz\.tw|we\.tl|ouo\.io|bfy\.tw|bit\.do|'
            'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
            'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
            'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
            'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
            'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
            'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
            'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net|shorturl\.at', url)
        if match:
            return 1
        else:
            return 0

    def get_dots_in_hostname(self, url):
        """Basic idea is that more dots in domain part = Sub Domain and Multi Sub Domains"""
        return urlparse(url).netloc.count(".")

    def has_at_sign(self, url):
        if "@" in url:
            return 1
        return 0

    # def has_double_slash(self, url):
    #    if "//" in urlparse(url).netloc:
    #        return 1
    #    return 0

    def has_double_slash(self, url):
        # since the position starts from, we have given 6 and not 7 which is according to the document
        list = [x.start(0) for x in re.finditer('//', url)]
        if list[len(list)-1] > 6:
            return 1
        else:
            return 0

    def has_hyphen_domain(self, url):
        if "-" in urlparse(url).netloc:
            return 1
        return 0

    def has_https(self, url):
        if urlparse(url).scheme == "https":
            return 1
        return 0

    def get_host_length(self, url):
        return len(urlparse(url).netloc)

    def has_hyphen_or_underscore(self, url):
        if ("_" in url or "-" in url):
            return 1
        return 0

    def get_base_url_length(self, url):
        parsedUrl = urlparse(url)
        return len(parsedUrl.scheme) + len(parsedUrl.netloc) + len(parsedUrl.path)

    def get_features_list(self):
        return self.features

    def set_features_list(self, url):
        self.features = [
            self.has_ip(url),
            self.is_url_short(url),
            self.get_dots_in_hostname(url),
            self.has_at_sign(url),
            self.has_double_slash(url),
            self.has_hyphen_domain(url),
            self.has_https(url),
            self.get_host_length(url),
            self.has_hyphen_or_underscore(url),
            self.get_base_url_length(url),
        ]

    def get_features_names(self):
        """Get names of all the methods in the class as a list.
        This will be used as column names in the Dataframe.
        Doesn't seem to be better way than to call __name__ on each method.
        The best would be to somehow automatically call this on all methods in the class.
        But I don't know how to do it without overcomplicating things."""
        return [
            self.has_ip.__name__,
            self.is_url_short.__name__,
            self.get_dots_in_hostname.__name__,
            self.has_at_sign.__name__,
            self.has_double_slash.__name__,
            self.has_hyphen_domain.__name__,
            self.has_https.__name__,
            self.get_host_length.__name__,
            self.has_hyphen_or_underscore.__name__,
            self.get_base_url_length.__name__,
        ]


class UrlFeaturesWithLabel(UrlFeatures):
    def __init__(self, url: str, label: int):
        #self.features = self.get_features_list(url)
        self.set_features_list(url, label)

    def set_features_list(self, url, label):
        """Setting the features, same as base class
        and adding the label."""
        super().set_features_list(url)
        self.features.append(label)

    def get_features_names(self):
        """Overriding feature names and adding the label for classification"""
        feature_names = super().get_features_names()
        feature_names.append('is_phishing')
        # print(feature_names)
        return feature_names


def extract_features_from_csv(file_path: str, is_phishing: int, number_of_samples=None):
    """
    Extract features from a csv file and create pandas Data Frame.
    file_path - path to the csv file with a list of URLs only
    is_phishing - a flag used to mark whether the URL dataset contains phishing or not
    1 means phishing
    """
    RANDOM_STATE = 12
    features = []
    # encoding because of "UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d in position 7380: character maps to <undefined>"
    with open(file_path, 'r', encoding='cp850') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            # in the CSV file first item in first row should be the URL, thus the row[0]
            featureExtraction = UrlFeaturesWithLabel(row[0], is_phishing)
            features.append(featureExtraction.features)

    data = pd.DataFrame(
        features, columns=featureExtraction.get_features_names())
    if (number_of_samples is None):
        return data.sample(frac=1, random_state=RANDOM_STATE).copy()
    return data.sample(n=number_of_samples, random_state=RANDOM_STATE).copy()

# Split the dataset into a training and a testing dataset.


def split_dataset(dataset, random_seed, test_ratio=0.20):
    """Splits a panda dataframe in two."""
    np.random.seed(random_seed)
    test_indices = np.random.rand(len(dataset)) < test_ratio
    return dataset[~test_indices], dataset[test_indices]


if (__name__ == '__main__'):
    RANDOM_STATE = 12
    # settings to display all columns, used for debugging
    #pd.set_option('display.max_columns', None)
    legitURLs = extract_features_from_csv(
        './Data/Benign_list_big_final.csv', 0)
    phishingURLs = extract_features_from_csv('./Data/merged.csv', 1)
    print('Number of legitimate URLs: {}'.format(len(legitURLs)))
    print('Number of phishing URLs: {}'.format(len(phishingURLs)))
    #legitURLs = extract_features_from_csv('./Data/Benign_list_big_final.csv', 0,5000)
    #phishingURLs = extract_features_from_csv('./Data/phishing_dataset.csv', 1,5000)
    # Here, specifying drop=True prevents .reset_index from creating a column containing the old index entries.
    dataset = pd.concat([legitURLs, phishingURLs]).sample(
        frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    print('Total number of URLs: {}'.format(len(dataset)))
    train_ds_pd, test_ds_pd = split_dataset(dataset, RANDOM_STATE)

    print('{} URLs for training, {} URLs for testing.'.format(
        len(train_ds_pd), len(test_ds_pd)))
    train_ds_pd.to_csv('./Data/training_dataset.csv', index=False)
    test_ds_pd.to_csv('./Data/testing_dataset.csv', index=False)

# Number of legitimate URLs: 35378
# Number of phishing URLs: 19478
# Total number of URLs: 54856
# 43941 URLs for training, 10915 URLs for testing.
