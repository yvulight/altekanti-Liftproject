import json
import math

def insertion_sort(ver, direction):
    for i in range(1, len(ver)):
        key = ver[i]
        j = i - 1
        if direction == "up":
            while j >= 0 and ver[j] > key:
                ver[j + 1] = ver[j]
                j -= 1
        elif direction == "down":
            while j >= 0 and ver[j] < key:
                ver[j + 1] = ver[j]
                j -= 1
        ver[j + 1] = key
    return ver

def choose_lift(input):
    # input_data IN VARIABELN SPEICHERN
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']

    # die drei state-listen
    lift_positions_list = []
    lift_targets_list = []
    lift_people_list = []
    for i in range(3):
        lift_positions_list.append(input['state']['lifts'][i]['position'])
        lift_targets_list.append(input['state']['lifts'][i]['targets'])
        lift_people_list.append(input['state']['lifts'][i]['people'])

    # Überprüfe, ob ein Lift bereits an der gleichen Position ist
    for lift_number in range(3):
        if lift_positions_list[lift_number] == where_pressed:
            return lift_number, True

    goodness_list = []
    for lift_number in range(3):
        if lift_people_list[lift_number] >= 14:
            goodness_list.append(float('inf'))  # Dieser Lift kann keine neuen externen Ziele annehmen
            continue

    goodness_list = []
    for lift_number in range(3):
        value = abs(lift_positions_list[lift_number] - where_pressed)  # return the absolute value 
        same_direction = (lift_positions_list[lift_number] < where_pressed) == direction_upwards
        value += 0.7 * same_direction  # Werte die Fahrtrichtung höher
        value -= 0.8 * (not same_direction)  # Verringere den Wert, wenn die Fahrtrichtung unterschiedlich ist

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

# Opening JSON file
f = open('Input.json')

# returns JSON object as a dictionary
input = json.load(f)
output = input.copy()
max_people = 14

# Falls der input INTERN im Lift ist, muss einfach das Stockwerk der Target-Liste hinzugefügt werden
if input['input']['is_internal']:
    lift_number = input['input']['internal']['lift']
    target = input['input']['internal']['storey']
    already_in_targets = False
else:
    lift_number, already_in_targets = choose_lift(input)
    target = input['input']['external']['storey']

print(f"Selected Lift: {lift_number}")
print(f"Already in Targets: {already_in_targets}")

# SORT LISTS ---- SORT
if not already_in_targets:
    lift_position = input['state']['lifts'][lift_number]['position']
    lift_targets = input['state']['lifts'][lift_number]['targets']
    direction = "up" if lift_position <= target else "down"
    sorted_targets = insertion_sort(lift_targets + [target], direction)
    output['state']['lifts'][lift_number]['targets'] = sorted_targets

# delete input_data part from Output.json
output.pop('input')

f.close()

with open('algo_output.json', 'w', encoding='utf-8') as v:
  json.dump(output, v, ensure_ascii=False, indent=4)
