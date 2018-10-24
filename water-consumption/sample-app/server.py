from flask import Flask, request, jsonify
import os

# <start> Pieces from notebook prototyping..
#

from PIL import Image
import re
from watson_developer_cloud import VisualRecognitionV3
import json

model_id = '' # <-- PASTE YOUR MODEL ID HERE
apikey   = '' # <-- PASTE YOUR APIKEY HERE

def saveSmallImage( filename ):
    full_im     = Image.open( filename )
    cropped_im  = full_im.crop( [50, 50, 1450, 1450 ] )
    small_im    = cropped_im.resize( [ 224, 224 ], resample=Image.LANCZOS )
    sm_filename = re.sub( '\.JPG', '', filename ) + '_sm.jpg'
    small_im.save( sm_filename, format="JPEG" )
    return sm_filename

def getKey( item ):
    return item["score"]

def getTopClass( results ):
    results_classes = results["images"][0]["classifiers"][0]["classes"]
    sorted_results_classes = sorted( results_classes, key=getKey, reverse=True )
    return sorted_results_classes[0]

def classifyImage( image_filename_sm ):
    visual_recognition = VisualRecognitionV3( version='2018-03-19', iam_apikey=apikey )
    with open( image_filename_sm, 'rb' ) as image_file:
        results = visual_recognition.classify( image_file, threshold='0', classifier_ids=model_id ).get_result()
        print( 'Results:')
        print( json.dumps( results, indent=3 ) )
        top_class = getTopClass( results )
        return { 'top_class' : top_class, 'results' : results }

# <end> Pieces from notebook prototyping..
#


app = Flask( __name__, static_url_path='' )

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int( os.getenv( 'PORT', 8000 ) )

@app.route('/')
def root():
    return app.send_static_file( 'index.html' )

@app.route( '/idanimal', methods=['GET'] )
def idanimal():
    image_id = request.args['image_id']
    image_filename = 'static/' + image_id + '.JPG'
    print( 'image_id:          ' + image_id )
    print( 'image_filename:    ' + image_filename )
    image_filename_sm = saveSmallImage( image_filename )
    print( 'image_filename_sm: ' + image_filename_sm )
    return jsonify( classifyImage( image_filename_sm ) )

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
