import web_scraper
import sys
import recipe_parser
import utils


def main():
    addresses = sys.stdin.readlines()
    addresses = [address.strip() for address in addresses]
    recipes = web_scraper.fetch_recipes(addresses)
    recipes = [recipe['ingredients'] for recipe in recipes]
    pos = [recipe_parser.parse_ingredients(ingredients) for ingredients in recipes]

    utils.print_nested_lst(pos)
    # flat_pos = utils.flatten(pos)
    # sentence_tag_pairs = utils.pmap(utils.unzip, flat_pos)

    # unique_tags = filter_duplicates(sentence_tag_pairs)

    # tags = utils.nested_map(foo, flat_pos)
    # tags = utils.pmap(tuple, tags)
    # unique_tags = set(tags)

    # utils.print_nested_lst(unique_tags)

def foo(tup):
    return tup[1]

def filter_duplicates(pairs):
    cache = []
    new_lst = []
    for sent, tag in pairs:
        if tag in cache:
            continue
        cache.append(tag)
        new_lst.append((sent, tag))
    return new_lst
    

def cache_ingredients(sentence_tag_pair):
    cache = {}
    for sent, tag in sentence_tag_pair:
        cache[tag] = sent
    return cache


if __name__ == '__main__':
    main()
