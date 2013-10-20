#import pytest
from dice import roll
import re


class TestDice:

    def test_simple(self):
        x = roll('d6')
        r = re.findall(r'\( [1-6] \) = [1-6]', x)
        assert len(r) == 1

    def test_two(self):
        x = roll('2d6')
        r = re.findall(r'\( [1-6] \+ [1-6] \) = \d+', x)
        assert len(r) == 1

    def test_result(self):
        x = roll('2d6')
        r = re.findall(r'\( ([1-6]) \+ ([1-6]) \) = (\d+)', x)
        assert len(r) == 1
        assert int(r[0][0]) + int(r[0][1]) == int(r[0][-1])

    def test_bigger(self):
        x = roll('2w1000')
        r = re.findall(r'\( (\d+) \+ (\d+) \) = (\d+)', x)
        assert len(r) == 1
        assert int(r[0][0]) + int(r[0][1]) == int(r[0][-1])

    def test_addition(self):
        x = roll('2w20+5')
        r = re.findall(r'\( (\d+) \+ (\d+) \) \+ (5) = (\d+)', x)
        assert len(r) == 1
        assert int(r[0][0]) + int(r[0][1]) + int(r[0][2]) == int(r[0][-1])
