import re


def get_cities_data():
    with open('data/polish_cities/data', 'r') as file:
        dic = {}
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            values = re.split("  +", line)

            if len(values) == 3:
                if values[2][-1] == 'N' or values[2][-1] == 'S':
                    lat = values[1]
                    deg, minutes, direction = re.split('[°\']', lat)
                    lat_n = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)
                    longt = values[2]
                    deg, minutes, direction = re.split('[°\']', lat)
                    longt_n = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)
                    dic[values[0]] = [lat_n, longt_n]

    return dic
