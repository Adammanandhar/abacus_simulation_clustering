import re
import csv
from io import StringIO


class DataExtractor:
    def __init__(self, input_file, output_file_path):
        self.input_file = input_file
        self.output_file_path = output_file_path
        

    def extract_and_save_data(self,start_line):
        """
        Extracts data from a text file starting from a specific line and writes it to another text file.

        This method reads the content of the input file specified by `self.input_file`. It starts recording
        the lines into the output file specified by `self.output_file_path` when it encounters a line that
        contains the `start_line` string. The recording continues until the end of the file.

        Parameters:
        start_line (str): A string that triggers the start of data recording. The method begins to
                        write lines to the output file from the point it encounters a line containing this string.

        Raises:
        FileNotFoundError: If the input file specified by `self.input_file` does not exist.
        Exception: If any other error occurs during file reading or writing.

        Returns:
        None: This method does not return any value but prints a message upon successful completion or
            if an exception is encountered.
        """
        try:
            # First, count the total number of lines in the file
            with open(self.input_file, 'r') as file:
                total_lines = sum(1 for _ in file)

            start_recording = False
            current_line = 0
            last_reported_progress = -10

            with open(self.input_file, 'r') as input, open(self.output_file_path, 'w') as txt_file:
                for line in input:
                    current_line += 1

                    if start_recording:
                        txt_file.write(line)

                    elif start_line in line:
                        start_recording = True

                    # Calculate and report progress
                    progress = (current_line / total_lines) * 100
                    if progress - last_reported_progress >= 10:
                        print(f"Progress: {progress:.0f}%")
                        last_reported_progress = progress

            print(f"Data extracted and saved to {self.output_file_path}")

        except FileNotFoundError:
            print(f"File not found: {self.input_file}")
        except Exception as e:
            print(f"An error occurred: {e}")



    def split_file(self,split_range):
        """
        Splits a portion of the input file and writes it to an output file.

        This method reads the first `split_range` lines from the file specified by `self.input_file`
        and writes them to a new file specified by `self.output_file_path`.

        Parameters:
        split_range (int): The number of lines to be read from the input file and written to the output file.

        The method does not return any value and assumes the input file is readable and the output file is writable.
        """
        with open(self.input_file, 'r') as input:
            with open(self.output_file_path, 'w') as output_file:
                for i in range(split_range):
                    line = input.readline()
                    output_file.write(line)




    def temperature_to_csv(self):
        """
        Extracts temperature data from the input file and writes it to a CSV file.

        Reads lines matching a specific pattern (1      2.4500000E+02) from `self.input_file`
        and writes them to `self.output_file_path` in CSV format. The CSV file will have two columns: 'NODE' and 'TEMP'.

        Assumes the input file format is consistent with the expected pattern and that both input and output files
        are properly set up for reading and writing, respectively.
        """

        with open(self.input_file, 'r') as file:
            text = file.read()

        # Regular expression pattern to match the lines with node data
        pattern = r"\s*(\d+)\s+([\d.E+-]+)"
        
        # Extracting the matched lines
        matches = re.findall(pattern, text)

        # Writing to the CSV file
        with open(self.output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["NODE", "TEMP"])  # Writing header
            writer.writerows(matches)



