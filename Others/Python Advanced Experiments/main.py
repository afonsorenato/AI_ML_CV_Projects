from timeit import default_timer as timer
from collections import Counter

def getList():

    mylist = ["banana", "cherry", "apple"]
    print(mylist)

    myList2 = mylist
    mylist.append("lemon")
    mylist.insert(1, "blueberry")

    if "banana" in mylist:
        print("Yes")
    else:
        print("No")

    print(mylist)


def getDictionary():
    mydict = {"name": "Max", "age": 28, "city": "New York"}
    print(mydict)

    mydict2 = dict(name = "Mary", age = 27, city="Boston")
    print(mydict2)

    value = mydict["name"]
    print(value)

    mydict["email"] = "max@gmail.com"
    print(mydict)

    try:
        print(mydict["name"])
    except:
        print("Error")


def getSets():
    myset = set("Hello")
    print(myset)

    myset.add(1)
    myset.add('g')
    print(myset)

    for i in myset:
        print(i)

    myset.clear()
    print(myset)


def getString():

    my_string = "Hello world"
    print(my_string)
    substring = my_string[::-1]
    print(substring)

    if 'e' in my_string:
        print("yes")
    else:
        print("No")

    str = " Hello world"
    str = str.strip()
    print(str)

    my_string.replace("world", "Universe")
    print(my_string)

    my_list = ['a']*6
    print(my_list)

    init = timer()
    my_string = ''.join(my_list)
    print(my_string)
    fin = timer()

    print(fin-init )

    var = 3
    my_string = "The variable is %f" % var
    my_string2 = "The variable is {:.2f} and {}".format(var, var2)
    print(my_string)


def getCollections():



#getList()
#getDictionary()
#getSets()
#getString()

getCollections()