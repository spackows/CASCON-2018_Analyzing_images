from flask import Flask, request, jsonify
import os

# <start> Pieces from notebook prototyping..
#

# import cv2
import re
import json
from watson_developer_cloud import VisualRecognitionV3

model_id = '' # <-- PASTE YOUR MODEL ID HERE
apikey   = '' # <-- PASTE YOUR APIKEY HERE

def applyColourThreshold( frame ):
    lower_green = ( 0, 0, 0 )
    upper_green = ( 90, 255, 255 )
    frame_hsv    = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV )
    frame_mask   = cv2.bitwise_not( cv2.inRange( frame_hsv, lower_green, upper_green ) )
    return frame_mask

def findContours( frame_mask ):
    im, contours_arr, heirarchy = cv2.findContours( frame_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    return contours_arr

def get_object_bounding_boxes( contours_arr ):
    object_bounding_boxes = []
    for c in contours_arr:
        ( center, radius ) = cv2.minEnclosingCircle(c)
        if ( radius > 20 ):
            row_begin = int(round(center[1])) - int(round(radius)) - 5;
            row_end   = int(round(center[1])) + int(round(radius)) + 5;
            col_begin = int(round(center[0])) - int(round(radius)) - 5;
            col_end   = int(round(center[0])) + int(round(radius)) + 5;
            if( ( row_begin > 0 ) and ( col_begin > 0 ) ):
                object_bounding_boxes.append( ( row_begin, row_end, col_begin, col_end ) )
    return object_bounding_boxes

def bounding_box_size( box ):
    return ( box[1] - box[0] )

def getBiggestBox( boxes ):
    biggest_box = boxes[0]
    for i in range( 1, len( boxes ) ):
        if( bounding_box_size( boxes[i] ) > bounding_box_size( biggest_box ) ):
            biggest_box = boxes[i]
    return biggest_box

def getCloseup( frame ):
    frame_mask   = applyColourThreshold( frame )
    contours_arr = findContours( frame_mask )
    bounding_box = getBiggestBox( get_object_bounding_boxes( contours_arr ) )
    closeup      = frame[ bounding_box[0]:bounding_box[1], bounding_box[2]:bounding_box[3] ]
    return closeup

def saveCloseup( filename ):
    frame = cv2.imread( filename )
    closeup = getCloseup( frame )
    new_filename = re.sub( '.jpg', '', filename ) + '_closeup.png'
    cv2.imwrite( new_filename, closeup )
    return new_filename

def getKey( item ):
    return item["score"]

def getTopClass( results ):
    results_classes = results["images"][0]["classifiers"][0]["classes"]
    sorted_results_classes = sorted( results_classes, key=getKey, reverse=True )
    return sorted_results_classes[0]

def classifyObject( filename ):
    visual_recognition = VisualRecognitionV3( version='2018-03-19', iam_apikey=apikey )
    with open( filename, 'rb' ) as image_file:
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

@app.route( '/idobject', methods=['GET'] )
def idobject():
    video_id = request.args['vid_id']
    frame_filename  = 'static/' + video_id + '_frame.jpg'
    print( 'video_id:          ' + video_id )
    print( 'frame_filename: ' + frame_filename )
    #closeup_filename = saveCloseup( frame_filename )
    closeup_filename = re.sub( '.jpg', '_closeup.png', frame_filename )
    return jsonify( classifyObject( closeup_filename ) )

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
