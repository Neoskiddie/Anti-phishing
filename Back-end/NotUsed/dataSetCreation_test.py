"""
Unfinished class used to test URL processing.
"""
import pandas as pd
import pandas.testing as pd_testing
import numpy as np
import unittest
import feauture_extraction as fe

NUMBER_OF_SAMPLES = 2


class TestFeautureExtraction(unittest.TestCase):
    def setUp(self):
        self.legitURLs = pd.DataFrame(
            data={
                "url": [
                    "https://www.google.com",
                    "https://stackoverflow.com",
                ]
            }
        )

        self.phishingURLs = pd.DataFrame(
            data={
                "url": [
                    "http://www.g00gle.invalid.com/",
                    "http://www.stackoverf1ow.invalid.com",
                ]
            }
        )

        self.set = fe.DataSet(
            self.legitURLs, self.phishingURLs, NUMBER_OF_SAMPLES)

    def test_legitURLs(self):
        # TODO: It's BROKEN, fix it
        # not sure why but when creating np array it's using int32, while the one
        # from the DataFrame is int64, so need to specify that here
        # This test compares output of the feautre extractiona against an array of hardcoded values.
        # self.has_ip(url),
        # self.is_url_short(url),
        # self.getDotsInHostname(url),
        # self.hasAtSign(url),
        # self.has_double_slash(url),
        # self.has_hyphen_domain(url),
        # self.hasHttps(url),
        # self.getHostLength(url),
        # self.hasHyphenOrUnderscore(url),
        # self.getBaseUrlLength(url),
        testData = np.array([[0, 0, 2, 0, 1, 0, 0, 0, 0, 14, 0, 19, 0],
                             [0, 0, 1, 0, 1, 17, 0, 22, 0]], dtype=np.int64)
        testDataFrame = pd.DataFrame(
            testData, columns=fe.UrlFeaturesWithLabel.getFeauturesNames())
        pd_testing.assert_frame_equal(
            self.set.createLegitimateDataFrame(), testDataFrame)

    def test_phishingURLs(self):
        # not sure why but when creating np array it's using int32, while the one
        # from the DataFrame is int64, so need to specify that here
        testData = np.array([[0, 0, 3, 0, 0, 22, 0, 27, 1],
                             [0, 0, 3, 0, 0, 29, 0, 33, 1]], dtype=np.int64)
        testDataFrame = pd.DataFrame(
            testData, columns=fe.UrlFeaturesWithLabel.getFeauturesNames())
        pd_testing.assert_frame_equal(
            self.set.createPhishingDataFrame(), testDataFrame)


if __name__ == "__main__":
    unittest.main()
