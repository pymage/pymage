import io
from os import path, mkdir
from PIL import Image
from typing import List
from zipfile import ZipFile
import traceback 


class ImagesProcessor:
    def __init__(
        self,
        images: List[str] = [],
        widths: List[float] = [],
        formats: List[str] = [],
        quality: float = 100,
        zip: bool = False
    ):
        self.images = self.__get_valid_images_paths(images)
        self.widths = widths or [300, 500, 750]
        self.formats = formats
        self.quality = quality or 100
        self.zip = zip or False

    def process(self):
        processed_images = []

        try:
            for image in self.images:
                image_output_dir = self.__create_output_dir(image)
                image_results = self.__process_image(image, self.widths, self.formats, image_output_dir)
                processed_images.append(image_results)

            self.__save_images(processed_images, image_output_dir, self.quality, self.zip)
        except Exception as e:
            traceback.print_exc()
            print('Something went wrong -.-\'')

    def __process_image(
        self,
        image: str,
        widths: List[float],
        formats: List[str],
        img_output_dir: str
    ):
        image_absolute_path = path.realpath(image)
        file_name = path.splitext(path.basename(image_absolute_path))[0]
        processed_images = []

        with Image.open(image_absolute_path) as img:
            if not formats:
                image_mimetype = img.get_format_mimetype()
                image_format = image_mimetype.split('/')[1]
                formats = [image_format]

            for width in widths:
                resized_img = self.__resize_image(img, width)

                for format in formats:
                    if (format == 'jpg'):
                        format = 'jpeg'

                    output_filename = file_name + "_" + str(width) + "." + format
                    image_result = {
                        "outputFilename": output_filename,
                        "format": format,
                        "image": resized_img,
                        "imgOutputPath": path.join(img_output_dir, output_filename)
                    }
                    processed_images.append(image_result)
        
        return processed_images

    def __resize_image(self, image, width):
        img_width = float(image.size[0])
        img_height = float(image.size[1])
        width_percent = float(width / img_width)
        new_image_height = int(img_height * width_percent)

        return image.resize((width, new_image_height), resample=Image.Resampling.BICUBIC)

    def __create_output_dir(self, image: str):
        image_absolute_path = path.realpath(image)
        output_dir = path.dirname(image_absolute_path)
        file_name = path.splitext(path.basename(image_absolute_path))[0]
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

    def __save_images(self, images, image_output_dir, quality, zip):
        if (zip == True):
            self.__save_images_in_zip(images, image_output_dir, quality)
        else:
            self.__save_images_in_dir(images, quality)

    def __save_images_in_zip(self, images, image_output_dir, quality):
        with ZipFile(image_output_dir + ".zip", 'w') as zip_file:
            for image_results in images:
                for image in image_results:
                    image_object = io.BytesIO()
                    image["image"].save(image_object, format=image["format"], extension=image["format"], quality=quality)
                    zip_file.writestr(image["outputFilename"], image_object.getvalue())
    
    def __save_images_in_dir(self, images, quality):
        for image_results in images:
            for image in image_results:
                image["image"].save(image["imgOutputPath"], extension=image["format"], quality=quality)
                