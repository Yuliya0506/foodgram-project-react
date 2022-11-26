from datetime import datetime

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import BooleanField, Exists, OuterRef, Sum, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Cart, Favorite, Ingredient, IngredientAmount,
    Recipe, Tag
)
from users.models import Follow
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AdminOrReadOnly, AdminUserOrReadOnly
from .serializers import (
    CustomUserSerializer, FollowSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, ShortRecipeSerializer,
    TagSerializer
)

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class FollowViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination

    @action(
        methods=['post', 'delete'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            follow = Follow.objects.create(
                user=user,
                author=author
            )
            serializer = FollowSerializer(
                follow,
                context={'request': request}
            )
            return Response(serializer.data, status=HTTPStatus.CREATED)

        if request.method == 'DELETE':
            follow = get_object_or_404(
                Follow,
                user=user,
                author=author
            )
            follow.delete()
            return Response(status=HTTPStatus.NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = LimitPageNumberPagination
    filter_class = RecipeFilter
    permission_classes = (AdminUserOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                ),
                is_in_shopping_cart=Exists(Cart.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                )
            )
        else:
            queryset = queryset.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )
        return queryset

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.__add_obj(Favorite, request.user, pk)

    @favorite.mapping.delete
    def del_from_favorite(self, request, pk=None):
        return self.__delete_obj(Favorite, request.user, pk)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.__add_obj(Cart, request.user, pk)

    @shopping_cart.mapping.delete
    def del_from_shopping_cart(self, request, pk=None):
        return self.__delete_obj(Cart, request.user, pk)

    @staticmethod
    def __add_obj(model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Ошибка добавления рецепта в список'
            }, status=HTTPStatus.BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @staticmethod
    def __delete_obj(model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response({
            'errors': 'Ошибка удаления рецепта из списка'
        }, status=HTTPStatus.BAD_REQUEST)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values(
            'ingredients__name',
            'ingredients__measurement_unit').annotate(amount=Sum('amount'))
        today = datetime.today()
        shopping_cart = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_cart += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_cart += f'\n\nFoodgram ({today:%Y})'
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
