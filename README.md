Resizing and Serving images with Google Cloud Platform
==================================

Google Cloud storage can do a lot of interesting things by itself. If you combine it with [Images Python API](https://developers.google.com/appengine/docs/python/images/), you can use the =sXXX param to get properly scaled images that you can use for various breakpoints via picture or src-set.

## Setup

1. Clone this repo.

```
git clone https://github.com/albertcht/image-resize-gae.git
```

2. Install the requirements. (Flask)

```
pip install -r requirements.txt -t lib
```

3. Deploy to App Engine.

```
gcloud deploy
```

## Usage

1. Get a serving url from existed file on Google Cloud Storage:

```
curl https://PROJECT_NAME.appspot.com/image-url?bucket=mybuckey&image=image_name.jpg
```

2. It will return a url that looks something like:

```
https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg
```

## Reminders

1. Only one app can "own" the image. As stated in the [documentation](https://developers.google.com/appengine/docs/python/images/functions) for get_serving_url:

> If you serve images from Google Cloud Storage, you cannot serve an image from two separate apps. Only the first app that calls get_serving_url on the image can get the URL to serve it because that app has obtained ownership of the image.

2. Can't scale images up above 2560 pixels.

3. The serving url is inherently public (no support for private serving urls).
