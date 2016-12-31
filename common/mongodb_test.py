import mongodb_client

db = mongodb_client.getDB()

PROPERTY_TABLE_NAME = "property"

# db[PROPERTY_TABLE_NAME].replace_one({'test': 123}, 'property_detail', upsert=True)

result = db.test.delete_many({'test123':'123'})
# print result.deleted_count

print db.property.count()
