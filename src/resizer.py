from os import path, mkdir
from PIL import Image

def resizeImages(images, widths, quality, formats):
  for image in images:
    try:
      if path.exists(image):
        resize(image, widths, quality, formats)
      else:
        raise RuntimeError('Image %(image)s not found' % { 'image': image })
    except RuntimeError as e:
        print(e)
    except Exception as e:
        print(e)
        print('Something went wrong -.-\'')


def resize(image, widths, quality, formats):
  widths = widths or [300, 500, 750]
  quality = quality or 100
  formats = formats or ['jpeg']

  image_absolute_path = path.realpath(image)
  output_dir = path.dirname(image_absolute_path)
  file_name = path.splitext(path.basename(image_absolute_path))[0]
  
  with Image.open(image_absolute_path) as img:
    for width in widths:
      resized_img = resizeImage(img, width)

      for format in formats:
        file_props = {
          'name': file_name,
          'size': width,
          'format': format
        }
        output_filename = '%(name)s_%(size)s.%(format)s' % file_props
        img_output_dir = path.join(output_dir, file_name)
        createOutputDir(img_output_dir)
        img_output_path = path.join(img_output_dir, output_filename)
        resized_img.save(img_output_path, extension=format, quality=quality)

def resizeImage(image, width):
  img_width = float(image.size[0])
  img_height = float(image.size[1])
  width_percent = float(width / img_width)
  new_image_height = int(img_height * width_percent)
  
  return image.resize((width, new_image_height), resample=Image.BICUBIC)

def createOutputDir(dir_path):
  output_dir_exists = path.exists(dir_path)

  if not output_dir_exists:
    mkdir(dir_path)