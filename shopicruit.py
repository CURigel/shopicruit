import json
import urllib2 as ul2
from pandas.io.json import json_normalize

__author__ = 'Devin Denis'


def get_available_keyboards_and_computers():
    response = ul2.urlopen('http://shopicruit.myshopify.com/products.json')
    json_data = json.load(response)
    json_products = json_data['products']

    # Weight and price will be needed for the problem.  Product type is for filtering.
    variants = json_normalize(json_products, 'variants', ['product_type'])
    keys_and_comps = variants.loc[variants['product_type'].isin(['Computer', 'Keyboard'])]

    # Although it wasn't specified in the problem description, it stands to reason that only
    # items which are actually available can be bought
    return keys_and_comps.loc[variants['available'] == True]


def main():
    keys_and_comps = get_available_keyboards_and_computers()

    # So the weight of all the available computers and keyboards sums up to less than 100kg.
    # We can just take everything.  However, I'm going to solve this properly anyway.  It's
    # not very much work, and if new items were added I could reuse it.

    # We want to find the maximum number of items subject to sum(weight(item)) <= 100kg.
    # For this we should add items in order of lightest to heaviest until the next item would put us over the limit.
    # A little proof that this is correct:
    # Let S be the solution set we described.  Let W be the max weight.
    # Imagine a larger subset P exists, and weight(P) <= 100kg.
    # (1)
    # If S is a subset of P, then we know the additional items in P must fit into W - weight(s).
    # But we know by our definition of S that no items which have not already been chosen fit into  that space.
    # This situation creates a contradiction, and is therefore impossible.
    # (2)
    # If S is not a subset of P, then we could create another set Q by replacing items in P, heaviest first, with items
    # in S, such that S is a subset of Q.  We know that size of Q = size of P, and S is a subset of Q.
    # We know already by (1) that Q cannot exist.  Therefore P also cannot exist.

    max_weight = 100000  # 100kg = 100000g, the weights in the columns are in grams
    keys_and_comps.sort_values('grams', inplace=True)
    keys_and_comps['cumulative_grams'] = keys_and_comps['grams'].cumsum()
    largest_set = keys_and_comps.loc[keys_and_comps['cumulative_grams'] < max_weight]
    price = largest_set['price'].astype(float).sum()
    print price

if __name__ == '__main__':
    main()
