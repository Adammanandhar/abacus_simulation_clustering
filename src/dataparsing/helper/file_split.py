# Open the .dat file in read mode
with open(r'C:\Users\aayush.manandhar\Documents\Abacus_file_parser\src\data\synthetic_datagen.dat', 'r') as dat_file:
    # Open a new text file in write mode
    with open('sample_thermal.txt', 'w') as output_file:
        # Loop through the first 1000 lines of the .dat file
        for i in range(700000):
            # Read a line from the .dat file
            line = dat_file.readline()
            # Write the line to the new text file
            output_file.write(line)
