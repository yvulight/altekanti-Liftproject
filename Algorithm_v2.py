
import json
import math

def sort_list(input,lift_number): # Funktion für das Sortieren wird erstellt
    lift_position = input['state']['lifts'][lift_number]['position'] # lift position zb. 1
    lift_targets = input['state']['lifts'][lift_number]['targets'] #Liste mit den momentanen targets zb. [5,6,7]
    all_list = [lift_position]+lift_targets # Liste mit den Positionen und den targets

    if input['input']['is_internal']: # falls dies False ist
        new_target = input['input']['internal']['storey'] #new_target ist das gwünschte Stockwerk (intern)
        direction_upwards = lift_position <= new_target # die Fahrtrichtung wird bestimmt
    else:
        direction_upwards = input['input']['external']['upwards'] # direction_upwarts wird dem Input (boolean) gleichgesetzt
        new_target = input['input']['external']['storey'] # der input für das gewünschte Stockwerk wird gespeichert

    done = False # done wird der boolean False zugeschrieben
    #Hier werden die Listen richtig sortier unter berücksichtigung der Fahrtrichtung
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
        all_list.append(new_target) # der Liste all_list wird new_target hinzugefügt

    all_list.pop(0) #
    return all_list # die Liste wird zurückgegeben


def choose_lift(input): # Funktion für die Selektion der Lifts
    #INPUT IN VARIABELN SPEICHERN
    #inputs
    where_pressed = input['input']['external']['storey']
    direction_upwards = input['input']['external']['upwards']

    #die drei state-listen
    lift_positions_list = []
    lift_targets_list = []
    lift_people_list = []
    for i in range(3): # 3, weil es drei Lifts hat
        lift_positions_list.append(input['state']['lifts'][i]['position']) # auf diesr Variabel werden die momentanen Positon der Lifts gespeichert
        lift_targets_list.append(input['state']['lifts'][i]['targets']) # uf diesr Variabel werden die momentanen targets der Lifts gespeichert
        lift_people_list.append(input['state']['lifts'][i]['people']) auf diesr Variabel werden die momentane Anzahl Personen der Lifts gespeichert

    # Überprüfe, ob ein Lift bereits an der gleichen Position ist
    for lift_number in range(3):
        if lift_positions_list[lift_number] == where_pressed and direction_upwards == (lift_positions_list[lift_number] < where_pressed) and lift_people_list[lift_number] < 10:
            return lift_number, where_pressed in lift_targets_list[lift_number]

    goodness_list = []
    # Hier wird überprüft, ob ein Lift die maximale Anzahl an Personen überschitten hat
    for lift_number in range(3): # für jeden Lift
        if lift_people_list[lift_number] >= 14: # die max. Anzahl der Personen ist 14
            goodness_list.append(float('inf'))  # Dieser Lift kann keine neuen externen Ziele annehmen
            continue

        # Berechnung welcher Lift zum gewünschten Stockwerk geht
        value = abs(lift_positions_list[lift_number] - where_pressed)
        same_direction = (lift_positions_list[lift_number] < where_pressed) == direction_upwards
        value += 0.7 * same_direction  # Werte die Fahrtrichtung höher
        value += 0.8 * abs(same_direction - 1)  # Verringere den Wert, wenn die Fahrtrichtung unterschiedlich ist

        if where_pressed in lift_targets_list[lift_number]: # wird überprüft, ob "where_pressed" schon in der liste ist
            target_index = lift_targets_list[lift_number].index(where_pressed) # gibt in der Liste ermittelt und "target_index" zugewiesen
        else:
            target_index = len(lift_targets_list[lift_number]) # das gewünschte Stockwerk wird hinten an der Liste hinzugefügt
            
        # weitere Berechnungen, die für die Auswahl der Lifts sorgen
        value += 1.2 * (target_index + 1)
        someone_enters = 1 if lift_positions_list[lift_number] == where_pressed else 0
        value += 5 * someone_enters
        goodness_list.append(value) # der Liste goodness_list wird das Resultat der Berechnungen hinzugefügt

    # Füge eine Überprüfung hinzu, um sicherzustellen, dass `goodness_list` immer die richtige Anzahl von Elementen hat
    while len(goodness_list) < 3:
        goodness_list.append(float('inf'))

    lift_number = goodness_list.index(min(goodness_list)) # auf Lift_number wird der Index des Liftes mit dem geringsten Wert gespeichert 
    already_in_targets = where_pressed in lift_targets_list[lift_number] # falls sich der gewünschte Stockwerk schon in der Liste befindet
    return lift_number, already_in_targets # lift_number und already_in_targets werden zurückgegeben

def run_algorithm(): # Funktion für das starten des Algorithmus wird definiert
    import json
    import math

    # Opening JSON file
    f = open('Input.json') # Das Json-File, das unser Input darstellt wird geöffnet 

    # returns JSON object as a dictionary
    input = json.load(f) # das Json-File wird als input "gespeichert"
    output = input.copy()
    max_people = 14 # definiert die max. Anzahl Personen, die sich in einem Lift befinden dürfen
    where_pressed = input['input']['external']['storey'] # where_pressed wird das gewünschte Stockwerk hinzugefügt



    #Falls der Input INTERNim Lift ist, muss einfach das stockwerk der Target liste hinzugefügt werden
    if input['input']['is_internal']:
        lift_number = input['input']['internal']['lift'] # auf lift_number wird der Lift gespeichert
        target = input['input']['internal']['storey'] # das gewünschte Stockwerk wird auf target gespeichert
        already_in_targets = False # wird auf False gesetzt

    #Falls der Input EXTERN ist, muss heruasgefunden werden welcher Lift die Person abhohlt
    if not input['input']['is_internal']:
        lift_number, already_in_targets = choose_lift(input)
        target = input['input']['external']['storey']
        print(lift_number, already_in_targets)


    #SORT LISTS ---- SORT
    if not already_in_targets and len(input['state']['lifts'][lift_number]['targets']) > 0: # falls die Liste mind. ein element enthält und das gewünschte Stockwerk noch nicht in der Liste ist
        lift_targets = sort_list(input, lift_number) # Liste wird sortiert
        output['state']['lifts'][lift_number]['targets'] = lift_targets # aktualisiert die Liste im output-File
    else: #Input einfach anfuegen wenn noch kein Element in targets
        lift_targets = input['state']['lifts'][lift_number]['targets'].append(target) # Es wird einfach an die Liste angefügt




    #delete Input part from Output.json
    output.pop('input') #  der ursprüngliche Input wird aus dem Output gelöscht

    f.close() # das Json-File (input) geschlossen

    with open('algo_output.json', 'w', encoding='utf-8') as v: # algo_output.json wird geöffnet, nach dem gebrauch sofort wider geschlossen und in UTF-8 geschriebe
        json.dump(output, v, ensure_ascii=False, indent=4) # output-Daten werden auf v gespeichert, nicht ASCII-Zeichen werdenin Unicode-Zeichen beibehalten

run_algorithm()
