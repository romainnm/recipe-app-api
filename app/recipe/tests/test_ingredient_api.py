"""
Tests for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return detail url"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


def create_ingredient(user, **params):
    return Ingredient.objects.create(user=user, **params)


class PublicIngredientApiTest(TestCase):
    """Test ingredient api for unauthorized user."""

    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_user(self):
        """Test auth is required to retrieve ingredients"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientTest(TestCase):
    """Test for ingredients API."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient(self):
        create_ingredient(user=self.user, name='Garlic')
        create_ingredient(user=self.user, name='Sugar')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')

        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test unique association user and ingredients"""
        user2 = create_user(email='user2@example.com', password='testpass2123')
        create_ingredient(user=user2, name='Orange')
        ingredient = create_ingredient(user=self.user, name='Pear')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = create_ingredient(user=self.user, name='Cilantro')

        payload = {'name': 'Coriander'}
        url = detail_url(ingredient.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        ingredient = create_ingredient(user=self.user, name='Cilantro')

        url = detail_url(ingredient.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())
