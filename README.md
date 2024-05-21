# altekanti-Liftproject
## Intro
An Algorithm/Simulation of 3 Lifts and 7 storeys
It is a replica of the Elevators at the Alte Kanti Headquater.

## Explenation for Yves
Also, immer wenn en Input bet'tiget wird, wird es input.json file an algorithm gschickt. de algorithmus entscheidet, welle lift das als Target added. Er git en algo_out.json us, wo aehnlich wie s input.json isch us. das algo_out.json wird ans darstellungsskript gschickt, wo neui uftraeg bechunt. und anhand dem entscheidet das Draw.py isch mit Tkinter und duet alle 50ms updaten und die neuen Auftraege beachten.
Viel spass bi dem mini herre :)

## new Explanation
1. Input Fila en ALgo
2. ALgo gibt auftrag weiter, ordnet -> Output.json fast wie input.json nur ohne Inpunt

## Prioritaeten des Lifts 21.5 - Yves
**extern gedrueckt**
1. Lift steht gerade hier
2. Lift der nichts zu tun hat und inherhalb 2 stockwerken hier ist
3. leerere lift auf der Durchfahrt.
else: der lift, mit den wenigsten targets/am nahsten
