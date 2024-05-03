import json

# Opening JSON file
f = open('Input.json')

# returns JSON object as a dictionary
input = json.load(f)
output = input.copy()

#Tells which Elevator to do something
if input['input']['is_internal']:
    lift_number = input['input']['internal']['lift']
    target = input['input']['internal']['storey']
    output['state']['lifts'][lift_number]['targets'].append(target)

if not input['input']['is_internal']:
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']
    # jetzt kommt die heilige Frage, welcher Lift hohlt diese Person ab?
     

#targets ordnen






f.close()

with open('algo_output.json', 'w', encoding='utf-8') as v:
    json.dump(output, v, ensure_ascii=False, indent=4)
