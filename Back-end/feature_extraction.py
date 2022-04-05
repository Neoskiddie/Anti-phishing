
# Helper libraries
import pandas as pd
import re

# libraries for parsing the URLs
from urllib.parse import urlparse
# https://github.com/Chandni97/PhishDetect/blob/master/extract_feature.py
# https://github.com/ESDAUNG/Phishing-URL-Detection/blob/main/Feature_extraction.java
# https://github.com/shreyagopal/Phishing-Website-Detection-by-Machine-Learning-Techniques/blob/master/URL%20Feature%20Extraction.ipynb


class UrlFeautures():

    def __init__(self, url: str):
        self.set_feautures_list(url)

    def has_ip(self, url):
        '''
        Code from https://gist.github.com/dfee/6ed3a4b05cfe7a6faf40a2102408d5d8
        slightly modified to detect IPv4 on it's own. Because it's enough to detect IPv4 on it's own, the embeded cases were deleted, as they are detected anyway.
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

    def get_feautures_list(self):
        return self.feautures

    def set_feautures_list(self, url):
        self.feautures = [
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

    def get_feautures_names(self):
        """Get names of all the methods in the class as a list.
        This will be used as column names in the Dataframe.
        Doesn't seem to be better way than to call __name__ on each method.
        The best would be to somehow automatically call this on all methods in the class.
        But I don't know how to do it without overcomplicaitng things."""
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


class UrlFeaturesWithLabel(UrlFeautures):
    def __init__(self, url: str, label: int):
        #self.feautures = self.get_feautures_list(url)
        self.set_feautures_list(url, label)

    def set_feautures_list(self, url, label):
        """Setting the feautures, same as base class
        and adding the label."""
        super().set_feautures_list(url)
        self.feautures.append(label)

    def get_feautures_names(self):
        """Overriding feauture names and adding the label for clasificaiton"""
        feauture_names = super().get_feautures_names()
        feauture_names.append('is_phishing')
        print(feauture_names)
        return feauture_names


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

        return pd.DataFrame(phishingFeatures, columns=feautureExtraction.get_feautures_names())

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

        return pd.DataFrame(legi_features, columns=feautureExtraction.get_feautures_names())

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
    dataSet = DataSet(legitURLs, phishingURLs, 5000)
    urldata = dataSet.data
