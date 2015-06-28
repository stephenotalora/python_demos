__author__ = 'jonathano'

import random
import math

hour = 3
ones = str(hour % 10)
print ones
tens = str(hour // 10)
print tens

print tens + ones + ':00'

def getRand():
    random.seed()
    return random.randrange(0, 6)

r = getRand()
print "rand number =", r, "the type of random num is: ", type(r)

a = True
b = False

print a, b
print not a # should equal to false
print a and b # should equal to false
print a or b # should equal to true
x = 3
print x

def greet(friend, money):
    if friend and (money > 10):
        print "HI!"
        money -= 20
    elif friend: "Hello!"
    else: print "Hello!"
    return money

money = 50.00
print "my pockets have: ", money
money = greet(True, money)
print "my pockets now have: ", money

money = greet(True, money)
print "my pockets now have: ", money

money = greet(True, money)
print "my pockets now have: ", money

money = greet(True, money)
print "my pockets now have: ", money

print 10 -- 2


def func(x):
    return (-5 * (x**5)) + (69 * (x**2)) - 47

print func(0), func(1), func(2), func(3)


## rate period
def futureValue(presentValue, annualRate, periodsPerYear, years):
    """
    :param presentValue:
    :param annualRate:
    :param periodsPerYear:
    :param years:
    :return:
    """
    # determines future value
    ratePerPeriod = annualRate / periodsPerYear
    periods = periodsPerYear * years
    totalRate = 1 + ratePerPeriod
    return presentValue * (totalRate)**periods

print 'future value = %.4f' % futureValue(1000, (2/float(100)), 365, 3)


def polygonArea(numOfSides, lengthPerSide):
    # the foruma to determine a poly area is 1/4 n s^2 / tan(pi/n)
    nominator = 1/4.0 * (numOfSides * (lengthPerSide**2))
    denom = math.tan(math.pi/float(numOfSides))
    return nominator / denom

print "the polygon area is %.4f " % polygonArea(7, 3)



def project_to_distance(point_x, point_y, distance):
    dist_to_origin = math.sqrt(point_x**2 + point_y**2)
    scale = distance / dist_to_origin
    print "%.4f %.4f" % (point_x * scale, point_y * scale)

project_to_distance(2, 7, 4)

print not (True or (not False))

print (123//10) % 10

# False  False True False
print not (True or not True)
print not (True or not False)
print not (False or not True)
print not (False or not False)