

class ValueTooHighError(Exception):
    pass

class ValueTooSmallError(Exception):
    def __init__(self, message, value):
        self.message = message
        self.value = value

def test_value(x):
    if x > 100:
        raise ValueTooHighError("Value is too high")
    if x < 5:
        raise ValueTooSmallError("Value to small", x)

try:
    test_value(1)
except ValueTooHighError as e:
    print(e)
except ValueTooSmallError as e:
    print(e.message, e.value)


x = 5
assert (x >= 0), "x is not positive"

try:
    a = 5/0
    b = a + '10'
except Exception as e:
    print(e)
    print("An error happened")
except TypeError as e:
    print(e)
else:
    print("Everything is fine")
finally:
    print("Cleaning up ...")