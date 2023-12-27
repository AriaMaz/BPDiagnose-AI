import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# File path configurations - Update these paths as necessary
score_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/scores.csv"
control_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/control/control_"
condition_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/condition/condition_"
output_file_saving_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/"

def daily_data_generator_condition(j):
    """
    Process and normalize activity data for a given condition.
    """
    # Load file and convert the timestamp from string to date
    test_file = pd.read_csv(condition_location + str(j) + ".csv")
    score_file = pd.read_csv(score_location)
    test_file["timestamp"] = pd.to_datetime(test_file["timestamp"])

    # Normalize the activity data
    test_file["activity"] = test_file["activity"] * 1000 / test_file["activity"].max()

    # Identify timestamps indicating the start of a new day (00:00)
    test_file["hour"] = test_file["timestamp"].dt.hour
    test_file["minute"] = test_file["timestamp"].dt.minute
    day_splitter = test_file[(test_file["hour"] == 0) & (test_file["minute"] == 0)].index

    # Split the data by day, discarding incomplete first and last days
    daily_motion_j = pd.DataFrame()
    for i in range(1, len(day_splitter) - 1):
        start = day_splitter[i]
        end = day_splitter[i + 1]
        daily_motion_j[i] = test_file["activity"].loc[start:end - 1].to_numpy()

    # Transpose and configure the DataFrame
    daily_motion_j = daily_motion_j.transpose()
    daily_motion_j.columns = np.arange(daily_motion_j.shape[1])

    # Add time and other attributes from scores.csv
    temp = test_file["timestamp"].iloc[day_splitter]
    daily_motion_j["Time"] = temp.dt.date.iloc[1:-1].to_list()
    daily_motion_j = daily_motion_j.set_index("Time")

    # Repeat this process for attributes like age, gender, etc.
    # ...

    return daily_motion_j

# Similar function for control data, replacing 'condition' with 'control'
def daily_data_generator_control(j):
    # Function body is similar to daily_data_generator_condition
    # ...

# Main execution block
if __name__ == "__main__":
    # Initialize DataFrame with data for a specific condition
    daily_motion = daily_data_generator_condition(5)

    # Define ranges for condition and control numbers
    control_number = np.arange(1, 33)
    condition_number = np.arange(2, 24)

    # Concatenate data for all conditions and controls
    for k in condition_number:
        daily_motion = pd.concat([daily_motion, daily_data_generator_condition(k)], axis=0)
    for h in control_number:
        daily_motion = pd.concat([daily_motion, daily_data_generator_control(h)], axis=0)

    # Shuffle, reset index, and save the combined DataFrame
    daily_motion = daily_motion.sample(frac=1).reset_index(drop=True)
    daily_motion.to_csv(output_file_saving_location + "daily_motion.csv")

