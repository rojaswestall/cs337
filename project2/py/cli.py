import argparse
import transform

TRANSFORM_CODE_MAP = {
    'veg': transform.to_vegetarian,
    'meat': transform.from_vegetarian,
    'healthy': transform.to_healthy,
    'unhealthy': transform.from_healthy,
    'chinese': transform.to_chinese
}


def parse_transform_code():
    parser = argparse.ArgumentParser(
        description='Recipe Transformer',
    )

    parser.add_argument(
        'transform code',
        action="store",
        type=str,
        help='Choose Recipe Transformation',
        choices=TRANSFORM_CODE_MAP.keys())

    args = vars(parser.parse_args())

    code = args['transform code']

    transformer = TRANSFORM_CODE_MAP[code]

    return transformer
