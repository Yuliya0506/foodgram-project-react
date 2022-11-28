from http import HTTPStatus

from django.db.models import Sum
from rest_framework.response import Response

from recipes.models import IngredientAmount


def generate_shop_list(user):
    ingredients = IngredientAmount.objects.filter(
        recipe__cart__user=user).values(
            'ingredients__name',
            'ingredients__measurement_unit',
    ).annotate(Sum('amount'))
    if not ingredients:
        return Response({'error': 'Ваша корзина пуста'},
                        status=HTTPStatus.BAD_REQUEST)
    shop_list = {}
    for item in ingredients:
        name = item['ingredients__name']
        if name not in shop_list:
            shop_list[name] = {
                'name': item['ingredients__name'],
                'unit': item['ingredients__measurement_unit'],
                'amount': item['amount__sum']
            }
        else:
            shop_list[name]['amount'] += item['amount__sum']
    final_list = 'Список покупок: \n'
    for ingredient in shop_list:
        final_list += (
            f"{shop_list[ingredient]['name']} - "
            f"{shop_list[ingredient]['amount']} "
            f"{shop_list[ingredient]['unit']} \n"
        )
    return final_list
