#!/usr/bin/python

import json

from flask import Flask
from flask import request
from flask import make_response

from google.appengine.ext import blobstore
from google.appengine.api import images

JSON_MIME_TYPE = 'application/json'

app = Flask(__name__)

@app.route('/image-url', methods=['GET'])
def image_url():
	bucket = request.args.get('bucket')
	image = request.args.get('image')

	if not all([bucket, image]):
		error = json.dumps({'error': 'Missing `bucket` or `image` parameter.'})
		return json_response(error, 422)

	filepath = (bucket + "/" + image)

	try:
		servingImage = images.get_serving_url(None, filename='/gs/' + filepath, secure_url=True)
	except images.AccessDeniedError:
		error = json.dumps({'error': 'Ensure the GAE service account has access to the object in Google Cloud Storage.'})
		return json_response(error, 401)
	except images.ObjectNotFoundError:
		error = json.dumps({'error': 'The object was not found.'})
		return json_response(error, 404)
	except images.TransformationError:
		# A TransformationError may happen in several scenarios - if
		# the file is simply too large for the images service to
		# handle, if the image service doesn't have access to the file,
		# or if the file was already uploaded to the image service by
		# another App Engine app. For the latter case, we can try to
		# work around that by copying the file and re-uploading it to
		# the image service.
		error = json.dumps({'error': 'There was a problem transforming the image. Ensure the GAE service account has access to the object in Google Cloud Storage.'})
		return json_response(error, 400)

	return json_response(json.dumps({'image_url': servingImage}))

def json_response(data='', status=200, headers=None):
	headers = headers or {}
	if 'Content-Type' not in headers:
		headers['Content-Type'] = JSON_MIME_TYPE

	return make_response(data, status, headers)
