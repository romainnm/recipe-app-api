"""
Tests for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'test@example.com'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_nomalized(self):
        email = 'TestUser@MAIL.COM'

        sample = get_user_model().objects.create_user(
            email,
            password='password',
        )

        self.assertEqual(sample.email, 'TestUser@mail.com')

    def test_new_user_without_email_raises_error(self):
        email = ''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, password='password')

    def test_create_super_user(self):
        email = 'superuser@mail.com'
        password = 'password'

        superuser = get_user_model().objects.create_superuser(
            email,
            password
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_in_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creation of new tag"""
        user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        tag = models.Tag.objects.create(user=user, name='tagname')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        ingredient = models.Ingredient.objects.create(
            user=user,
            name='ingredientname'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test gemerating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
