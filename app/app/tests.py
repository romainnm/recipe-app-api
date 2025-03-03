"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """"Test the calc module."""
    def test_add_numbers(self):
        """Test adding numbers together."""
        result = calc.add(1, 2)

        self.assertEqual(result, 3)
