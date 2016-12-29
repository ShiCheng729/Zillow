import mongodb_client

PROPERTY_TABLE_NAME = 'property'
db = mongodb_client.getDB()
record = list(db.property.find({}))

db.getCollection('property').aggregate(
   [
     {
       '$group':
         {
           _id: "$zipcode",
           avgQuantity: { '$avg': {'$divide' : [ "$list_price","$size"]} }
         }
     }
   ]
)

print 'done'
