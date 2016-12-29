import pyjsonrpc

URL = "http://localhost:5050/"

client = pyjsonrpc.HttpClient(url=URL)

def predict(bathroom, school_rating, bedroom, property_type, size,avg):
    predicted_value = client.call('predict', bathroom, school_rating, bedroom, property_type, size,avg)
    print "Predicted value: %f" % predicted_value
    return predicted_value
