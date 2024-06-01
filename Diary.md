# Programmiertagebuch
## Algorithm
### external lift zuordnen
#### Yves - 21.5
sehr schlecht programmiert. Es hat einen for loop, daher wird einfach der erst beste und nicht der beste genommen. Deshalb unbeding for loop loswerden!!

#### besprochen mit Toni 29.5
Sobald lift losfaehrt wird er im naechstne Stock angeyeigt.
Toni bekommt Liste mit dem Neuen Element am Ende der Liste.
muss ordnen, je nach hoch oder runter.
keine Elemente doppelt vorhanden

#### Yves - 30.5
neuer zuordner:
- Lift hier? J
- wird ein Lift hier halten J
    - ist er halbvoll? J
    - wenn er vom 0 ins 6 ins 7 fahr und du vom 6 runter willst???
- naher leerer lift(wartend) J
- faehrt ein Lift in meine Richtung J
    - halbvoll?(reihenfolge) Jein
-Lift mit den wenigsten Target/leuten/nahsten
    mithilfe werte Multiplizieren mit wertigkeit (1*n(Targets)+0.5*Distanz+0.1*n(Leute)) -> tiefster Wert nimmt

#### Vayquey
Kommentar zur library pygame.
In Dokumentation unbedingt Algorithm kommentieren

#### Yves - 1.6
bloeder fall:{
    "external": {
      "storey": 5,
      "upwards": true
    }
  "state": {
    "lifts": [
      {
        "position": 0,
        "targets": [
          3,
          6
        ],
        "people": 14
      },
      {
        "position": 4,
        "targets": [
        3
        ],
        "people": 0
      },
      {
        "position": 6,
        "targets": [
          7
        ],
        "people": 1
      }

Kann man es so programmieren, dass zuerst alles angegeben wird un dann erst gekuck. also alle werte in Variabeln gespeichert
