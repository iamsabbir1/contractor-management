from django.test import SimpleTestCase
from app import calc


class CalcTest(SimpleTestCase):

    def test_adding_two_number(self):
        """Test adding two number failed."""
        res = calc.add(5, 5)

        self.assertEqual(res, 10)

    def test_subtracting_two_number(self):
        res = calc.subtract(10, 5)

        self.assertEqual(res, 5)

    def test_multiply_two_numbers(self):
        """Test multiplying two numbers failed."""

        res = calc.multiplication(5, 10)

        self.assertEqual(res, 50)

    def test_division_two_number(self):
        """Test diving two numbers falied."""

        res = calc.division(10, 2)

        self.assertEqual(res, 5)
