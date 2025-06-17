def filter_recipes_by_restrictions(recipes, restrictions):
    restrictions = [r.lower() for r in restrictions]
    return recipes[~recipes["ingredients"].str.lower().apply(lambda ing: any(r in ing for r in restrictions))]
