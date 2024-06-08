def sort_list(input, lift_number):
    lift_position = input['state']['lifts'][lift_number]['position']
    lift_targets = input['state']['lifts'][lift_number]['targets']
    all_list = [lift_position] + lift_targets

    if input['input']['is_internal']:
        new_target = input['input']['internal']['storey']
        direction_upwards = lift_position <= new_target
    else:
        direction_upwards = input['input']['external']['upwards']
        new_target = input['input']['external']['storey']

    done = False
    if direction_upwards:
        for i in range(1, len(all_list)):
            if all_list[i-1] <= new_target < all_list[i]:
                all_list.insert(i, new_target)
                done = True
                break
    else:
        for i in range(1, len(all_list)):
            if all_list[i-1] >= new_target > all_list[i]:
                all_list.insert(i, new_target)
                done = True
                break

    if not done:
        all_list.append(new_target)

    all_list.pop(0)  # Entferne die initiale Aufzugsposition
    return all_list

def choose_lift(input):
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']

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

import json
k = 0
# Simulierte Eingabedaten
input_data = {
    "input": {
        "is_internal": False,
        "external": {
            "storey": 5,
            "upwards": True
        },
        "internal": {
            "lift": k,
            "storey": 5
        }
    },
    "state": {
        "lifts": [
            {
                "position": 2,
                "targets": [0],
                "people": 0
            },
            {
                "position": 6,
                "targets": [7],
                "people": 0
            },
            {
                "position": 4,
                "targets": [6],
                "people": 0
            }
        ]
    }
}

# Initialisieren der Ausgabedaten
output = input_data.copy()
max_people = 14
where_pressed = input_data['input']['external']['storey']

# Auswahl des Lifts und Zielgeschosses
if input_data['input']['is_internal']:
    lift_number = input_data['input']['internal']['lift']
    target = input_data['input']['internal']['storey']
    already_in_targets = False

    # Benutzereingabe für das Zielstockwerk
    new_target = int(input("Welches Stockwerk möchten Sie erreichen?\n"))
    new_people = int(input("Wie viele Menschen steigen ein?\n"))
    input_data['input']['internal']['storey'] = new_target
    k = lift_number
else:
    lift_number, already_in_targets = choose_lift(input_data)
    target = input_data['input']['external']['storey']

# Welcher Lift wurde ausgewählt?
print(f"Selected Lift: {lift_number}")
print(f"Already in Targets: {already_in_targets}")

# Sortieren der Ziel-Liste
if not already_in_targets:
    if input_data['state']['lifts'][lift_number]['targets']:
        lift_targets = sort_list(input_data, lift_number)
    else:
        lift_targets = [target]
else:
    lift_targets = input_data['state']['lifts'][lift_number]['targets']

# Aktualisieren der Ziel-Liste des gewählten Aufzugs
output['state']['lifts'][lift_number]['targets'] = lift_targets

# Entfernen des Eingabeteils aus der Ausgabe
output.pop('input')

# Ergebnis ausgeben
print(json.dumps(output, ensure_ascii=False, indent=4))
