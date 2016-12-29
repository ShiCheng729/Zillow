import web_scrape_advanced as client

url = client.get_zpid_by_zipcode(75080).get('next')[0]

print client.get_property_by_url(url)