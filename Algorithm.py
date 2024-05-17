import json

# Opening JSON file
f = open('Input.json')

# returns JSON object as a dictionary
input = json.load(f)
output = input.copy()
max_people = 14

#Falls der Input im Lift ist, muss einfach das stockwerk der Target liste hinzugefügt werden
if input['input']['is_internal']:
    lift_number = input['input']['internal']['lift']
    target = input['input']['internal']['storey']
    output['state']['lifts'][lift_number]['targets'].append(target)

#Falls der Input extern ist, muss heruasgefunden werden welcher Lift die Person abhohlt
if not input['input']['is_internal']:
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']
    # jetzt kommt die heilige Frage, welcher Lift hohlt diese Person ab?
    lift0_position = input['state']['lifts'][0]['position']
    lift1_position = input['state']['lifts'][1]['position']
    lift2_position = input['state']['lifts'][2]['position']
    lift0_target = input['state']['lifts'][0]['targets']
    lift1_target = input['state']['lifts'][1]['targets']
    lift2_target = input['state']['lifts'][2]['targets']

    lift_positions_list = []#liste erstellen im Format [0,3,5] mit der Position der lifte
    lift_targets_list = []
    for i in range(3):
        lift_positions_list.append(input['state']['lifts'][i]['position'])
        lift_targets_list.append(input['state']['lifts'][i]['targets'])

    #1. ist ein Lift hier?
    for lift_number in range(3):
        if where_pressed in lift_positions_list[lift_number]:
            #Dieser Lift machts
            output['state']['lifts'][lift_number]['targets'].append(where_pressed)

    #2. Lift nicht voll auf der Durchfahrt
    #3. leerer Lift nah(x>2)

    #ev. check ob Lift hier ist; ob ein Lift vorbeifähret(der noch platz hat);welcher Lift denn sonst der nächste ist, falls keiner was macht
    



#targets ordnen






f.close()

with open('algo_output.json', 'w', encoding='utf-8') as v:
    json.dump(output, v, ensure_ascii=False, indent=4)
