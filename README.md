<p align="center">
  <img src="https://raw.githubusercontent.com/pymage/pymage/main/docs/img/pymage.png" height="400" />
</p>

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Give a Star! ⭐
If you liked my work and want to support me, please give it a star. Thanks!

## 1. The problem 
When I was starting at the IT area, I pick up some website building projects and then I recognize that performance is a really good issue to improove the amout of leads at your site.

When we are talking about website performance one of the most important thing is the images, images can be a really good vilain because in some scenarious we use a bad format or a incorrect size.

Ideally, we shoud have a single image in some low-size format like WEBP and a common format like JPEG as a fallback, but not only the format is important, if you will open a website at a 1920x1080 pixels screen and the website has a banner image, that image should be 1080 pixels wide, but, if you acess the same site from a smartphone with screen size of 390x844 pixels, doesn't make sense you load an image that are 1080 pixels wide.

So, to have a performance optimized website we should have each userd image in multiples formats and sizes.

## 2. What Pymage do?
That project was created with the objective to make that process of resize and reformat images easier, with a single command, you create some versions with different sizes and formats from an image. 

## 3. Features 💡
- Resize images.
- Generate images with multiple sizes
- Change image format
- Generate images with multiple formats
- Change image quality

## 4. Using 📕

**Install (Requires Python >= 3.8)**
```bash
  pip install pymage-processor
```

**Running**
```bash
  pymage
```

*If, when executing this command, you do not see the help command, refer to the item below.*

**Problem running**
The install process put the app in the ~/.local/bin directory so check if you have that directory in the PATH variable.

You can do this by running this command, but you will need to put it in your .bashrc file or equivalent so you don't have to do it every time you open a new terminal
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Uninstall**
```bash
  pip uninstall pymage-processor
```

## 5. Run Locally 🚀

**Clone the project**

```bash
  git clone https://github.com/pymage/pymage.git
  OR
  git clone git@github.com:pymage/pymage.git
```

**Go to the project directory**

```bash
  cd pymage
```

**Install and run virtualenv**
```bash
  sudo pip3 install virtualenv
  mkdir venv
  which python3
  virtualenv --python='/path/to/python3' venv
  source venv/bin/activate
```

**Install dependencies**
```bash
  pip install -r requirements.txt
```

**Running**
```bash
  python -m src.pymage [pathToImage] -f [formats] -w [sizes] -q [quality]
```

**Commands**
```bash
  # Help!
  python src/pymage --help

  # Output
  usage: pymage [image_files] [-f] [-w] [-q]

  optional arguments:
    -h, --help  show this help message and exit

  args:
    
    -f --format   Set the output image formats | -f webp jpeg
    -w --width    Set the output image sizes   | -w 300 600 900
    -q --quality  Set the output image quality | -q 100
    -v --version  Print version info
            

  Enjoy the program! :)
```

*To stop the virtual environment run:* `deactivate`
*Top remove all dependencies run:* `rm -r venv`

## 6. Running Tests 🧪

To run tests, run the following command

```bash
  source venv/bin/activate
  pip install -r requirements_dev.txt
  pytest -s
```

## 7. Suport and Bugs Report 🚨
If you found a bug, have a feature need, feedback or doubt, just open a issue.
