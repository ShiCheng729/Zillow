import random
import re
import requests

from decimal import Decimal
from lxml import html
from re import sub
from urllib import pathname2url


URL = '''http://www.zillow.com'''
SEARCH_FOR_SALE_PATH = '''homes/for_sale'''
GET_PROPERTY_BY_ZPID_PATH = '''homes'''
GET_SIMILAR_HOMES_FOR_SALE_PATH = '''homedetails'''
IMAGE_URL_REGEX_PATTERN = '"z_listing_image_url":"([^"]+)",'
SIMILAR_HOMES_ZPID_REGEX_PATTERN ='\/(\d+)_zpid'

SEARCH_XPATH_FOR_ZPID = '''//div[@id='list-results']/div[@id='search-results']/ul[@class='photo-cards']/li/article/@id'''
GET_INFO_XPATH_FOR_STREET_ADDR = '''//header[@class='zsg-content-header addr']/h1[@class='notranslate']/text()'''
GET_INFO_XPATH_FOR_CITY_STATE_ZIP = '''//header[@class='zsg-content-header addr']/h1[@class='notranslate']/span/text()'''
GET_INFO_XPATH_FOR_TYPE = '''//div[@class='loan-calculator-container']/div/@data-type'''
GET_INFO_XPATH_FOR_BEDROOM = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][1]/text()'''
GET_INFO_XPATH_FOR_BATHROOM = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][2]/text()'''
GET_INFO_XPATH_FOR_SIZE = '''//header[@class='zsg-content-header addr']/h3/span[@class='addr_bbs'][3]/text()'''
GET_INFO_XPATH_FOR_SALE = '''//div[@id='home-value-wrapper']/div[@class='estimates']/div/text()'''
GET_INFO_XPATH_LIST_FOR_PRICE = '''//div[@id='home-value-wrapper']/div[@class='estimates']/div[@class='main-row  home-summary-row']/span/text()'''
GET_INFO_XPATH_FOR_LATITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='latitude']/@content'''
GET_INFO_XPATH_FOR_LONGITUDE = '''//div[@class='zsg-layout-top']/p/span/span[@itemprop='geo']/meta[@itemprop='longitude']/@content'''
GET_INFO_XPATH_DESCRIPTION = '''//div[@class='zsg-lg-2-3 zsg-md-1-1 hdp-header-description']/div[@class='zsg-content-component']/div/text()'''
GET_INFO_XPATH_FOR_FACTS = '''//div[@class='fact-group-container zsg-content-component top-facts']/ul/li/text()'''
GET_INFO_XPATH_FOR_ADDITIONAL_FACTS = '''//div[@class='fact-group-container zsg-content-component z-moreless-content hide']/ul/li/text()'''
GET_SIMILAR_HOMES_FOR_SALE_XPATH = '''//ol[@id='fscomps']/li/div[@class='zsg-media-img']/a/@href'''


# Load user agents
USER_AGENTS_FILE = '../common/user_agents.txt'
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip())
random.shuffle(USER_AGENTS)

def build_url(url, path):
    if url[-1] == '/':
        url = url[:-1]
    return '%s/%s' % (url, path)

def getHeaders():
    ua = random.choice(USER_AGENTS)  # select a random user agent
    headers = {
        "Connection" : "close",
        "User-Agent" : ua
    }
    return headers


""" Get property information by Zillow Property ID (zpid) """
def get_property_by_zpid(zpid):
    request_url = '%s/%s_zpid' % (build_url(URL, GET_PROPERTY_BY_ZPID_PATH), str(zpid))
    session_requests = requests.session()
    response = session_requests.get(request_url, headers=getHeaders())
    try:
        tree = html.fromstring(response.content)
    except Exception:
        return {}

    # Street address
    street_address = None
    try:
        street_address = tree.xpath(GET_INFO_XPATH_FOR_STREET_ADDR)[0].strip(', ')
    except Exception:
        pass

    return {'zpid':zpid,'street_address': street_address}






