import sys
import web_scraper
import vegetarian
import knowledge_base
import os

kb_filepath = os.path.join(os.path.dirname(__file__), os.pardir, 'kb.json')


def main():
    kb = knowledge_base.KnowledgeBase(kb_filepath)
    address = sys.stdin.read()
    recipe = web_scraper.fetch_recipe(address)
    vegetarian_recipe = vegetarian.make_vegetarian(recipe, kb)
    print('VEGETARIAN\n\n', vegetarian_recipe)


if __name__ == '__main__':
    main()
