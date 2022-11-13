from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    FollowViewSet, IngredientsViewSet, RecipeViewSet,
    TagsViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', FollowViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
