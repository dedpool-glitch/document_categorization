import pandas as pd
import constants

def save_to_csv(filepath,confidence_array,raw_content):

    """
    This function takes in the filepath and the confidence array as input.

    Saves a dataframe saved to the filepath specified.
    
    """
    filename_with_extension = filepath.split("\\")[-1]
    filename = filename_with_extension.rsplit(".", 1)[0]
    columns=constants.output_df_columns    
    """output_df=pd.DataFrame([confidence_array,raw_content],columns=columns)
    output_df.to_csv(filename+".csv")"""
    if len(confidence_array) == len(raw_content):
        combined_data = [inner_list + [content] for inner_list, content in zip(confidence_array,raw_content)]
        combined_df = pd.DataFrame(combined_data, columns=columns)
    else:
        print("The lengths of the DataFrame column and the list of lists do not match.")
    combined_df.to_csv({filename}+".csv")
    return combined_df,filename