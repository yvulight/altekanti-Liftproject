timport json

# Opening JSON file
f = open('Input.json')

# returns JSON object as a dictionary
input = json.load(f)
output = input.copy()

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
    #ev. check ob Lift hier ist; ob ein Lift vorbeifähret(der noch platz hat);welcher Lift denn sonst der nächste ist, falls keiner was macht
    
     

#targets ordnen






f.close()

with open('algo_output.json', 'w', encoding='utf-8') as v:
    json.dump(output, v, ensure_ascii=False, indent=4)
