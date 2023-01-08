"""
Not used in final project. Whois features extraction. Very slow.
"""
import whois
import traceback
import datetime
# needed to easily add one year to today's data
from dateutil.relativedelta import relativedelta
import tldextract


class WhoisFeatures(UrlFeatures):

    def __init__(self, url: str):
        self.set_features_list(url)

    def has_short_expiry(self, domain_record):
        """
        Query whois for domain expiry and return 1 if shorter than a year.
        Notice from whois:
        'The expiration date displayed in this record is the date the
        registrar's sponsorship of the domain name registration in the registry is
        currently set to expire. This date does not necessarily reflect the expiration
        date of the domain name registrant's agreement with the sponsoring
        registrar.  Users may consult the sponsoring registrar's Whois database to
        view the registrar's reported date of expiration for this registration.'

        :return: 1 if expiry in less than a year
        """

        if domain_record is None:
            return 0

        whois_data = domain_record
        # print(whois_data)

        expiration_date = whois_data.expiration_date
        if expiration_date is None:
            return 0
        date_in_one_year = datetime.datetime.today() + relativedelta(years=1)
        print('The date in one year: ' + str(date_in_one_year))
        # depending on the record whois either returns a list of datatime, or datetime
        # this is handling that
        print('The expiration date for is: ' + str(expiration_date))
        if type(expiration_date) is datetime.datetime:
            if expiration_date <= date_in_one_year:
                return 1
        else:
            date = expiration_date[0]
            if date <= date_in_one_year:
                return 1
            return 0
            # for date in expiration_date:
            #    #new_date = parser.parse(date)
            #    if date <= date_in_one_year:
            #        return 1
            # return 0

    def is_domain_young(self, domain_record):
        """
        Query whois for domain age and if younger than 6 months return 1
        :return: 1 if expiry in less than a year
        """
        if domain_record is None:
            return 0

        whois_data = domain_record
        print(whois_data)
        creation_date = whois_data.creation_date

        if creation_date is None:
            return 0

        datetime_six_month_ago = datetime.datetime.today() - relativedelta(months=6)
        print('The date six months ago: ' + str(datetime_six_month_ago))
        # depending on the record whois either returns a list of datatime, or datetime
        # this is handling that
        print('The creation date for is: ' + str(creation_date))
        if type(creation_date) is datetime.datetime:
            if creation_date >= datetime_six_month_ago:
                return 1
        else:
            new_date = creation_date[0]
            if new_date >= datetime_six_month_ago:
                return 1
            return 0
#            for date in creation_date:
#                #new_date = parser.parse(date)
#                new_date = date
#                if type(date) is str:
#                    print("This is the record with string: " + str(whois_data))
#                    #2007-05-30T23:13:24+0000Z
#                    new_date = datetime.datetime.strptime('2015-02-10T13:00:00Z', '%Y-%m-%dT%H:%M:%S+0000Z')
#                if new_date >= datetime_six_month_ago:
#                    return 1
#            return 0

    def get_domain_record(self, url: str):
        """
        :param url: url of the website to check
        """
        print("Domain record called")
        try:
            whois_data = whois.whois(url)
            return whois_data
        except:
            return None

    def has_domain_record(self, domain_record):
        if domain_record is None:
            return 0
        else:
            return 1

    def extract_domain_from_url(self, url: str):
        extracted = tldextract.extract(url)
        return extracted.registered_domain

    def get_features_names(self):
        """
        Get names of all the methods in the class as a list.
        """
        feature_names = super().get_features_names()
        feature_names.extend([
            self.has_domain_record.__name__,
            self.is_domain_young.__name__,
            self.has_short_expiry.__name__
        ])
        print(feature_names)
        return feature_names

    def set_features_list(self, url):
        super().set_features_list(url)
        domain = self.extract_domain_from_url(url)
        domain_record = self.get_domain_record(domain)
        if domain_record is None:
            # no record available, maybe set this to None?
            self.features.extend([0, 0, 0])
        else:
            self.features.extend([
                self.has_domain_record(domain_record),
                self.is_domain_young(domain_record),
                self.has_short_expiry(domain_record)
            ])
