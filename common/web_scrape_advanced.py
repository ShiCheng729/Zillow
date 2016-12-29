import random
import re
import requests
import json
from decimal import Decimal
from lxml import html
from re import sub
from urllib import pathname2url
from PIL import Image
import urllib, cStringIO


URL = '''http://www.zillow.com'''
SEARCH_FOR_SALE_PATH = '''homes/for_sale'''
GET_PROPERTY_BY_ZPID_PATH = '''homes'''
GET_SIMILAR_HOMES_FOR_SALE_PATH = '''homedetails'''
IMAGE_URL_REGEX_PATTERN = '"z_listing_image_url":"([^"]+)",'
SIMILAR_HOMES_ZPID_REGEX_PATTERN ='zpid'

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



ALL_ZIPCODE_URL = '''http://www.zillow.com/homes/recently_sold'''
GET_SOLD_PRICE = '''//span[@class="zsg-photo-card-status"]/text()[1]'''
GET_HOUSE_PROPERTY = '''//p/span[@class='zsg-photo-card-info']/text()'''
GET_NEXT_PAGE='''//link[@rel= 'next']/@href'''
GET_IMAGE_URL='''//div[@class='zsg-photo-card-img']/img/@data-src'''
GET_ADDRESS='''//span[@itemprop='streetAddress']/text()'''


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

"""Get the zpid list from zipcode"""
def get_zpid_by_zipcode(zipcode):
    request_url = '%s/%s/%s' % (ALL_ZIPCODE_URL,str(zipcode),'10000-_price')
    session_requests = requests.session();
    response = session_requests.get(request_url, headers=getHeaders())
    try:
        tree = html.fromstring(response.content)
    except Exception:
        return 

    zpids = None
    try:
        zpids = tree.xpath(SEARCH_XPATH_FOR_ZPID)
    except Exception:
        pass

    prices = None
    try:
        prices = tree.xpath(GET_SOLD_PRICE)
    except Exception:
        pass

    prop = None
    try:
        prop = tree.xpath(GET_HOUSE_PROPERTY)
    except Exception:
        pass

    image = None
    try:
        image = tree.xpath(GET_IMAGE_URL)
    except Exception:
        pass

    hometype = None
    try:
        hometype = tree.xpath(GET_ADDRESS)
    except Exception:
        pass

    nextpage = None
    try:
        nextpage = tree.xpath(GET_NEXT_PAGE)
    except Exception:
        pass

    i = 0
    k = 0 
    for zpid in zpids:
        ps = prop[i*4+0]
        if 'Price/sqft: --' not in ps:
            ps = float(prop[i*4+0].replace('Price/sqft: $', ''))
            bds = prop[i*4+1]
            if 'Studio' not in bds:
                bds = float(prop[i*4+1][:2])
            else:
                bds = 1
            ba = float(prop[i*4+2].replace('ba',''))
            sqft = float(prop[i*4+3].replace('sqft','').replace(',',''))

            if i == 0:
                result = {i:[zpid,prices[i],ps,bds,ba,sqft,hometype[i],image[i]]}
            else:
                result[k] = [zpid.replace('zpid_',''),float(prices[i].replace('SOLD: $','').replace(',','')),ps,bds,ba,sqft,hometype[i],image[i]]
                k=k+1
            i=i+1
        else:
            i=i+1

    result['next'] = nextpage

    return result


def get_property_by_url(nexturl):
    request_url = '%s' % str(nexturl)
    session_requests = requests.session();
    response = session_requests.get(request_url, headers=getHeaders())
    try:
        tree = html.fromstring(response.content)
    except Exception:
        return 

    zpids = None
    try:
        zpids = tree.xpath(SEARCH_XPATH_FOR_ZPID)
    except Exception:
        pass

    prices = None
    try:
        prices = tree.xpath(GET_SOLD_PRICE)
    except Exception:
        pass

    prop = None
    try:
        prop = tree.xpath(GET_HOUSE_PROPERTY)
    except Exception:
        pass

    image = None
    try:
        image = tree.xpath(GET_IMAGE_URL)
    except Exception:
        pass

    hometype = None
    try:
        hometype = tree.xpath(GET_ADDRESS)
    except Exception:
        pass

    nextpage = None
    try:
        nextpage = tree.xpath(GET_NEXT_PAGE)
    except Exception:
        pass

    for t in hometype:
        if "APT" in t:
            t = 1
        else:
            t = 2

    i = 0
    for zpid in zpids:
        ps = prop[i*4+0]
        if 'Price/sqft: --' not in ps:
            ps = float(prop[i*4+0].replace('Price/sqft: $', ''))
            bds = prop[i*4+1]
            if 'Studio' not in bds:
                bds = float(prop[i*4+1][:2])
            else:
                bds = 1
            ba = float(prop[i*4+2].replace('ba',''))
            sqft = float(prop[i*4+3].replace('sqft','').replace(',',''))

            if i == 0:
                result = {i:[zpid,prices[i],ps,bds,ba,sqft,hometype[i],image[i]]}
            else:
                result[i] = [zpid.replace('zpid_',''),float(prices[i].replace('SOLD: $','').replace(',','')),ps,bds,ba,sqft,hometype[i],image[i]]
            i=i+1

    result['next'] = nextpage

    return result

""" Get property information by Zillow Property ID (zpid)"""
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






