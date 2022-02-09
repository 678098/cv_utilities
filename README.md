# cv_utilities

## Background provider

Class and utility script for generating different backgrounds from image files from the specified parent folder.  As a
good source of backgrounds [Indoor dataset](http://web.mit.edu/torralba/www/indoor.html) can be used.

### Limitations

* `.jpg`, `.png`, `.bmp` image extensions are supported.

* Parent image folder is scanned recursively, paths to images are cached on `BackgroundProvider` construction.

* Backgrounds can be prepared in `BGR` or `grayscale` image format (see `grayscale` flag).

* Resize interpolation is picked randomly from `opencv`.

### Usage workflow

1. Download or prepare parent `images_dir` with images.
   
**Note:** it's better to place image folder on a fast drive for
faster reading.

**Note:** image extension matters when loading - `.bmp` might load faster (almost no overhead on decoding in comparison
to other formats).

**Note:** it's wise to check generation performance with different image formats on specific task and it might be a good
idea to reconvert images to the most suitable format to speed-up the generation.  Compression level and image quality
should be taken into consideration though.

2. Construct an instance of `BackgroundProvider` with the given `images_dir`.

3. Initialize system default `random` with some seed to get a truly randomized backgrounds.

4. Generate random backgrounds as a numpy arrays:

* `get_random_image` to load random image from `images_dir`.

* `get_random_crop` to cut random crop from a random image.

* `get_random_crops` to cut several random crops from the same random image.  This function is useful when limited on IO
  operations.
