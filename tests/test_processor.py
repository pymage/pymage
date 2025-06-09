from os import path
from src.pymage.processor import ImagesProcessor
from PIL import Image
import pytest
import shutil
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
images_path = CURRENT_DIR / "images"
images_output_path = CURRENT_DIR / "images/output"


@pytest.fixture(autouse=True)
def run_around_tests():
    # Running test
    yield

    # Teardown
    if path.exists(images_output_path):
        shutil.rmtree(images_output_path)

    if path.exists(CURRENT_DIR / 'output'):
        shutil.rmtree(CURRENT_DIR / 'output')

    if path.exists(CURRENT_DIR / 'custom_output'):
        shutil.rmtree(CURRENT_DIR / 'custom_output')


def test_should_save_processed_images_in_custom_output_folder():
    ImagesProcessor(
        input=[images_path],
        output_dir_name="custom_output",
        formats=["jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = CURRENT_DIR / 'custom_output/mountain_320.jpeg'

    assert path.exists(resized_image_path) is True
    resized_image = Image.open(resized_image_path)
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_images_from_folder():
    ImagesProcessor(
        input=[images_path],
        formats=["jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = CURRENT_DIR / 'output/mountain_320.jpeg'

    assert path.exists(resized_image_path) is True
    resized_image = Image.open(resized_image_path)
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_one_size_same_format():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        formats=["jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = images_output_path / 'mountain_320.jpeg'

    assert path.exists(resized_image_path) is True
    resized_image = Image.open(resized_image_path)
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_multiple_sizes_same_format():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        formats=["jpg"],
        quality=100,
        widths=[320, 640, 960]
    ).process()

    resized_image_320_path = images_output_path / 'mountain_320.jpeg'
    resized_image_640_path = images_output_path / 'mountain_640.jpeg'
    resized_image_960_path = images_output_path / 'mountain_960.jpeg'

    # 320px width image
    assert path.exists(resized_image_320_path) is True
    resized_image_320 = Image.open(resized_image_320_path)
    assert resized_image_320.size[0] == 320
    assert resized_image_320.get_format_mimetype() == "image/jpeg"

    # 640px width image
    assert path.exists(resized_image_640_path) is True
    resized_image_640 = Image.open(resized_image_640_path)
    assert resized_image_640.size[0] == 640
    assert resized_image_640.get_format_mimetype() == "image/jpeg"

    # 960px width image
    assert path.exists(resized_image_960_path) is True
    resized_image_960 = Image.open(resized_image_960_path)
    assert resized_image_960.size[0] == 960
    assert resized_image_960.get_format_mimetype() == "image/jpeg"


def test_process_image_one_size_changing_format():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        formats=["webp"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = images_output_path / 'mountain_320.webp'

    assert path.exists(resized_image_path) is True
    resized_image = Image.open(resized_image_path)
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/webp"


def test_process_image_one_size_changing_to_multiple_formats():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        formats=["jpeg", "webp", "png"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_jpeg_path = images_output_path / 'mountain_320.jpeg'
    resized_image_webp_path = images_output_path / 'mountain_320.webp'
    resized_image_png_path = images_output_path / 'mountain_320.png'

    assert path.exists(resized_image_jpeg_path) is True
    resized_image_jpeg = Image.open(resized_image_jpeg_path)
    assert resized_image_jpeg.size[0] == 320
    assert resized_image_jpeg.get_format_mimetype() == "image/jpeg"

    assert path.exists(resized_image_webp_path) is True
    resized_image_webp = Image.open(resized_image_webp_path)
    assert resized_image_webp.size[0] == 320
    assert resized_image_webp.get_format_mimetype() == "image/webp"

    assert path.exists(resized_image_png_path) is True
    resized_image_png = Image.open(resized_image_png_path)
    assert resized_image_png.size[0] == 320
    assert resized_image_png.get_format_mimetype() == "image/png"


def test_process_image_without_quality():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        formats=["jpg"],
        widths=[320]
    ).process()

    resized_image_path = images_output_path / 'mountain_320.jpeg'

    assert path.exists(resized_image_path) is True
    resized_image = Image.open(resized_image_path)
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_without_format_generates_image_from_mimetype():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        quality=100,
        widths=[320]
    ).process()

    resized_image_path = images_output_path / 'mountain_320.jpeg'

    assert path.exists(resized_image_path) is True
    resized_image = Image.open(resized_image_path)
    assert resized_image.size[0] == 320
    assert resized_image.get_format_mimetype() == "image/jpeg"


def test_process_image_without_width_generates_images_of_300px_500px_750px():
    ImagesProcessor(
        input=[images_path / "mountain.jpg"],
        formats=["jpg"],
        quality=100
    ).process()

    resized_image_300_path = images_output_path / 'mountain_300.jpeg'
    resized_image_500_path = images_output_path / 'mountain_500.jpeg'
    resized_image_750_path = images_output_path / 'mountain_750.jpeg'

    # 300px width image
    assert path.exists(resized_image_300_path) is True
    resized_image_300 = Image.open(resized_image_300_path)
    assert resized_image_300.size[0] == 300
    assert resized_image_300.get_format_mimetype() == "image/jpeg"

    # 500px width image
    assert path.exists(resized_image_500_path) is True
    resized_image_500 = Image.open(resized_image_500_path)
    assert resized_image_500.size[0] == 500
    assert resized_image_500.get_format_mimetype() == "image/jpeg"

    # 750px width image
    assert path.exists(resized_image_750_path) is True
    resized_image_750 = Image.open(resized_image_750_path)
    assert resized_image_750.size[0] == 750
    assert resized_image_750.get_format_mimetype() == "image/jpeg"
