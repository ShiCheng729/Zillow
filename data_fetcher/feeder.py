import os
import sys
import time

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import zillow_api_client
import zillow_web_scraper_client

from cloudAMQP_client import CloudAMQPClient

# Automatically feed zpids into queue
### REPLACE CLOUD_AMQP_URL WITH YOUR OWN ###
CLOUD_AMQP_URL = '''amqp://gbomelox:1v13-VN_Mv4cjNc4E_Foc4I4Vqp5dz2e@zebra.rmq.cloudamqp.com/gbomelox'''
DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'
ZIPCODE_FILE = 'bay_area_zipcode_list.txt'

WAITING_TIME = 1

cloudAMQP_client = CloudAMQPClient(CLOUD_AMQP_URL, DATA_FETCHER_QUEUE_NAME)

zipcode_list = []

with open(ZIPCODE_FILE, 'r') as zipcode_file:
    for zipcode in zipcode_file:
        zipcode_list.append(str(zipcode))

for zipcode in zipcode_list:
    zpids = zillow_web_scraper_client.get_zpid_by_zipcode(zipcode)
    time.sleep(WAITING_TIME)

    for zpid in zpids:
    	time.sleep(WAITING_TIME)
    	zpid = zpid[5:]
        cloudAMQP_client.sendDataFetcherTask({'zpid': zpid})

