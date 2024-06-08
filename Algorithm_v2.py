import json
import math

def sort_list(input,lift_number):
    lift_position = input['state']['lifts'][lift_number]['position'] # lift position zb. 1
    lift_targets = input['state']['lifts'][lift_number]['targets'] #Liste mit den momentanen targets zb. [5,6,7]
    all_list = [lift_position]+lift_targets

    if input['input']['is_internal']:
        new_target = input['input']['internal']['storey']
        if lift_position > new_target:
            direction_upwards = False
        else:
            direction_upwards = True
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

    #GENERIERTE lISTEN
    #n(targets)
    #distance
    #direction
    #where_pressed in targets
    n_targets_list = []
    distance_list = []
    direction_same_list = []
    where_pressed_in_targets_list = []
    someone_enters = []

    for lift_number in range(3):
        n_targets_list.append(len(lift_targets_list[lift_number])) # anzahl Targets des Lifts
        distance_list.append(math.sqrt((lift_positions_list[lift_number] - where_pressed)**2)) # distanz zum Input(where_pressed)

        # die direction_upwards True or False or ''
        if len(lift_targets_list[lift_number]) > 0: #Wenn der Lift mind. ein Target hat
            if lift_positions_list[lift_number] < lift_targets_list[lift_number][0] and direction_upwards:
                direction_same_list.append(1) # same direction up
            elif lift_positions_list[lift_number] > lift_targets_list[lift_number][0] and not direction_upwards:
                direction_same_list.append(1) # same direction down
            elif lift_positions_list[lift_number] < lift_targets_list[lift_number][0] and (where_pressed == 7 and not direction_upwards):
                direction_same_list.append(1.5 - (distance_list[lift_number]/5)) # Person top down, lift on its way to turn
            elif lift_positions_list[lift_number] > lift_targets_list[lift_number][0] and (where_pressed == 0 and direction_upwards):
                direction_same_list.append(1.5 - (distance_list[lift_number]/5)) # Lift umdrehen, distance weil einfluss wie weit weg er noch ist
            else:
                direction_same_list.append(0) # Nothing
        else:
            direction_same_list.append(0) # Nothing

        #where_pressed in targets
        if where_pressed in lift_targets_list[lift_number] and direction_same_list[lift_number] > 1: # direction_same weil wenn verschieden direction ist wertlos
            in_targets_temp = lift_targets_list[lift_number].index(where_pressed)
            where_pressed_in_targets_list.append(in_targets_temp) #das wievielte target in die liste mal 0 oder 1 ob es die gleiche richtung hat
        else:
            where_pressed_in_targets_list.append(9) # False, 7 ist der schlechteste Wert, den es oben annehmen kann

        #someone_enters
        if len(lift_targets_list[lift_number]) == 1 and lift_targets_list[lift_number][0] == lift_positions_list[lift_number]:
            #jemand steigt ein
            someone_enters.append(1)
        else:
            someone_enters.append(0)

    print(n_targets_list, distance_list, direction_same_list, where_pressed_in_targets_list, someone_enters)
    lift_chosen = False
    already_in_targets = False




    #AUSWAHLVERFAHREN!!!
    #Lift hier?
    #Wertigkeit
    if where_pressed in lift_positions_list: #wenn der Lift hier ist
        lift_number = lift_positions_list.index(where_pressed)
        if lift_people_list[lift_number] < max_people/2:
            lift_chosen = True

    #GUTIGKEITSVERFAHREN!!
    if not lift_chosen:
        goodness_list = []
        for lift_number in range(3):
            value = 0.4 * (lift_people_list[lift_number]) #0,1,2...14
            value = 1 * (n_targets_list[lift_number]) + value # 0,1,2...7
            value = 0.9 * (distance_list[lift_number]) + value # 0,1,2...6
            value = 2 * (2-direction_same_list[lift_number] ) + value # 1,0 (Same, not same)
            value = 1.2 * (where_pressed_in_targets_list[lift_number] + 1) + value # 0,1,2...7 oder 7 (wievieltes oder nicht drin->7)
            value = 5 * someone_enters[lift_number] + value # 0,1 jemand steigt ein sind 15 punkte
            goodness_list.append(value)
        print(goodness_list)
        lift_number = goodness_list.index(min(goodness_list))
        lift_chosen = True

    if where_pressed in lift_targets_list[lift_number]:
        already_in_targets = True

    print('already_in_targets', already_in_targets)
    return lift_number,already_in_targets








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
