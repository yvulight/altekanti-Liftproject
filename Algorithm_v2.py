
def sort_list(input,lift_number):
    lift_position = input['state']['lifts'][lift_number]['position'] # lift position zb. 1
    lift_targets = input['state']['lifts'][lift_number]['targets'] #Liste mit den momentanen targets zb. [5,6,7]
    all_list = [lift_position]+lift_targets

    if input['input']['is_internal']:
        new_target = input['input']['internal']['storey']
        direction_upwards = lift_position <= new_target
    else:
        direction_upwards = input['input']['external']['upwards']
        new_target = input['input']['external']['storey']

    done = False
    #Alles durchgehen und checken ob dazwischen mit beruecksichtigung von direction
    if direction_upwards: # hochfahren
        for i in range(1,len(all_list)):
                if all_list[i-1] <= new_target < all_list[i]:
                    all_list.insert(i, new_target)
                    done = True
                    break
    if not direction_upwards: # runterfahren
        for i in range(1,len(all_list)):
                if all_list[i-1] >= new_target > all_list[i]:
                    all_list.insert(i, new_target)
                    done = True
                    break
    if not done:
        all_list.append(new_target)

    all_list.pop(0)
    return all_list


def choose_lift(input):
    #INPUT IN VARIABELN SPEICHERN
    #inputs
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']

    #die drei state-listen
    lift_positions_list = []
    lift_targets_list = []
    lift_people_list = []
    for i in range(3):
        lift_positions_list.append(input['state']['lifts'][i]['position'])
        lift_targets_list.append(input['state']['lifts'][i]['targets'])
        lift_people_list.append(input['state']['lifts'][i]['people'])

    # Überprüfe, ob ein Lift bereits an der gleichen Position ist
    for lift_number in range(3):
        if lift_positions_list[lift_number] == where_pressed and direction_upwards == (lift_positions_list[lift_number] < where_pressed) and lift_people_list[lift_number] < 10:
            return lift_number, where_pressed in lift_targets_list[lift_number]

    goodness_list = []
    for lift_number in range(3):
        if lift_people_list[lift_number] >= 14:
            goodness_list.append(float('inf'))  # Dieser Lift kann keine neuen externen Ziele annehmen
            continue

        value = abs(lift_positions_list[lift_number] - where_pressed)
        same_direction = (lift_positions_list[lift_number] < where_pressed) == direction_upwards
        value += 0.7 * same_direction  # Werte die Fahrtrichtung höher
        value += 0.8 * abs(same_direction - 1)  # Verringere den Wert, wenn die Fahrtrichtung unterschiedlich ist

        if where_pressed in lift_targets_list[lift_number]:
            target_index = lift_targets_list[lift_number].index(where_pressed)
        else:
            target_index = len(lift_targets_list[lift_number])

        value += 1.2 * (target_index + 1)
        someone_enters = 1 if lift_positions_list[lift_number] == where_pressed else 0
        value += 5 * someone_enters
        goodness_list.append(value)

    # Füge eine Überprüfung hinzu, um sicherzustellen, dass `goodness_list` immer die richtige Anzahl von Elementen hat
    while len(goodness_list) < 3:
        goodness_list.append(float('inf'))

    lift_number = goodness_list.index(min(goodness_list))
    already_in_targets = where_pressed in lift_targets_list[lift_number]
    return lift_number, already_in_targets

def run_algorithm():
    import json
    import math

    # Opening JSON file
    f = open('Input.json')

    # returns JSON object as a dictionary
    input = json.load(f)
    output = input.copy()
    max_people = 14
    where_pressed = input['input']['external']['storey']



    #Falls der Input INTERNim Lift ist, muss einfach das stockwerk der Target liste hinzugefügt werden
    if input['input']['is_internal']:
        lift_number = input['input']['internal']['lift']
        target = input['input']['internal']['storey']
        already_in_targets = False

    #Falls der Input EXTERN ist, muss heruasgefunden werden welcher Lift die Person abhohlt
    if not input['input']['is_internal']:
        lift_number, already_in_targets = choose_lift(input)
        target = input['input']['external']['storey']
        print(lift_number, already_in_targets)


    #SORT LISTS ---- SORT
    if not already_in_targets and len(input['state']['lifts'][lift_number]['targets']) > 0:
        lift_targets = sort_list(input, lift_number)
        output['state']['lifts'][lift_number]['targets'] = lift_targets
    else: #Input einfach anfuegen wenn noch kein Element in targets
        lift_targets = input['state']['lifts'][lift_number]['targets'].append(target)




    #delete Input part from Output.json
    output.pop('input')

    f.close()

    with open('algo_output.json', 'w', encoding='utf-8') as v:
        json.dump(output, v, ensure_ascii=False, indent=4)


run_algorithm()