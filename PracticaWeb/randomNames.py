import random

consonants = ["F","B","K","G","R","P","N","M","L","D","S","T","V","H"]
vocals = ["A","E","I","O","U","Y"]
vocals_espe = ["Ä","Ü","Ö","Ë"]
probability = ["C","V","C","C","V","C","C","C","V","V"]
prob_vocals = ["N","E","N","N","N","N","E","E","N","N"]
final_leters_con = ["N","A","E","S","G","D","L","R","X","K"]
final_leters_voc = ["A","E","Ö"]
after_k = ["A","I","V","U","R","O","N","L"]

def random_names(n):
    names = []
    for i in range(n):
        name = consonants[random.randint(0, len(consonants)-1)]
        if name == "K":
            name = name + random.choice(after_k)
        else:
            name = name + vocals[random.randint(0, len(vocals)-1)]
        name_length = random.randint(2, 7)
        for j in range(name_length):
            if (j < name_length-1):
                if name[-1] in consonants and name[-2] in consonants:
                    name = choose_vocal(name)
                elif name[-1] in consonants:
                    next_let = random.choice(probability)
                    if next_let == "C":
                        name = choose_consonant(name)
                    else:
                        name = choose_vocal(name)
                else:
                    name = choose_consonant(name)
            else:
                if name[-1] in consonants and name[-2] in consonants:
                    if name[-1] == "T" and name[-2] == "S":
                        name = name + "A"
                    else:
                        name = choose_final_vocal(name)
                else:
                    name = choose_final_consonant(name)

        names.append(name)
        print(name)
    return names


def choose_final_vocal(name):
    return name + random.choice(final_leters_voc)


def choose_final_consonant(name):
    if name[-1] == "N":
        return name + "D"
    elif name[-1] == "E":
        return name + "N"
    elif name[-1] == "T":
        return name + "A"
    elif name[-1] == "I":
        return name + "G"
    else:
        return name + random.choice(final_leters_con)


def choose_vocal(name):
    next_vocal = random.choice(prob_vocals)
    if next_vocal == "E":
        vocal = random.choice(vocals_espe)
        while vocal in name:
            vocal = random.choice(vocals_espe)
        name = name + vocal
    else:
        vocal = random.choice(vocals)
        while vocal in name:
            vocal = random.choice(vocals)
        name = name + vocal
    return name


def choose_consonant(name):
    consonant = random.choice(consonants)
    cons = consonants.copy()
    cons.remove(consonant)
    while consonant in name:
        consonant = random.choice(cons)
    name = name + consonant
    return name


random_names(30)

