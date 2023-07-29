import sys
import argparse
from pathlib import Path
from .processor import ImagesProcessor


class PymageCLI:
    CLI_VERSION = 'Pymage CLI 1.0.0'

    def __init__(self):
        self.__run()

    def __run(self):
        self.parser = argparse.ArgumentParser(
            prog="pymage",
            usage="pymage [image_files] [-f] [-w] [-q]",
            epilog="Enjoy the program! :)",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.parser.add_argument_group(title="args", description='''
-f --format   Set the output image formats | -f webp jpeg
-w --width    Set the output image sizes   | -w 300 600 900
-q --quality  Set the output image quality | -q 100
-v --version  Print version info
        ''')
        self.parser.add_argument("image_file", type=Path, nargs='*', help=argparse.SUPPRESS)
        self.parser.add_argument("-w", "--width", type=int, nargs='*', help=argparse.SUPPRESS, dest='widths')
        self.parser.add_argument("-f", "--format", type=str, nargs='*', help=argparse.SUPPRESS, dest='formats')
        self.parser.add_argument("-q", "--quality", type=int, nargs='?', help=argparse.SUPPRESS, dest='quality')
        self.parser.add_argument("-v", "--version", action="version", help=argparse.SUPPRESS, dest='')

        parser_args = self.parser.parse_args()

        if not any(vars(parser_args).values()):
            self.parser.print_help()
            sys.exit(1)
        else:
            try:
                images_processor = ImagesProcessor(
                    images=parser_args.image_file,
                    widths=parser_args.widths,
                    quality=parser_args.quality,
                    formats=parser_args.formats
                )

                images_processor.process()
            except Exception as e:
                print("Invalid argument: {}".format(e))
                sys.exit(1)
