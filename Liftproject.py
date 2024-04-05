import json

# Opening JSON file
f = open('Input.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['input']:
	print(i)

# Closing file
f.close()
