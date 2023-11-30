import pandas as pd
import numpy as np


class DataAugment:
    def __init__(self):
        pass
    
    def inner_join_dataframes(self,df1, df1_column, df2, df2_column):
        # Convert the join columns to the same data type (string)
        df1[df1_column] = df1[df1_column].astype(int)
        df2[df2_column] = df2[df2_column].astype(int)

        # Perform an inner join using the columns specified
        merged_df = pd.merge(df1, df2, how='inner', left_on=df1_column, right_on=df2_column)

        return merged_df
    def filter_df_by_dict_keys(self,data_dict, df):
        """
        Filters a DataFrame based on the keys of a provided dictionary.

        Parameters:
        - data_dict: The dictionary whose keys will be used for filtering.
        - df: The DataFrame to be filtered.

        Returns:
        - A DataFrame containing only the rows where 'Node' matches the keys of the dictionary.
        """
        # Get the list of keys from the dictionary
        dict_keys = list(data_dict.keys())
        
        # Filter the DataFrame based on whether 'Node' is in dict_keys
        filtered_df = df[df['Node'].isin(dict_keys)]
        
        return filtered_df
    
    def filter_dict_by_df_column(self,df,dict,col_name='Node'):
        interested_nodes=df[col_name]
        interested_nodes=np.array(interested_nodes).astype(int)
        # Create a new dictionary with only the keys of interest
        interested_temp_dict={key: dict[key] for key in interested_nodes if key in dict}
        return interested_temp_dict


    
    def df_to_dict(self,df, node_column):
        """
        Converts a DataFrame into a dictionary where the key is the node and the value is a list
        of temperature values, excluding initial consecutive 245.0 values.

        Parameters:
        - df: The DataFrame to convert.
        - node_column: The name of the node column.

        Returns:
        - A dictionary with nodes as keys and lists of temperature values as values.
        """
        node_dict = {}
        for _, row in df.iterrows():
            # Filter out the leading 245.0 values
            temps = row[row != 245.0].tolist()
            # If the list is not empty, remove the node value from the list
            if temps and temps[0] == row[node_column]:
                temps.pop(0)
            # Add to dictionary
            node_dict[row[node_column]] = temps

        return node_dict
    
    def delete_keys_less_length(self,dict,length):
        keys_to_remove = [key for key, value in dict.items() if len(value) < length]

        # Removing the keys from the dictionary
        for key in keys_to_remove:
            del dict[key]
        return dict
    
    def truncate_dictionary(self,dict,length):
        truncated_dict={key: value[:length] for key, value in dict.items()}
        return truncated_dict
    
    def sparse_dict(self,original_dict,ratio):
        """
        Creates a new dictionary with only every fifth key from the original dictionary.

        Parameters:
        - original_dict: The original dictionary.

        Returns:
        - A new dictionary containing every fifth key and its corresponding value.
        """
        # Use dictionary comprehension to filter out every fifth key
        filtered_dict = {k: original_dict[k] for i, k in enumerate(original_dict) if i % ratio == 0}

        return filtered_dict
    
    def sparse_mesh_df(self,mesh,ratio):
        mesh_sparse=mesh.iloc[::ratio].reset_index(drop=True)
        return mesh_sparse

    

    def merge_clustered_data(self, node_dict, cluster_labels, mesh_data):
        """
        Merges the provided node dictionary and mesh data based on the cluster labels.

        Args:
        node_dict (dict): A dictionary where keys represent node identifiers.
        cluster_labels (list or array): Cluster labels corresponding to each node.
        mesh_data (DataFrame): DataFrame containing mesh data to be merged.

        Returns:
        DataFrame: A merged DataFrame with labels and mesh data.
        """
        # Convert the keys of the node dictionary to a DataFrame
        key_list = list(node_dict.keys())
        df_with_label = pd.DataFrame(key_list, columns=['Node'])
        
        # Add the cluster labels to the DataFrame
        df_with_label['Label'] = cluster_labels
        
        # Ensure the 'Node' column is of integer type
        df_with_label['Node'] = df_with_label['Node'].astype(int)
        
        # Merge the DataFrame with the mesh data
        merged_df = pd.merge(df_with_label, mesh_data, on="Node", how='inner')
        
        return merged_df
