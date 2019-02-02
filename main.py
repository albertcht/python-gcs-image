#!/usr/bin/python

import json

from flask import Flask
from flask import request

from google.appengine.ext import blobstore
from google.appengine.api import images

app = Flask(__name__)

@app.route('/image-url', methods=['GET'])
def image_url():
	bucket = request.args.get('bucket')
	image = request.args.get('image')

	filename = (bucket + "/" + image)
	servingImage = images.get_serving_url(None, filename='/gs/' + filename)

	return(servingImage)
