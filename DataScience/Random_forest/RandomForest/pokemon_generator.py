import random as rnd

element = [
    "normal",
    "flying",
    "ice",
    "fire"]

poke = [
    "Vulpix",
    "Meowth",
    "Zubat",
    "Rattata",
    "Pidgey",
    "Ponyta",
    "Lapras",
    "Glaceon"
]

def vulpix_gen():
    chars = []
    chars.append(element[3])
    chars.append( (rnd.random()-0.3) * 10)
    chars.append()

def generate_a_poke():
    i = poke[rnd.randint(0, len(poke))-1]
    chars = []
    weight = 0
    height = 0
    attack = 0
    defence = 0
    type = ""
    rndz = 0.3


    if i is "Vulpix" :
        weight = 10
        height = 0.6
        attack = 106
        defence = 118
        type = element[3]

    elif i is "Ponyta":
        weight = 95
        height = 2
        attack = 200
        defence = 170
        type = element[3]

    elif i is "Meowth":
        weight = 6
        height = 0.5
        attack = 104
        defence = 94
        type = element[0]

    elif i is "Zubat":
        weight = 8
        height = 0.7
        attack = 90
        defence = 90
        type = element[1]
    elif i is "Rattata":
        weight = 3
        height = 0.3
        attack = 92
        defence = 86
        type = element[0]

    elif i is "Pidgey":
        weight = 3
        height = 0.3
        attack = 90
        defence = 90
        type = element[1]

    elif i is "Lapras":
        weight = 200
        height = 2.5
        attack = 190
        defence = 190
        type = element[2]

    elif i is "Glaceon":
        weight = 11
        height = 0.7
        attack = 118
        defence = 106
        type = element[2]

    weight += weight * rndz * (rnd.random() - 0.5)
    height += height * rndz * (rnd.random() - 0.5)
    attack += attack * rndz * (rnd.random() - 0.5)
    defence += defence * rndz * (rnd.random() - 0.5)

    chars = [type, weight, height, attack, defence, i]
    return chars

for i in range(5000):
    print(str(generate_a_poke()))