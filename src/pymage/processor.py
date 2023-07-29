from os import path, mkdir
from PIL import Image
from typing import List


class ImagesProcessor:
    def __init__(
        self,
        images: List[str] = [],
        widths: List[float] = [],
        formats: List[str] = [],
        quality: float = 100
    ):
        self.images = self.__get_valid_images_paths(images)
        self.widths = widths or [300, 500, 750]
        self.formats = formats
        self.quality = quality or 100

    def process(self):
        for image in self.images:
            try:
                self.__process_image(image, self.widths, self.quality, self.formats)
            except Exception as e:
                print(e)
                print('Something went wrong -.-\'')

    def __process_image(
        self,
        image: str,
        widths: List[float],
        quality: float,
        formats: List[str]
    ):
        image_absolute_path = path.realpath(image)
        output_dir = path.dirname(image_absolute_path)
        file_name = path.splitext(path.basename(image_absolute_path))[0]

        with Image.open(image_absolute_path) as img:
            if not formats:
                image_mimetype = img.get_format_mimetype()
                image_format = image_mimetype.split('/')[1]
                formats = [image_format]

            for width in widths:
                resized_img = self.__resize_image(img, width)

                for format in formats:
                    file_props = {
                        'name': file_name,
                        'size': width,
                        'format': format
                    }
                    output_filename = '%(name)s_%(size)s.%(format)s' % file_props
                    img_output_dir = self.__create_output_dir(output_dir, file_name)
                    img_output_path = path.join(img_output_dir, output_filename)
                    resized_img.save(img_output_path, extension=format, quality=quality)

    def __resize_image(self, image, width):
        img_width = float(image.size[0])
        img_height = float(image.size[1])
        width_percent = float(width / img_width)
        new_image_height = int(img_height * width_percent)

        return image.resize((width, new_image_height), resample=Image.Resampling.BICUBIC)

    def __create_output_dir(self, output_dir: str, file_name: str):
        img_output_dir = path.join(output_dir, file_name)
        output_dir_exists = path.exists(img_output_dir)

        if not output_dir_exists:
            mkdir(img_output_dir)

        return img_output_dir

    def __get_valid_images_paths(self, images_paths: List[str]):
        existent_images = []

        for image in images_paths:
            try:
                if path.exists(image):
                    existent_images.append(image)
                else:
                    raise RuntimeError('Image %(image)s not found' % {'image': image})
            except RuntimeError as e:
                print(e)

        return existent_images
