<p align="center">
  <img src="./doc/img/pymage.png" height="400" />
</p>

## Give a Star! :star:
If you liked my work and want to support me, please give it a star. Thanks!

---
## The problem 
When I was starting at the IT area, I pick up some website building projects and then I recognize that performance is a really good issue to improove the amout of leads at your site.

When we are talking about website performance one of the most important thing is the images, images can be a really good vilain because in some scenarious we use a bad format or a incorrect size.

Ideally, we shoud have a single image in some low-size format like WEBP and a common format like JPEG as a fallback, but not only the format is important, if you will open a website at a 1920x1080 pixels screen and the website has a banner image, that image should be 1080 pixels wide, but, if you acess the same site from a smartphone with screen size of 390x844 pixels, doesn't make sense you load an image that are 1080 pixels wide.

So, to have a performance optimized website we should have each userd image in multiples formats and sizes.

## Resolution
That project was created with the objective to make that process of resize and reformat images easier, with a single command, you create some versions with different sizes and formats from an image. 


## Running as DEV
#### Installing Virtualenv:
- `sudo pip3 install virtualenv`
- `mkdir venv`
- `which python3`
- `virtualenv --python='/path/to/python3' venv`
- `source venv/bin/activate`
- *To stop the virtual environment run:* `deactivate`
- *Top remove all dependencies run:* `rm -r venv`