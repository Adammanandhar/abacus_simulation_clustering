import pandas as pd
import re
import os
import sys
import re



class DataProcessor:
    def __init__(self, input_file_path, output_file_path_transformed, temp_dir="temp_data"):
        self.input_file_path = input_file_path
        self.output_file_path_transformed = output_file_path_transformed
        self.temp_dir = temp_dir
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

    def process_file(self):
        pattern = r"\s*(\d+)\s+([\d.E+-]+)"
        temp_file_count = 0
        matches = []

        with open(self.input_file_path, 'r') as file:
            for line in file:
                match = re.findall(pattern, line)
                if match:
                    matches.append(match[0])
                    # Write to temp file and reset matches list if it grows too large
                    if len(matches) > 3437700:
                        print("Total File covered: ",(temp_file_count*20)/14000," %")
                        temp_file_path = os.path.join(self.temp_dir, f"temp_{temp_file_count}.csv")
                        pd.DataFrame(matches, columns=["NODE", "TEMP"]).to_csv(temp_file_path, index=False)
                        temp_file_count += 1
                        matches = []

        # Process any remaining matches
        if matches:
            temp_file_path = os.path.join(self.temp_dir, f"temp_{temp_file_count}.csv")
            pd.DataFrame(matches, columns=["NODE", "TEMP"]).to_csv(temp_file_path, index=False)

        # Aggregate results from temp files
        temp_files = [os.path.join(self.temp_dir, f) for f in os.listdir(self.temp_dir) if f.startswith("temp_")]
        df_list = [pd.read_csv(f) for f in temp_files]
        full_df = pd.concat(df_list)

        print("Grouping the temperature history based on Nodes")
        # Transform the data
        transformed_df = (full_df.assign(col=full_df.groupby('NODE').cumcount())
                            .pivot(index='NODE', columns='col', values='TEMP')
                            .rename(columns=lambda x: f'TEMP_{x+1}'))

        # Save the transformed data
        transformed_df.to_csv(self.output_file_path_transformed)

        # Clean up temporary files
       # for f in temp_files:
        #    os.remove(f)
    
    def sort_numerically(self,filename):
        numbers = re.findall(r'\d+', filename)
        return int(numbers[0]) if numbers else filename
        
    def aggregate_csv_data(self, temp_dir, output_csv_path):
        # List to hold data from all CSV files
        all_data = []
        
        # Read each CSV file and store the data
        for filename in sorted(os.listdir(temp_dir), key=self.sort_numerically):
            print("working with: ", filename)
            if filename.endswith('.csv'):
                file_path = os.path.join(temp_dir, filename)
                df = pd.read_csv(file_path)
                all_data.append(df)
        
        
        # Concatenate all data into a single DataFrame
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Group by 'NODE' and create a new 'TEMP_x' column for each temperature value per node
        combined_df['TEMP_ID'] = combined_df.groupby('NODE').cumcount() + 1
        aggregated_df = (combined_df.set_index(['NODE', 'TEMP_ID'])
                                    .unstack()
                                    .sort_index(level=1, axis=1))
        
        # Flatten the MultiIndex columns and create a simple one-level index
        aggregated_df.columns = [f'TEMP_{i}' for i in range(1, len(aggregated_df.columns) + 1)]
        aggregated_df.reset_index(inplace=True)
        
        # Replace NaN values with a neutral value or remove them
        # aggregated_df.fillna(value=np.nan, inplace=True)
        
        # Save to CSV
        aggregated_df.to_csv(output_csv_path, index=False)


