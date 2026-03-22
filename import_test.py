import math
import random as rnd
from math import sqrt, sin
from random import choice

def test_imports():
    x = sqrt(16)
    y = sin(0)
    z = rnd.uniform(0, 1)
    item = choice(["a", "b", "c"])
    return x, y, z, item

print(test_imports())