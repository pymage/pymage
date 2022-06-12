from os import path
from glob import glob
from PIL import Image

def resize(widths=[300,500], quality=100, file='*.jpg', formats=['jpeg']):
  script_dir = path.dirname(__file__)
  abs_file_path = path.join(script_dir, file)

  for infile in glob(abs_file_path):
    file_path, extension = path.splitext(infile)
    file_name = path.basename(file_path)
    
    with Image.open(infile) as img:
      for width in widths:
        img_width = float(img.size[0])
        img_height = float(img.size[1])
        width_percent = float(width / img_width)
        new_image_height = int(img_height * width_percent)
        resized_img = img.resize((width, new_image_height))

        for format in formats:
          file_props = {
            'name': file_name,
            'size': width,
            'format': format
          }
          imgPath = path.join(script_dir, '%(name)s_%(size)s.%(format)s' % file_props)
          resized_img.save(imgPath, extension=format, quality=quality)