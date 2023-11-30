import csv
import re
input_file="/home/amanandhar/ASCC/abacus_file/thermal.txt"
output_csv="/home/amanandhar/ASCC/abacus_file/temp.csv"
output_csv1="/home/amanandhar/ASCC/abacus_file/temp2.csv"

mesh_input="/home/amanandhar/ASCC/abacus_file/thermal_mesh-500mm_15-8mm.txt"
mesh_output="/home/amanandhar/ASCC/abacus_file/mesh.csv"


def mesh_parse(input_file,output_file):
    start_line=6
    end_line=12144
    data=[]
    try:
        with open(input_file,'r') as file:
            # Initialize a line counter
            line_number = 1

            # Read and process lines within the specified range
            while True:
                line = file.readline()
                
                # Check if we have reached the end of the file
                if not line:
                    break

                # Check if the current line number is within the specified range
                if start_line <= line_number <= end_line:
                    numbers = re.findall(r'\S+', line.replace(',',''))
                    
                    if numbers[0]=='12138':
                        break

                    number_array = [float(num) for num in numbers]
                    data.append(number_array)
                    
                # Increment the line counter
                line_number += 1

        print("Reading complete.")
    except FileNotFoundError:
        print("File not found")

    print(len(data))

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Node', 'x','y','z'])  # Write header if needed
        csvwriter.writerows(data)


def thermal_parse_all(input_file,output_csv):
    start_line=20
    end_line=133807

    data=[]
    try:
        with open(input_file,'r') as file:
            # Initialize a line counter
            line_number = 1

            # Read and process lines within the specified range
            while True:
                line = file.readline()
                
                # Check if we have reached the end of the file
                if not line:
                    break

                # Check if the current line number is within the specified range
                if start_line <= line_number <= end_line:
                    numbers = re.findall(r'\S+', line)
                    
                    if len(numbers)==0:
                        print("Empty found")
                        continue
                    elif not numbers[0].isdigit() and not numbers[0].replace('.', '', 1).isdigit():
                        continue
                    else:
                        number_array = [float(num) for num in numbers]
                        data.append(number_array)
                    
                # Increment the line counter
                line_number += 1

        print("Reading complete.")
    except FileNotFoundError:
        print("File not found")

    print(len(data))

    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Node', 'Temp'])  # Write header if needed
        csvwriter.writerows(data)



#mesh_parse(mesh_input,mesh_output)

thermal_parse_all(input_file,output_csv1)