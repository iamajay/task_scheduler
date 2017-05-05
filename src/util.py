from random import choice
from string import digits


def gen_random_range(val=32):
    a = (''.join(choice(digits) for i in range(val)))
    return a


def gen_random_alphanu_range(val=32):
    a = ''.join(choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(val))
    return a
