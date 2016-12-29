import zillow_web_scraper_client as client
import mongodb_client
import time
'''print client.get_zpid_by_zipcode("75080")'''

'''print client.search_zillow_by_city_state("San Francisco", "CA")'''

'''print client.get_property_by_zpid(80736607)'''

'''print client.get_properties_by_zip(94080)

print client.get_properties_by_city_state('San Bruno', 'CA')

print client.get_similar_homes_for_sale_by_id(2096630311)'''
property_detail = client.get_property_by_zpid(80736607)
property_detail['last_update'] = time.time()
PROPERTY_TABLE_NAME = 'property'
db = mongodb_client.getDB()
db[PROPERTY_TABLE_NAME].replace_one({'zpid': 80736607}, property_detail, upsert=True)