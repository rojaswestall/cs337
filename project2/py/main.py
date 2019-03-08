import sys
import web_scraper
import vegetarian
import knowledge_base
import os
import cli


kb_filepath = os.path.join(os.path.dirname(__file__), os.pardir, 'kb.json')


def main(transform_code):
    kb = knowledge_base.KnowledgeBase(kb_filepath)

    address = sys.stdin.read()

    recipe = web_scraper.fetch_recipe(address)

    transformer = choose_transformer(transform_code)

    transformed_recipe = transformer(recipe, kb)

    print('TRANSFORMED RECIPE\n\n', transformed_recipe)


def choose_transformer(transform_code):
    if transform_code == 'veg':
        return vegetarian.make_vegetarian

    else
    print('invalid transform code. Something went wrong.')


if __name__ == '__main__':
    transform_code = cli.parse_transform_code()
    main(transform_code)
