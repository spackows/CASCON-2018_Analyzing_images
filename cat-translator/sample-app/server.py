from flask import Flask, request, jsonify
import os

# <start> Pieces from notebook prototyping..
#
import tensorflow as tf
from tensorflow import keras
import numpy as np

class_names = [ "feedme", "opendoor" ]

model = tf.keras.models.load_model( "trained-model" )

def classifySpectrogram( filename ):
    img = tf.keras.utils.load_img( filename, target_size = ( 224, 224 ) )
    img_array = tf.keras.utils.img_to_array( img )
    img_array = tf.expand_dims( img_array, 0 )
    predictions = model.predict( img_array )
    score = tf.nn.softmax( predictions[0] )
    classification = class_names[ np.argmax( score ) ]
    confidence = str( round( 100 * np.max( score ), 3 ) ) + "%"
    return { 'top_class' : classification, 'confidence' : confidence }
    

# <end> Pieces from notebook prototyping..
#


app = Flask( __name__, static_url_path='' )

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int( os.getenv( 'PORT', 8000 ) )

@app.route('/')
def root():
    return app.send_static_file( 'index.html' )

@app.route( '/translate', methods=['GET'] )
def translate():
    vid_id = request.args['vid_id']
    video_file_name = 'static/' + vid_id + '.mp4'
    spec_file_name  = 'static/' + vid_id + '.spec.png'
    print( 'vid_id:          ' + vid_id )
    print( 'video_file_name: ' + video_file_name )
    print( 'spec_file_name:  ' + spec_file_name )
    return jsonify( classifySpectrogram( spec_file_name ) )

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
