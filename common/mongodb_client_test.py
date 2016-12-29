import mongodb_client

PROPERTY_TABLE_NAME = 'property'
db = mongodb_client.getDB()
record = list(db.property.find({}))
for re in record:
	idd = re['_id']
	r = re['zipcode']
	avg = db.average.find({'_id':r})
	m = avg[0]['avgQuantity']
	db[PROPERTY_TABLE_NAME].update({ '_id':idd},{'$set': { "avg": m}})

print 'done'