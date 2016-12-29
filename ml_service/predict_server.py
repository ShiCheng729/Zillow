import numpy as np
import pandas
import pyjsonrpc
import tensorflow as tf
import time

from ml_common import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

MODEL_DIR = './model'
MODEL_UPDATE_LAG = 5

linear_regressor = tf.contrib.learn.LinearRegressor(
    feature_columns=feature_columns,
    model_dir=MODEL_DIR)

print "Model loaded"

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print "Model update detected. Loading new model."
        time.sleep(MODEL_UPDATE_LAG)
        linear_regressor = tf.contrib.learn.LinearRegressor(
            feature_columns=feature_columns,
            model_dir=MODEL_DIR)
        print "Model updated."

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test method"""
    @pyjsonrpc.rpcmethod
    def predict(self, bathroom, school_rating, bedroom, property_type, size,avg):
        sample = pandas.DataFrame({
            'bathroom': bathroom,
            'school_rating': school_rating,
            'bedroom': bedroom,
            'property_type': property_type,
            'size': size, 
            'avg': avg,
            'list_price':0}, index=[0])
        def input_fn_predict():
            return input_fn(sample)
        prediction = linear_regressor.predict(input_fn=input_fn_predict)
        #print prediction
        for i in prediction:
            print i
            break
        return float(i)

# Setup watchdog
#observer = Observer()
#observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
#observer.start()

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting predicting server ..."
print "URL: http://" + str(SERVER_HOST) + ":" + str(SERVER_PORT)

http_server.serve_forever()
