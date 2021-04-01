import argparse
from converter import convert, ParsersEnum


def create_parser():
    parser = argparse.ArgumentParser(
        prog='wtf_converter',
        usage='%(prog)s [A | [file_to_convert & format | file_to_save]]'
    )

    parser.add_argument('-cfg', '--config', type=argparse.FileType('r', encoding='UTF-8'), help='')
    parser.add_argument('-f', '--format', choices=['json', 'pickle'])
    parser.add_argument('-ftc', '--file_to_convert', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('-fts', '--file_to_save', type=argparse.FileType('r', encoding='UTF-8'))

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.config is not None:
        pass
    elif args.format and args.file_to_convert is not None:
        if args.file_to_save is not None:
            convert(ParsersEnum.JSON, ParsersEnum.JSON, open('text.txt', 'r'), open('text2.txt', 'w'))
            #close
    else:
        parser.error('parameters --format and --file_to_convert are required together')


if __name__ == '__main__':
    main()
