Resizing and Serving images with Google Cloud Platform
==================================

Resize your image files on Google Cloud storage with [Images Python API](https://developers.google.com/appengine/docs/python/images/) powered by Google.

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
gcloud app deploy
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

2. The serving url is inherently public (no support for private serving urls).

3. By default it returns an image of a maximum length of 512px. [(link)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg)

4. By appending the =sXX to the end of it where XX can be any integer in the range of 0–2560 and it will result to scale down the image to longest dimension without affecting the original aspect ratio. [(link =s256)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=s256)

5. By appending =sXX-c a cropped version of that image is being returned as a response. [(link =s400-c)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=s400-c)

6. By appending =s0 (s zero) the original image is being returned without any resize or modification. [(link =s0)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=s0)
