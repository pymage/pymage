from os import path
from src.pymage.processor import ImagesProcessor
from PIL import Image
import pytest
import shutil

@pytest.fixture(autouse=True)
def run_around_tests():
    # Running test
    yield

    # Teardown
    if path.exists('./images/output'):
        shutil.rmtree('./images/output')

    if path.exists('./output'):
        shutil.rmtree('./output')

    if path.exists('./custom_output'):
        shutil.rmtree('./custom_output')

def test_should_save_processed_images_in_custom_output_folder():
    ImagesProcessor(
        input=["./images/"],
        output_dir_name="custom_output",
        formats=["jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = './custom_output/mountain_320.jpeg'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"

def test_process_images_from_folder():
    ImagesProcessor(
        input=["./images/"],
        formats=["jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = './output/mountain_320.jpeg'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"

def test_process_image_one_size_same_format():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        formats=["jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = './images/output/mountain_320.jpeg'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_multiple_sizes_same_format():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        formats=["jpg"],
        quality=100,
        widths=[320, 640, 960]
    ).process()

    # 320px width image
    resized_image_320_path = './images/output/mountain_320.jpeg'
    resized_image_320 = Image.open(resized_image_320_path)

    # 640px width image
    resized_image_640_path = './images/output/mountain_640.jpeg'
    resized_image_640 = Image.open(resized_image_640_path)

    # 960px width image
    resized_image_960_path = './images/output/mountain_960.jpeg'
    resized_image_960 = Image.open(resized_image_960_path)

    # 320px width image
    assert path.exists(resized_image_320_path) is True
    assert resized_image_320.size[0] == 320
    assert resized_image_320.get_format_mimetype() == "image/jpeg"

    # 640px width image
    assert path.exists(resized_image_640_path) is True
    assert resized_image_640.size[0] == 640
    assert resized_image_640.get_format_mimetype() == "image/jpeg"

    # 960px width image
    assert path.exists(resized_image_960_path) is True
    assert resized_image_960.size[0] == 960
    assert resized_image_960.get_format_mimetype() == "image/jpeg"


def test_process_image_one_size_changing_format():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        formats=["webp"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = './images/output/mountain_320.webp'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/webp"


def test_process_image_one_size_changing_to_multiple_formats():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        formats=["jpeg", "webp", "png"],
        quality=100,
        widths=[320]
    ).process()

    # JPEG image
    resized_image_jpeg_path = './images/output/mountain_320.jpeg'
    resized_image_jpeg = Image.open(resized_image_jpeg_path)

    # WEBP image
    resized_image_webp_path = './images/output/mountain_320.webp'
    resized_image_webp = Image.open(resized_image_webp_path)

    # PNG image
    resized_image_png_path = './images/output/mountain_320.png'
    resized_image_png = Image.open(resized_image_png_path)

    assert path.exists(resized_image_jpeg_path) is True
    assert resized_image_jpeg.size[0] == 320
    assert resized_image_jpeg.get_format_mimetype() == "image/jpeg"

    assert path.exists(resized_image_webp_path) is True
    assert resized_image_webp.size[0] == 320
    assert resized_image_webp.get_format_mimetype() == "image/webp"

    assert path.exists(resized_image_png_path) is True
    assert resized_image_png.size[0] == 320
    assert resized_image_png.get_format_mimetype() == "image/png"


def test_process_image_without_quality():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        formats=["jpg"],
        widths=[320]
    ).process()

    resized_image_path = './images/output/mountain_320.jpeg'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_without_format_generates_image_from_mimetype():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = './images/output/mountain_320.jpeg'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_without_width_generates_images_of_300px_500px_750px():
    ImagesProcessor(
        input=["./images/mountain.jpg"],
        formats=["jpg"],
        quality=100
    ).process()

    # 300px width image
    resized_image_300_path = './images/output/mountain_300.jpeg'
    resized_image_300 = Image.open(resized_image_300_path)

    # 500px width image
    resized_image_500_path = './images/output/mountain_500.jpeg'
    resized_image_500 = Image.open(resized_image_500_path)

    # 750px width image
    resized_image_750_path = './images/output/mountain_750.jpeg'
    resized_image_750 = Image.open(resized_image_750_path)

    # 300px width image
    assert path.exists(resized_image_300_path) is True
    assert resized_image_300.size[0] == 300
    assert resized_image_300.get_format_mimetype() == "image/jpeg"

    # 500px width image
    assert path.exists(resized_image_500_path) is True
    assert resized_image_500.size[0] == 500
    assert resized_image_500.get_format_mimetype() == "image/jpeg"

    # 750px width image
    assert path.exists(resized_image_750_path) is True
    assert resized_image_750.size[0] == 750
    assert resized_image_750.get_format_mimetype() == "image/jpeg"
