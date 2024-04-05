import json

# Opening JSON file
f = open('Input.json')

# returns JSON object as a dictionary
input = json.load(f)
output = input.copy()

#Tells which Elevator to do something
if input['input']['is_internal'] == True:
    print("it is internal")

print(output)




f.close()
