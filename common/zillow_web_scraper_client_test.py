import zillow_web_scraper_client as client
import time

# while True:
print client.get_property_by_zpid(83154148)
time.sleep(3)

# print client.search_zillow_by_zip("94051")
print client.search_zillow_by_zip("94015")
time.sleep(3)

print client.search_zillow_by_city_state("San Francisco", "CA")
time.sleep(3)
#
# #
# print client.get_properties_by_zip(94080)
#
# print client.get_properties_by_city_state('San Bruno', 'CA')
#
# print client.get_similar_homes_for_sale_by_id(2096630311)
