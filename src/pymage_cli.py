import os, sys
from pathlib import Path
import argparse
from resizer import resize

class PymageCLI:
  CLI_VERSION = 'Pymage CLI 1.0.0'

  def __init__(self):
    self.__run()

  def __run(self):
    self.parser = argparse.ArgumentParser(
      prog="pymage",
      usage="pymage [image_file] [-f] [-w] [-q]",
      epilog="Enjoy the program! :)",
      formatter_class=argparse.RawDescriptionHelpFormatter
    )
    self.parser.version = self.CLI_VERSION
    self.parser.add_argument_group(title="args", description='''
-f --format        Set the output image formats | -f webp jpeg
-w --width         Set the output image sizes   | -w 300 600 900
-q --quality       Set the output image quality | -q 100
-v --version       Print version info
    ''')
    self.parser.add_argument("image_file", type=Path, help=argparse.SUPPRESS)
    self.parser.add_argument("-w", "--width", type=int, nargs='*', help=argparse.SUPPRESS, dest='')
    self.parser.add_argument("-f", "--format", type=str, nargs='*', help=argparse.SUPPRESS, dest='')
    self.parser.add_argument("-q", "--quality", type=int, nargs='?', help=argparse.SUPPRESS, dest='')
    self.parser.add_argument("-v", "--version", action="version", help=argparse.SUPPRESS, dest='')

    parser_args = self.parser.parse_args()

    if parser_args:
      try:
        if os.path.exists(parser_args.file_path):
          #resize()
          print(os.path.abspath(parser_args.file_path))
          print(parser_args)
        else:
          raise Exception("file not found")
      except Exception as e:
        print("Inválid argument: {}".format(e))
        sys.exit(1)
    else:
      self.parser.print_help()
      sys.exit(1)