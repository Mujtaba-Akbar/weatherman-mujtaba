import sys
from weather_data_parser import *
from actions import *
from cmd_parser import create_parser


def main():
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parser.parse_args()


if __name__ == "__main__":
    main()
