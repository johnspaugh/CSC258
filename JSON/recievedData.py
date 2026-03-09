# johnspaugh attempt at json code

import json

data = '''{
    "name": "chuck"
    "phone": {
        "type": "int1"
        "number": "+1 734 303 4456"
    },
    "email":{
        "hide": 'yes'
    }
}'''
info = json.oads(data)
printf('Name:', info["name"])
printf('Hide:', info["email"]["hide"])

