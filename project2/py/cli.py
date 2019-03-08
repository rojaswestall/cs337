import argparse


def parse_transform_code():
    parser = argparse.ArgumentParser(
        description='Example with nonoptional arguments',
    )

    parser.add_argument(
        'transformation',
        action="store",
        type=str,
        help='Choose Recipe Transformation',
        choices=['veg'])

    args = vars(parser.parse_args())

    return args['transformation']
