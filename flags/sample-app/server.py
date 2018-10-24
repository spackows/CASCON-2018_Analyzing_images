from flask import Flask, request, jsonify
import os

# <start> Pieces from notebook prototyping..
#

import json
from watson_developer_cloud import VisualRecognitionV3

model_id = '' # <-- PASTE YOUR MODEL ID HERE
apikey   = '' # <-- PASTE YOUR APIKEY HERE

def getKey( item ):
    return item["score"]

def getTopClass( results ):
    results_classes = results["images"][0]["classifiers"][0]["classes"]
    sorted_results_classes = sorted( results_classes, key=getKey, reverse=True )
    return sorted_results_classes[0]

def classifyFlag( flag_image_filename ):
    visual_recognition = VisualRecognitionV3( version='2018-03-19', iam_apikey=apikey )
    with open( flag_image_filename, 'rb' ) as image_file:
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

@app.route( '/recognize', methods=['GET'] )
def recognize():
    flag_id = request.args['flag_id']
    flag_image_filename = 'static/' + flag_id + '.jpg'
    print( 'flag_id:             ' + flag_id )
    print( 'flag_image_filename: ' + flag_image_filename )
    return jsonify( classifyFlag( flag_image_filename ) )

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
