def generate_shop_cart(ingredients):
    shopping_cart = '\n'.join([
            f'{ingredient["ingredients__name"]} - {ingredient["amount"]} '
            f'{ingredient["ingredients__measurement_unit"]}'
            for ingredient in ingredients
        ])
    return shopping_cart
