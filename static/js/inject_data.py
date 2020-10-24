import json

if __name__ == "__main__":
    """Main module"""
    with open('map.js', 'w') as f_out:
        with open('map_part_1.txt', 'r') as f_in:
            f_out.write(f_in.read())
        
        with open('my_data.json') as json_file:
            data = json.load(json_file)

        json.dump(data, f_out)
        f_out.write(";\n")

        with open('map_part_2.txt', 'r') as f_in:
            f_out.write(f_in.read())
        

