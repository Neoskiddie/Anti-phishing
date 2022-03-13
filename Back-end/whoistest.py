import whois
import traceback
import datetime
from dateutil.relativedelta import relativedelta  # needed to easily add one year to today's data


# https://www.supportsages.com/whois-the-best-explanation-ever-multiple-expiration-dates/
def has_short_expiry(url: str):
    """
    Query whois for domain expiry and return 1 if shorter than a year.
    Notice from whois:
    'The expiration date displayed in this record is the date the
    registrar's sponsorship of the domain name registration in the registry is
    currently set to expire. This date does not necessarily reflect the expiration
    date of the domain name registrant's agreement with the sponsoring
    registrar.  Users may consult the sponsoring registrar's Whois database to
    view the registrar's reported date of expiration for this registration.'

    :param url: url of the website to check
    :return: 1 if expiry in less than a year
    """
    whois_data = whois.whois(url)
    # print(whois_data)
    expiration_date = whois_data.expiration_date
    date_in_one_year = datetime.datetime.today() + relativedelta(years=1)
    print('The date in one year: ' + str(date_in_one_year))
    # depending on the record whois either returns a list of datatime, or datetime
    # this is handling that
    print('The expiration date for ' + url + '\n is: ' + str(expiration_date))
    if type(expiration_date) is datetime.datetime:
        if expiration_date <= date_in_one_year:
            return 1
    else:
        for date in expiration_date:
            if date <= date_in_one_year:
                return 1
        return 0


def is_domain_young(url: str):
    """
    Query whois for domain age and if younger than 6 months return 1
    :param url: url of the website to check
    :return: 1 if expiry in less than a year
    """
    whois_data = whois.whois(url)
    creation_date = whois_data.creation_date
    datetime_six_month_ago = datetime.datetime.today() - relativedelta(months=6)
    print('The date six months ago: ' + str(datetime_six_month_ago))
    # depending on the record whois either returns a list of datatime, or datetime
    # this is handling that
    print('The creation date for ' + url + '\n is: ' + str(creation_date))
    if type(creation_date) is datetime.datetime:
        if creation_date >= datetime_six_month_ago:
            return 1
    else:
        for date in creation_date:
            if date >= datetime_six_month_ago:
                return 1
        return 0


def has_domain_record(url: str):
    try:
        whois_data = whois.whois(url)
        return 0
    except:
        return 1


#print(has_short_expiry(("google.com")))
#print(has_short_expiry(("skiddie.xyz")))
#print(has_short_expiry(("https://stackoverflow.com/questions/9195455/how-to-document-a-method-with-parameters")))
#
#print(is_domain_young(("google.com")))
#print(is_domain_young(("skiddie.xyz")))
print(has_domain_record("nothodfodsjf.com"))
print(has_domain_record("skiddie.xyz"))
