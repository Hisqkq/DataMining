import os


def load_movie_names():
    Names = {}

    itemfile = os.path.join('data', 'u.item')
    with open(itemfile, "r", encoding="ISO-8859-1") as f:
        for line in f:
            split = line.split('|')[:2]
            Names[split[0]] = split[1]
            
    return(Names)