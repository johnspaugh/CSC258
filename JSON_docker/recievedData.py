# johnspaugh attempt at json code

import json

data = '''{
    "username": "chuck",
    "date": datetime,
    "postcontact": yesStatus
    "phone": {
        "type": "int1"
        "number": "+1 734 303 4456"
    },
    "email":{
        "hide": 'yes'
    }
}'''
info = json.loads(data)
print('Name:', info["username"])
print('Hide:', info["email"]["hide"])

# good things to pull when examining MichealSampleData file
# display_name
# text
# created_at
# handle
# reply (Maybe if its not wierd) ref
# tags (if not have then don't include)
# indexed_at
# python map
# 25 posts #

