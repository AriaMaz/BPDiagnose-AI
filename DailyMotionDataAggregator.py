import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# File paths configuration (remember to change when running code)
score_location = "C:/Users/20amd23/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/scores.csv"
control_location = "C:/Users/20amd23/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/control/control_"
condition_location = "C:/Users/20amd23/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/condition/condition_"
output_file_saving_location = "C:/Users/20amd23/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/"

def daily_data_generator(file_location, file_index, score_file):
    """
    Generate daily motor activity readings from a given dataset.
    
    Parameters:
        file_location (str): The base path for the data files.
        file_index (int): The index number of the specific data file.
        score_file (DataFrame): DataFrame containing associated scores.
        
    Returns:
        DataFrame: A DataFrame containing processed motor activity data.
    """
    # Load the data file and convert timestamps from string to datetime
    test_file = pd.read_csv(file_location + str(file_index) + ".csv")
    test_file["timestamp"] = pd.to_datetime(test_file["timestamp"])

    # Normalize the activity data
    test_file["activity"] = test_file["activity"] * 1000 / test_file["activity"].max()

    # Find timestamps that indicate the start of a new day (00:00)
    day_start_indices = test_file[(test_file["timestamp"].dt.hour == 0) & 
                                  (test_file["timestamp"].dt.minute == 0)].index

    # Process and collect daily activity data
    daily_activity = pd.DataFrame()
    for i in range(1, len(day_start_indices) - 1):
        start = day_start_indices[i]
        end = day_start_indices[i + 1] - 1
        daily_activity[i] = test_file["activity"].loc[start:end].to_numpy()

    # Transpose and label the DataFrame for clarity
    daily_activity = daily_activity.transpose()
    daily_activity.columns = np.arange(daily_activity.shape[1])

    # Add additional attributes from the scores.csv file
    participant_type = "condition" if "condition" in file_location else "control"
    temp_row_index = score_file.index[score_file["number"] == participant_type + "_" + str(file_index)]
    temp_row = score_file.iloc[temp_row_index]
    for attribute in ["age", "gender", "mental_disorder", "melanch", 
                      "inpatient", "edu", "marriage", "madrs1", "madrs2"]:
        daily_activity[attribute] = np.repeat(temp_row.iloc[0][attribute], daily_activity.shape[0])

    return daily_activity

# Main execution block
if __name__ == "__main__":
    # Load the score file
    scores_df = pd.read_csv(score_location)

    # Generate and combine motor activity data for all conditions and controls
    combined_activity = pd.DataFrame()
    condition_numbers = np.arange(2, 24)
    control_numbers = np.arange(1, 33)

    for index in condition_numbers:
        combined_activity = pd.concat([combined_activity, 
                                       daily_data_generator(condition_location, index, scores_df)], 
                                       axis=0)

    for index in control_numbers:
        combined_activity = pd.concat([combined_activity, 
                                       daily_data_generator(control_location, index, scores_df)], 
                                       axis=0)

    # Shuffle, reset the index, and save the combined data
    combined_activity = combined_activity.sample(frac=1).reset_index(drop=True)
    combined_activity.to_csv(output_file_saving_location + "DailyMotorActivityReadings.csv")
