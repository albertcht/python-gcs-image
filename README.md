Resizing and Serving images on Google Cloud Storage
==================================

Resize your image files on Google Cloud storage with [Images Python API](https://developers.google.com/appengine/docs/python/images/) powered by Google.

### Important note ☢️

This project runs on the App Engine Python 2.7 Runtime and, even though Python 2.7 is not maintaned anymore, Google has [committed to providing long term support for the App Engine Python 2.7 runtime](https://cloud.google.com/appengine/docs/standard/long-term-support#our_commitment), continuing their _"more than decade-long history of supporting your apps"_.

Still, you need to be aware that:
> As communities stop maintaining versions of their languages, your app may be exposed to vulnerabilities for which no publicly available fix exists. Thus, continuing to run your app in some App Engine runtimes involves more risk than upgrading to a runtime that has a community supported language.

Also, you should know that if Google ever decides to deprecate any of the APIs used by this project, it will first be announced at their [deprecations page](https://cloud.google.com/appengine/docs/deprecations/).

For more discussions on this topic, please refer to [issue #3](https://github.com/albertcht/python-gcs-image/issues/3).

## Setup

1. Clone this repo.

```
git clone https://github.com/albertcht/python-gcs-image.git
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

## Google Cloud Storage Setup

Note you need to grant **Storage Object Admin** access on your GCS objects to a GAE service account responsible for generating URLs, which looks like:

```
your-project-id@appspot.gserviceaccount.com
```

## gsutil Commands for Reference

```
# Create a new bucket.
gsutil mb -p <project> gs://<bucket>

# Set the default ACL for objects uploaded to the bucket. Note the below
# command grants OWNER access to the service account.
gsutil defacl ch -u account@example.com:O gs://<bucket>

# If using the web uploader you will also need to grant access to the service
# account to create objects.
gsutil acl ch -u account@example.com:O gs://<bucket>

# Ensure that the files are set with `public-read` permissions. URLs generated
# by the images service respect GCS object permissions so if you intend to serve
# them publicly, they will need to be `public-read`. Adjust the default ACL with
# the command below.
gsutil defacl set public-read gs://<bucket>

# Upload assets to the Google Cloud Storage bucket.
gsutil cp file.jpg gs://<bucket>/<path>/
```

## Examples

* By default it returns an image of a maximum length of 512px. [(link)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg)

* By appending the =sXX to the end of it where XX can be any integer in the range of 0–1600 and it will result to scale down the image to longest dimension without affecting the original aspect ratio. [(link =s256)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=s256)

* By appending =sXX-c a cropped version of that image is being returned as a response. [(link =s400-c)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=s400-c)

* By appending =pp-br100-rp-s200 the image is smartly cropped, border 100%, format PNG and size is 200. [(link =pp-br100-rp-s200)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=pp-br100-rp-s200)

* By appending =pp-br100-rp-s200 the image is smartly cropped, width 100, height 300, quality 100, format JPG. [(link =w100-h300-c-pp-l100-rj)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=w100-h300-c-pp-l100-rj)

* By appending =s0 (s zero) the original image is being returned without any resize or modification. [(link =s0)](https://lh3.googleusercontent.com/93uhV8K2yHkRuD63KJxlTi7SxjHS8my2emuHmGLZxEmX99_XAjTN3c_2zmKVb3XQ5d8FEkwtgbGjyYpaDQg=s0)


## Advanced Parameters

### SIZE / CROP

* **s640** — generates image 640 pixels on largest dimension
* **s0** — original size image
* **w100** — generates image 100 pixels wide
* **h100** — generates image 100 pixels tall
* **s** (without a value) — stretches image to fit dimensions
* **c** — crops image to provided dimensions
* **n** — same as c, but crops from the center
* **p** — smart square crop, attempts cropping to faces
* **pp** — alternate smart square crop, does not cut off faces (?)
* **cc** — generates a circularly cropped image
* **ci** — square crop to smallest of: width, height, or specified =s parameter
* **nu** — no-upscaling. Disables resizing an image to larger than its original resolution.

### ROTATION

* **fv** — flip vertically
* **fh** — flip horizontally
* **r{90, 180, 270}** — rotates image 90, 180, or 270 degrees clockwise

### IMAGE FORMAT

* **rj** — forces the resulting image to be JPG
* **rp** — forces the resulting image to be PNG
* **rw** — forces the resulting image to be WebP
* **rg** — forces the resulting image to be GIF

* **v{0,1,2,3}** — sets image to a different format option (works with JPG and WebP)

> Forcing PNG, WebP and GIF outputs can work in combination with circular crops for a transparent background. Forcing JPG can be combined with border color to fill in backgrounds in transparent images.

### ANIMATED GIFs

* **rh** — generates an MP4 from the input image
* **k** — kill animation (generates static image)

### Filters

* **fSoften=1,100,0**: - where 100 can go from 0 to 100 to blur the image
* **fVignette=1,100,1.4,0,000000** where 100 controls the size of the gradient and 000000 is RRGGBB of the color of the border shadow
* **fInvert=0,1** inverts the image regardless of the value provided
* **fbw=0,1** makes the image black and white regardless of the value provided

### MISC.

* **b10** — add a 10px border to image
* **c0xAARRGGBB** — set border color, eg. =c0xffff0000 for red
* **d** — adds header to cause browser download
* **e7** — set cache-control max-age header on response to 7 days
* **l100** — sets JPEG quality to 100% (1-100)
* **h** — responds with an HTML page containing the image
* **g** — responds with XML used by Google's pan/zoom

## Full Reference

```
int:  s   ==> Size
int:  w   ==> Width
bool: c   ==> Crop
hex:  c   ==> BorderColor
bool: d   ==> Download
int:  h   ==> Height
bool: s   ==> Stretch
bool: h   ==> Html
bool: p   ==> SmartCrop
bool: pa  ==> PreserveAspectRatio
bool: pd  ==> Pad
bool: pp  ==> SmartCropNoClip
bool: pf  ==> SmartCropUseFace
int:  p   ==> FocalPlane
bool: n   ==> CenterCrop
int:  r   ==> Rotate
bool: r   ==> SkipRefererCheck
bool: fh  ==> HorizontalFlip
bool: fv  ==> VerticalFlip
bool: cc  ==> CircleCrop
bool: ci  ==> ImageCrop
bool: o   ==> Overlay
str:  o   ==> EncodedObjectId
str:  j   ==> EncodedFrameId
int:  x   ==> TileX
int:  y   ==> TileY
int:  z   ==> TileZoom
bool: g   ==> TileGeneration
bool: fg  ==> ForceTileGeneration
bool: ft  ==> ForceTransformation
int:  e   ==> ExpirationTime
str:  f   ==> ImageFilter
bool: k   ==> KillAnimation
int:  k   ==> FocusBlur
bool: u   ==> Unfiltered
bool: ut  ==> UnfilteredWithTransforms
bool: i   ==> IncludeMetadata
bool: ip  ==> IncludePublicMetadata
bool: a   ==> EsPortraitApprovedOnly
int:  a   ==> SelectFrameint
int:  m   ==> VideoFormat
int:  vb  ==> VideoBegin
int:  vl  ==> VideoLength
bool: lf  ==> LooseFaceCrop
bool: mv  ==> MatchVersion
bool: id  ==> ImageDigest
int:  ic  ==> InternalClient
bool: b   ==> BypassTakedown
int:  b   ==> BorderSize
str:  t   ==> Token
str:  nt0 ==> VersionedToken
bool: rw  ==> RequestWebp
bool: rwu ==> RequestWebpUnlessMaybeTransparent
bool: rwa ==> RequestAnimatedWebp
bool: nw  ==> NoWebp
bool: rh  ==> RequestH264
bool: nc  ==> NoCorrectExifOrientation
bool: nd  ==> NoDefaultImage
bool: no  ==> NoOverlay
str:  q   ==> QueryString
bool: ns  ==> NoSilhouette
int:  l   ==> QualityLevel
int:  v   ==> QualityBucket
bool: nu  ==> NoUpscale
bool: rj  ==> RequestJpeg
bool: rp  ==> RequestPng
bool: rg  ==> RequestGif
bool: pg  ==> TilePyramidAsProto
bool: mo  ==> Monogram
bool: al  ==> Autoloop
int:  iv  ==> ImageVersion
int:  pi  ==> PitchDegrees
int:  ya  ==> YawDegrees
int:  ro  ==> RollDegrees
int:  fo  ==> FovDegrees
bool: df  ==> DetectFaces
str:  mm  ==> VideoMultiFormat
bool: sg  ==> StripGoogleData
bool: gd  ==> PreserveGoogleData
bool: fm  ==> ForceMonogram
int:  ba  ==> Badge
int:  br  ==> BorderRadius
hex:  bc  ==> BackgroundColor
hex:  pc  ==> PadColor
hex:  sc  ==> SubstitutionColor
bool: dv  ==> DownloadVideo
bool: md  ==> MonogramDogfood
int:  cp  ==> ColorProfile
bool: sm  ==> StripMetadata
int:  cv  ==> FaceCropVersion
```

> Reference:
> * https://stackoverflow.com/questions/25148567/list-of-all-the-app-engine-images-service-get-serving-url-uri-options
> * https://medium.com/google-cloud/uploading-resizing-and-serving-images-with-google-cloud-platform-ca9631a2c556
