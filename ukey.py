from random import choice
from string import digits

def gen_random_range(val=32):
    a=(''.join(choice(digits) for i in range(16)))
    return a