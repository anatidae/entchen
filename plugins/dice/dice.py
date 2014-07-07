# -*- coding: utf-8 -*-
"""
I wrote this when I was bored after too many compiler design lessons

the plugin part is in __init__.py ;)
"""
from plex import (
    Scanner, Range, Str, Rep, NoCase, Any, Lexicon, State, Rep1, errors,
    IGNORE, Eol
)
from StringIO import StringIO
import random
#import sys

"""
2d6+10

=>

( 3 + 5 ) + 10 = 18
"""


class DiceScanner(Scanner):

    digit1 = Range("19")
    digit = Str("0") | digit1
    number = digit1 + Rep(digit)
    dice = NoCase(Any("dw"))
    plusminus = Any("+-")

    def scan_number(self, text):
        self.stack.append(int(text))
        self.begin('gotnum')

    def scan_number2(self, text):
        # after a die, self.multiplier is set
        d = int(text)
        result = 0
        self.produce('output', '(')
        for x in xrange(self.multiplier):
            number = random.randint(1, d)
            result += number
            self.produce('output', number)
            if x + 1 < self.multiplier:
                self.produce('output', '+')
        self.produce('output', ')')
        self.stack.append(result)
        # go back to default state
        self.begin('')

    def scan_dice(self, text):
        self.multiplier = 1
        self.begin('afterdie')

    def scan_dice2(self, text):
        # stack has a multiplier on top
        self.multiplier = self.stack.pop()
        self.begin('afterdie')

    def scan_mod(self, text):
        self.stack.append(text)
        self.produce('output', text)
        self.begin('start')

    def scan_mod2(self, text):
        # calc after num: need to produce prev num
        self.produce('output', self.stack[-1])
        self.scan_mod(text)

    def handle_endline(self, text):
        self.produce('output', self.stack[-1])

    lexicon = Lexicon([
        (dice, scan_dice),
        (number, scan_number),
        (plusminus, scan_mod),
        (Rep1(Any(" ")), IGNORE),
        State('start', [
            (dice, scan_dice),
            (number, scan_number),
            (Rep1(Any(" ")), IGNORE),
        ]),
        State('gotnum', [
            (dice, scan_dice2),
            (Rep1(Any(" ")), IGNORE),
            (plusminus, scan_mod2),
            (Eol, handle_endline),
        ]),
        State('afterdie', [
            (number, scan_number2),
            (Rep1(Any(" ")), IGNORE),
        ]),
    ])

    def __init__(self, f):
        Scanner.__init__(self, self.lexicon, f)
        self.stack = []
        self.begin('start')
        self.result = 0


def roll(line):
    result = ""
    success = True
    scanner = DiceScanner(StringIO(line))
    while 1:
        try:
            token, text = scanner.read()
        except errors.UnrecognizedInput:
            result += "?"
            success = False
            break
        if token is None:
            break
        elif token is 'output':
            result += unicode(text) + " "

    if success:
        stack = scanner.stack
        res = stack[0]
        for x in xrange(len(stack) / 2):
            i = (x + 1) * 2
            if stack[i - 1] == '+':
                res += stack[i]
            elif stack[i - 1] == '-':
                res -= stack[i]
        result += "= " + unicode(res)
    return result
