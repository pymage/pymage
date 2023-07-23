from os import path
from src.pymage.processor import process_image
from PIL import Image
import pytest
import shutil

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup

    # Running test
    yield

    # Teardown
    shutil.rmtree('./tests/images/mountain')


def test_process_image_one_size_same_format():
    process_image(
        image="./tests/images/mountain.jpg",
        formats=["jpg"],
        quality=100,
        widths=[320]
    )

    resized_image_path = './tests/images/mountain/mountain_320.jpg'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_multiple_sizes_same_format():
    process_image(
        image="./tests/images/mountain.jpg",
        formats=["jpg"],
        quality=100,
        widths=[320, 640, 960]
    )

    # 320px width image
    resized_image_320_path = './tests/images/mountain/mountain_320.jpg'
    resized_image_320 = Image.open(resized_image_320_path)

    # 640px width image
    resized_image_640_path = './tests/images/mountain/mountain_640.jpg'
    resized_image_640 = Image.open(resized_image_640_path)

    # 960px width image
    resized_image_960_path = './tests/images/mountain/mountain_960.jpg'
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
    process_image(
        image="./tests/images/mountain.jpg",
        formats=["webp"],
        quality=100,
        widths=[320]
    )

    resized_image_path = './tests/images/mountain/mountain_320.webp'
    resized_image = Image.open(resized_image_path)

    assert path.exists(resized_image_path) is True
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/webp"


def test_process_image_one_size_changing_to_multiple_formats():
    process_image(
        image="./tests/images/mountain.jpg",
        formats=["jpeg", "webp", "png"],
        quality=100,
        widths=[320]
    )

    # JPEG image
    resized_image_jpeg_path = './tests/images/mountain/mountain_320.jpeg'
    resized_image_jpeg = Image.open(resized_image_jpeg_path)

    # WEBP image
    resized_image_webp_path = './tests/images/mountain/mountain_320.webp'
    resized_image_webp = Image.open(resized_image_webp_path)

    # PNG image
    resized_image_png_path = './tests/images/mountain/mountain_320.png'
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
