import json
from json import JSONEncoder


class UserEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, User):
            return {"name": o.name, "age": o.age, o.__class__.__name__: True}
        return JSONEncoder.default(self, o)


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def encode_user(o):
    if isinstance(o, User):
        return {"name": o.name, "age": o.age, o.__class__.__name__: True}
    else:
        raise TypeError("Object user type is not JSON")


def firstTestJSON():
    person = {"name": "John", "age": 30, "city": "New York", "hasChildren": False, "titles": ["engineer", "programmer"]}
    personJSON = json.dumps(person, indent=4, sort_keys=True)
    print(personJSON)

    with open('person.json', 'w') as file:
        json.dump(person, file, indent=4)

    person = json.loads(personJSON)
    print(person)


user = User("Max", 27)
userJSON = json.dumps(user, default=encode_user)
print(userJSON)

userJSON = json.dumps(user, cls=UserEncoder)
print(userJSON)

user = json.loads(userJSON)
print(user)