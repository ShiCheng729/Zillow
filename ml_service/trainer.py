import numpy as np
import pandas
import sys
import tensorflow as tf

from ml_common import *
from IPython import display

# Training Parameter
LEARNING_RATE = 200
STEPS = 10000

CSV_FILE_PATH = '''./test.csv'''

CSV_FILE_FORMAT = {
    'bathroom': np.float32, 
    'list_price': np.float32,
    'school_rating': np.float32,
    'bedroom': np.float32,
    'property_type': str,
    'size': np.float32,
    'avg': np.float32
}

MODEL_OUTPUT_DIR = "./model/"

# Set the output display to have one digit for decimal places, for display readability only.
pandas.options.display.float_format = '{:.1f}'.format

# Load in the data from CSV files.
property_dataframe = pandas.read_csv(CSV_FILE_PATH, dtype=CSV_FILE_FORMAT)


# Randomize the index.
property_dataframe = property_dataframe.reindex(
    np.random.permutation(property_dataframe.index))


# Pick out the columns we care about.
property_dataframe = property_dataframe[COLUMNS]

# Clean up data
property_dataframe = property_dataframe[property_dataframe['school_rating'] != 0]
property_dataframe = property_dataframe[property_dataframe['list_price'] != 0]
# Drop rows with any value NaN
property_dataframe = property_dataframe.dropna()


# Split data into training and test
train_dataframe = property_dataframe.sample(frac=0.9)
#test_dataframe = property_dataframe.drop(train_dataframe.index)
test_dataframe = property_dataframe.head(1)

train_features_label = train_dataframe[FEATURE_COLUMNS]
test_features_label = test_dataframe[FEATURE_COLUMNS]

feature_columns = [bathroom, school_rating, bedroom, property_type, size_buckets,avg]

linear_regressor = tf.contrib.learn.LinearRegressor(
    feature_columns=feature_columns,
    optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE),
    model_dir = MODEL_OUTPUT_DIR)

print "Training model..."

def input_fn_train():
    return input_fn(train_features_label)

linear_regressor.fit(input_fn=input_fn_train, steps=STEPS)

print "Model training finished."

print "Evaluating model..."
def input_fn_test():
    return input_fn(test_features_label)

print linear_regressor.evaluate(input_fn=input_fn_test, steps=10)
print "Model evaluation finished."
