import os
from PIL import Image
from typing import List, Union
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


class ImagesProcessor:

    def __init__(
            self,
            input: Union[str, Path, List[Union[str, Path]]],
            output_dir_name: str = "output",
            widths: List[int] = [300, 500, 750],
            formats: List[str] = [],
            quality: int = 100
    ):
        self.widths = widths
        self.formats = formats
        self.quality = quality

        self.images = self.__get_valid_images(input)
        self.output_dir = self.__resolve_output_dir(input, output_dir_name)
        self.__create_output_dir()

    def process(self, max_workers: int = 1):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.__process_image, image_path): image_path for image_path in self.images}
            try:
                for future in tqdm(as_completed(futures), total=len(futures), desc="Processing images"):
                    image_path = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Error processing {image_path}: {e}")
            except KeyboardInterrupt:
                print("\nProcess cancelled by user. Shutting down...")
                # Cancel all futures that are not done yet
                for future in futures:
                    if not future.done():
                        future.cancel()
                executor.shutdown(wait=False)

    def __process_image(self, image_path: str):
        file_name = os.path.splitext(os.path.basename(image_path))[0]

        with Image.open(image_path) as img:
            image_formats = self.formats or [img.format.lower()]

            for width in self.widths:
                for fmt in image_formats:
                    # Normalize format
                    if fmt.lower() == "jpg":
                        fmt = "jpeg"
                    output_filename = f"{file_name}_{width}.{fmt.lower()}"
                    output_path = os.path.join(self.output_dir, output_filename)

                    if os.path.exists(output_path):
                        # Skip if already exists
                        continue

                    resized_img = self.__resize_image(img, width)

                    if fmt.lower() in ['jpg', 'jpeg'] and resized_img.mode != 'RGB':
                        resized_img = resized_img.convert('RGB')

                    print(f" ================== Saved image: {output_path}")
                    resized_img.save(output_path, format=fmt.upper(), quality=self.quality)

    def __resize_image(self, image, width: int):
        w_percent = width / float(image.size[0])
        height = int(float(image.size[1]) * w_percent)
        return image.resize((width, height), resample=Image.Resampling.BICUBIC)

    def __create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def __resolve_output_dir(self, input_source, output_dir_name: str) -> str:
        if isinstance(input_source, (str, Path)) and os.path.isdir(input_source):
            base_dir = os.path.dirname(os.path.abspath(os.fspath(input_source)))
        elif isinstance(input_source, list) and len(input_source) > 0:
            first = os.fspath(input_source[0])
            if os.path.isdir(first):
                base_dir = os.path.dirname(os.path.abspath(first))
            else:
                base_dir = os.path.dirname(os.path.abspath(first))
        else:
            base_dir = os.getcwd()

        return os.path.join(base_dir, output_dir_name)

    def __get_valid_images(self, input_source) -> List[str]:
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
        images = []

        if isinstance(input_source, (str, Path)) and os.path.isdir(input_source):
            input_dir = Path(input_source)
            images = [str(p) for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in valid_extensions]

        elif isinstance(input_source, list):
            input_list = [os.fspath(p) for p in input_source]
            if len(input_list) == 1 and os.path.isdir(input_list[0]):
                input_dir = Path(input_list[0])
                images = [str(p) for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in valid_extensions]
            else:
                for file in input_list:
                    if os.path.isfile(file) and os.path.splitext(file)[1].lower() in valid_extensions:
                        images.append(file)
                    else:
                        print(f"Skipping invalid or non-existent file: {file}")
        else:
            print("Invalid input source. Provide a directory or a list of image paths.")

        return images
