import json
import math

def insertion(lift_position, lift_targets): #Eine Funktion wird erstellt, mit den zwei Inputs als Parameter
    if direction_upwards == True: #Hier wird überprüft, ob der Lift nach unten oder nach oben fährt

        for i in range(1,le): #Toni, warum uebernimmst du die liste so kompliyiert und umgehst doppelte??????????????
            if lift_targets[i] < lift_position:
                if lift_targets[i] not in l:
                    l.append(lift_targets[i])
                    lift_targets.pop(i)
        print(l)


        for i in range(1,le): #Nun wird die Liste sortiert, angefangen mit dem kleinsten
            if lift_targets[i] < lift_targets[i-1]:
                temp = lift_targets[i]
                j = i
                while (temp <= lift_targets[j-1] and j > 0):
                    lift_targets[j] = lift_targets[j-1]
                    j-= 1
                lift_targets[j] = temp

        print(lift_targets)


        for i in range(1,la): #Hier wird die zweite Liste sortiert, angefangen mit dem grössten
            if l[i] > l[i-1]:
                temp = l[i]
                j = i
                while (temp >= l[j-1] and j > 0):
                    l[j] = l[j-1]
                    j-= 1
                l[j] = temp

        print(l)

        for i in range(1, la): # Hier wird jedes Element der zweiten Liste an die erste Liste angehängt
            lift_targets.append(l[i])
            l.pop(i)
        print(lift_targets)



    if direction_upwards == False: #Hier wird geprüft, ob der Lift nach unten oder nach oben fährt

        for i in range(1,le):
            if lift_targets[i] < lift_position:
                if lift_targets[i] not in l:
                    l.append(lift_targets[i])
                    lift_targets.pop(i)


        for i in range(1,le): #Hier wird die Liste sortiert, angefangen mit dem grössten
            if lift_targets[i] > lift_targets[i-1]:
                temp = lift_targets[i]
                j = i
                while (temp >= lift_targets[j-1] and j > 0):
                    lift_targets[j] = lift_targets[j-1]
                    j-= 1
                lift_targets[j] = temp
            return lift_targets


        for i in range(1,la): #Hier wird die Liste sortiert, angefangen mit dem kleinsten
            if l[i] < l[i-1]:
                temp = l[i]
                j = i
                while (temp <= l[j-1] and j > 0):
                    l[j] = l[j-1]
                    j-= 1
            l[j] = temp
        print(l)


        for i in range(1, la): #Hier wird jedes Element der zweiten Liste an die erste Liste angehängt
            lift_targets.append(l[i])
            l.pop(i)
        print(lift_targets)

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

    lift_positions_list = []#liste erstellen im Format [0,3,5] mit der Position der lifte
    lift_targets_list = []
    lift_people_list = []
    for i in range(3):
        lift_positions_list.append(input['state']['lifts'][i]['position'])
        lift_targets_list.append(input['state']['lifts'][i]['targets'])
        lift_people_list.append(input['state']['lifts'][i]['people'])

    lift_people_list_sorted = lift_people_list.copy()
    lift_people_list_sorted.sort()
    lift_people_list_numbers_sorted = []
    for lift_people in lift_people_list_sorted:
        lift_people_list_numbers_sorted.append(lift_people_list.index(lift_people)) #eine Liste gemacht, die die Liftnummern mit dem leichtesten Lift zuerst enthaelt
    lift_chosen = False
    already_in_targets = False


#versuch nummer 2 29.5.24
#ist ein Lift hier?
if where_pressed in lift_positions_list:
    #Hier ist ein Lift
    lift_number = lift_positions_list.index(where_pressed)
    print('hier ist ein Lift', lift_number)

    if lift_people_list[lift_number] < (max_people-2): #falls der Lift nicht voll ist
        print('here is one that aint full')
        if where_pressed not in lift_targets_list[lift_number]:
            #liftnummer hinzufuegen
            print('and it isnt in the lsit')
            already_in_targets = False
        else:
            already_in_targets = True
            print('and it is in the list')
        lift_chosen = True


if not lift_chosen and any(where_pressed in list for list in lift_targets_list): #wird ein Lift hier halten
    #was wenn mehrere lifte hier halten werden
    print('hoi')
    for list in lift_targets_list:
        if where_pressed in list:
            lift_number = lift_targets_list.index(list)
            if lift_people_list[lift_number] < max_people/2:
                print('ein lift machts')
                already_in_targets = True
                lift_chosen = True
                #Ein lift wird hier halten und ist nur halbvoll
                #lift bereits in name, DO NOTHING auch TONII
                #continue ????

if not lift_chosen and any(not list for list in lift_targets_list): #hat ein Lift nichts zu tun
    lift_number = lift_targets_list.index([])
    print('ein hobbyloser existiert')
    if (lift_positions_list[lift_number] - where_pressed)**2 < 9:
        lift_chosen = True

if not lift_chosen: #noch keiner zugeordnet
    for lift_number in lift_people_list_numbers_sorted: #der gewichtsreihenfolge nach
        if (lift_positions_list[lift_number] - where_pressed)**2 < 9: #der Lift ist nicht weiter als 3 stockwerke entfernt
            if direction_upwards and lift_positions_list[lift_number] < where_pressed: # der
                print('lift bellow', lift_number)
                lift_chosen = True
                break
            elif not direction_upwards and lift_positions_list[lift_number] > where_pressed:
                print('in higher', lift_number)
                lift_chosen = True
                break

if not lift_chosen: #die Hoffnungslose Wahl :(
    gute_liste = []
    for lift_number in range(3):
        g_n_targets = len(lift_targets_list[lift_number])
        g_distance = math.sqrt((lift_positions_list[lift_number] - where_pressed)**2)
        g_people = lift_people_list[lift_number]

        gute_liste.append(1*g_n_targets+0.5*g_distance+0.1*g_people)
    print(gute_liste)
    lift_number = gute_liste.index(min(gute_liste))


#targets ordnen
#TONI ------------------------



if not already_in_targets:
    output['state']['lifts'][lift_number]['targets'].append(where_pressed)

#delete Input part from Output.json
output.pop('input')

f.close()

with open('algo_output.json', 'w', encoding='utf-8') as v:
    json.dump(output, v, ensure_ascii=False, indent=4)
