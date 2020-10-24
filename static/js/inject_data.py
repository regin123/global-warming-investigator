import json
import os
import sys

if __name__ == "__main__":
    """Main module"""

    if len(sys.argv) != 2:
        print("Program takes exactly one argument")
        quit()
    data_name = sys.argv[1]
    # print(data_name)
    map_txt_folder = os.path.join(os.getcwd(), 'map_txt') 
    data_folder = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'data')
    with open('map.js', 'w') as f_out:
        with open(os.path.join(map_txt_folder, 'map_part_1.txt'), 'r') as f_in:
            f_out.write(f_in.read())
        
        with open(os.path.join(data_folder, data_name)) as json_file:
            data = json.load(json_file)

        json.dump(data, f_out)
        f_out.write(";\n")

        with open(os.path.join(map_txt_folder, 'map_part_2.txt'), 'r') as f_in:
            f_out.write(f_in.read())


