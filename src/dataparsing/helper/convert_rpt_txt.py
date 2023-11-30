file_path="/home/amanandhar/ASCC/abacus_file/abaqus.rpt"
output_file="/home/amanandhar/ASCC/abacus_file/thermal.txt"
try:
    with open(file_path, 'r') as rpt_file:
        rpt_contents=rpt_file.read()
    
    with open(output_file,'w') as txt_file:
        txt_file.write(rpt_contents)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
