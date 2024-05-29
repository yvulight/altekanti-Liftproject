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
    lift_people_list = []
    for i in range(3):
        lift_positions_list.append(input['state']['lifts'][i]['position'])
        lift_targets_list.append(input['state']['lifts'][i]['targets'])
        lift_people_list.append(input['state']['lifts'][i]['people'])

#versuch nummer 2 29.5.24
#ist ein Lift hier?
if where_pressed in lift_positions_list:
    lift_number = where_pressed
    output['state']['lifts'][lift_number]['targets'].append(where_pressed)
elif direction_upwards: #2. Lift < halbvoll und auf der Durchfahrt upwards (platz <where_pressed<ziel)
    for lift_number in range(0,3)



#dangerous passage: wenn error, ev. weil nichts in target liste-> 2.
'''
    for lift_number in range(3):
        if where_pressed == lift_positions_list[lift_number]: #1. ist ein Lift hier?
            #Dieser Lift machts
            output['state']['lifts'][lift_number]['targets'].append(where_pressed)
            break
        elif direction_upwards and lift_people_list[lift_number] < max_people/2 and (lift_positions_list[lift_number] <= where_pressed <= lift_targets_list[lift_number][0]): #2. Lift < halbvoll und auf der Durchfahrt upwards (platz <where_pressed<ziel)
            output['state']['lifts'][lift_number]['targets'].insert(0, where_pressed)
            break
        elif not direction_upwards and lift_people_list[lift_number] < max_people/2 and (lift_positions_list[lift_number] >= where_pressed >= lift_targets_list[lift_number][0]): #2. Lift < halbvoll und auf der Durchfahrt (pos>where_pressed>target)
            output['state']['lifts'][lift_number]['targets'].insert(0, where_pressed)
            break
        #3. leerer Lift nah(x>2)

    #ev. check ob Lift hier ist; ob ein Lift vorbeifähret(der noch platz hat);welcher Lift denn sonst der nächste ist, falls keiner was macht
'''



#targets ordnen
#falls doppelt vorhanden -> loeschen




#delete Input part from Output.json
#output.pop('input')

f.close()

with open('algo_output.json', 'w', encoding='utf-8') as v:
    json.dump(output, v, ensure_ascii=False, indent=4)
