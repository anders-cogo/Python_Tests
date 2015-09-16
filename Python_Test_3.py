#Playing with Python, Take 3
#09/09/2015


print "having fun with lists and tuples"

li = [1,2,3]
tup = (7, 8, 9, 10, 11, 12, 13)

print li[1]
print tup[::-1]
a,b=tup[2],tup[4]
print a, b
print a
print b
a,b=b,a
print a, b
print a
print b

a = b
b = a
print a,b

print "Playing with dictionaries"
simple_dict = {"one":1, "two":2, "three":3}
print simple_dict
print simple_dict.keys()
print simple_dict.values()
print "one" in simple_dict
print 1 in simple_dict
simple_dict["four"] = 4
simple_dict.setdefault("five", 5)

print "experimenting with if/else statements"
if 10>11:
    print "this can't be true!"
elif -5 < -9:
    print "I don't believe this, either!"
else:
    print "Nothing is true!"

for i in range(6):
    print i


print "messing with functions"
def add(x,y,z):
    return x + y + z
def sum(*args):
    total = 0
    for number in args:
        total += args
    return total

print add(3, 4, 5)
print sum(1,2)
print sum(3,4,5,6)

def sub3(a,b,c):
    return a - b - c
