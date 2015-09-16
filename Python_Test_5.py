#Anders Simpson-Wolf
#Practice With Vim - Using Generators and Catching Exceptions
#09/11/2015

for j in xrange(5):
    print "This is line is being generated one line at a time!"

###types of errors to try: TypeError, KeyError, ZeroDivisionError

def gonnaMakeErrors():
    try:
        print "j" + 4
    except TypeError:
        print "You can't add a string and a number, silly!"
    finally:
        print "This line gets printed no matter what."

def anotherError():
    try:
        new_dict={"name":3, "new name":54, "last name":99}
        print new_dict["last name"]
        print new_dict["does not exist"]
    except(KeyError):
        print "That key does not exist"

def finalError():
    try:
        print 5/0
    except(ZeroDivisionError):
        print "You can't divide by zero"

def noError():
    try:
        print 16/4
        print "This is" + " a string"
    except(KeyError, ZeroDivisionError,TypeError):
        print "Where did this error come from..."

gonnaMakeErrors()
anotherError()
finalError()
