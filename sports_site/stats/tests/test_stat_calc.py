from django.test import TestCase

from stats.stat_calc import (_convert_to_int, _normalize_str_length,
    _convert_to_str, _convert_to_str_pitching)



class Stats_ConvertToIntTests(TestCase):
    """
    Tests _convert_to_int function from stats/stat_calc.py
    """
    def test_3_digit_convert_to_int(self):
        string_stat = '.300'
        converted = 300
        self.assertEqual(converted, _convert_to_int(string_stat))


    def test_4_digit_convert_to_int(self):
        string_stat = '1.100'
        converted = 1100
        self.assertEqual(converted, _convert_to_int(string_stat))



class Stats_NormalizeStrLengthTests(TestCase):
    """
    Tests _normalize_str_length function from stats/stat_calc.py
    """

    def test_normalize_str_length_4(self):
        string_stat = '.3'
        converted = '.300'
        self.assertEqual(converted, _normalize_str_length(string_stat, 4))

    def test_normalize_str_length_5(self):
        string_stat = '1.1'
        converted = '1.100'
        self.assertEqual(converted, _normalize_str_length(string_stat, 5))

    def test_normalize_str_length_5_2(self):
        string_stat = '.1'
        converted = '.1000'
        self.assertEqual(converted, _normalize_str_length(string_stat, 5))


class Stats_ConvertToStrTests(TestCase):
    """
    Tests _convert_to_str function from stats/stat_calc.py
    """
    def test_convert_to_str_less_than_1(self):
        float_stat = .3
        converted = '.300'
        self.assertEqual(converted, _convert_to_str(float_stat))


    def test_convert_to_str_less_than_1_leading_zero(self):
        float_stat = 0.3
        converted = '.300'
        self.assertEqual(converted, _convert_to_str(float_stat))


    def test_convert_to_str_greater_than_1(self):
        float_stat = 1.1
        converted = '1.100'
        self.assertEqual(converted, _convert_to_str(float_stat))


    def test_convert_to_str_none(self):
        float_stat = None
        converted = '.000'
        self.assertEqual(converted, _convert_to_str(float_stat))


    def test_convert_to_str_0(self):
        float_stat = 0
        converted = '.000'
        self.assertEqual(converted, _convert_to_str(float_stat))


    def test_convert_to_str_long_float(self):
        float_stat = .3333333333333333333333333
        converted = '.333'
        self.assertEqual(converted, _convert_to_str(float_stat))


class Stats_ConvertToStrPitchingTests(TestCase):
    """
    Tests _convert_to_str_pitching function from stats/stat_calc.py

    TODO: Fix .3 --> .30 instead of 0.30
    """
    def test_convert_to_str_pitching_less_than_1(self):
        float_stat = .3
        converted = '.30'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))


    def test_convert_to_str_pitching_less_than_1_leading_zero(self):
        float_stat = 0.3
        converted = '.30'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))


    def test_convert_to_str_pitching_greater_than_1(self):
        float_stat = 1.1
        converted = '1.10'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))


    def test_convert_to_str_pitching_none(self):
        float_stat = None
        converted = '.000'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))


    def test_convert_to_str_pitching_0(self):
        float_stat = 0
        converted = '0.00'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))


    def test_convert_to_str_pitching_long_float(self):
        float_stat = 0.3333333333333333333333333
        converted = '.33'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))

    def test_convert_to_str_pitching_long_float_greater_than_1(self):
        float_stat = 1.3333333333333333333333333
        converted = '1.33'
        self.assertEqual(converted, _convert_to_str_pitching(float_stat))