import sys
import web_scraper
import knowledge_base
import os
import cli

KB_FILENAME = 'kb.json'


def main(transformer):
    kb_filepath = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        KB_FILENAME)

    kb = knowledge_base.KnowledgeBase(kb_filepath)

    address = sys.stdin.read()

    recipe = web_scraper.fetch_recipe(address, kb)

    transformed_recipe = transformer(recipe, kb)

    print('# Transformed Recipe\n')
    print(transformed_recipe)


if __name__ == '__main__':
    transformer = cli.parse_transform_code()
    main(transformer)
