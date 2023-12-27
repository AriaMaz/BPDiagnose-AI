import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#When running the code, remember to change the following locations, becareful with "/" 
score_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/scores.csv"
control_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/control/"+"control_"
condition_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/data/condition/"+"condition_"
output_file_saving_location = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/"

def daily_data_generator_condition(j):
    #Load file and convert the timestamp from string to date
    test_file = pd.read_csv(condition_location+str(j)+".csv")
    score_file = pd.read_csv(score_location)
    test_file["timestamp"] = pd.to_datetime(test_file["timestamp"])
    #Normalize the activity data
    test_file["activity"] = test_file["activity"]*1000/test_file["activity"].max()

    #Find all the timestamps at 0:00
    test_file["hour"] = test_file["timestamp"].dt.hour
    test_file["minute"] = test_file["timestamp"].dt.minute
    day_splitter = test_file[(test_file["hour"]==0) & (test_file["minute"]==0)].index

    #Split the data by day. Here we only take days with data from 0:00-23:59. So we discard the first and last day
    extract_first_day = test_file["activity"].loc[day_splitter[0]:day_splitter[1]-1]
    DailyMotorActivityReadings_j = pd.DataFrame()
    DailyMotorActivityReadings_j[0] = extract_first_day
    DailyMotorActivityReadings_j.reset_index()

    for i in range(2, len(day_splitter)-2):
        start = day_splitter[i]
        end = day_splitter[i+1]
        extract_day_activity = test_file["activity"].loc[start:end-1]
        #extract_day_time = temp[0]
        DailyMotorActivityReadings_j[i-1] = extract_day_activity.to_numpy()
        
    DailyMotorActivityReadings_j.reset_index()
    DailyMotorActivityReadings_j = DailyMotorActivityReadings_j.transpose()
    DailyMotorActivityReadings_j.columns = np.arange(0,  DailyMotorActivityReadings_j.shape[1], 1)

    #Add time 
    temp = test_file["timestamp"].iloc[day_splitter]
    DailyMotorActivityReadings_j["Time"] = temp.dt.date.iloc[1:-2].to_list()
    first_column = DailyMotorActivityReadings_j.pop('Time')
    DailyMotorActivityReadings_j.insert(0, "Time", first_column)

    #Add other attributes from scores.csv into the daily acitivity dataframe 
    temp_row_index = score_file.index[score_file["number"] == "condition_"+str(j)]
    temp_row = score_file.iloc[temp_row_index]
    DailyMotorActivityReadings_j["age"] = np.repeat(temp_row.iloc[0, 3], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["gender"] = np.repeat(temp_row.iloc[0, 4], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["mental_disorder"] = np.repeat(temp_row.iloc[0, 5], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["melanch"] = np.repeat(temp_row.iloc[0, 6], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["inpatient"] = np.repeat(temp_row.iloc[0, 7], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["edu"] = np.repeat(temp_row.iloc[0, 8], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["marriage"] = np.repeat(temp_row.iloc[0, 9], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["madrs1"] = np.repeat(temp_row.iloc[0, 10], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["madrs2"] = np.repeat(temp_row.iloc[0, 11], DailyMotorActivityReadings_j.shape[0])

    return DailyMotorActivityReadings_j

#This function is almost exactly the same as the one above, simply change condition into control
def daily_data_generator_control(j):
    #load file and convert the timestamp from string to date
    test_file = pd.read_csv(control_location+str(j)+".csv")
    score_file = pd.read_csv(score_location)
    test_file["timestamp"] = pd.to_datetime(test_file["timestamp"])
    #normalize the activity data
    test_file["activity"] = test_file["activity"]*1000/test_file["activity"].max()

    #Find all the timestamps at 0:00
    test_file["hour"] = test_file["timestamp"].dt.hour
    test_file["minute"] = test_file["timestamp"].dt.minute
    day_splitter = test_file[(test_file["hour"]==0) & (test_file["minute"]==0)].index

    #Split the data by day. Here we only take days with data from 0:00-23:59. So we discard the first and last day
    extract_first_day = test_file["activity"].loc[day_splitter[0]:day_splitter[1]-1]
    DailyMotorActivityReadings_j = pd.DataFrame()
    DailyMotorActivityReadings_j[0] = extract_first_day
    DailyMotorActivityReadings_j.reset_index()

    for i in range(2, len(day_splitter)-2):
        start = day_splitter[i]
        end = day_splitter[i+1]
        extract_day_activity = test_file["activity"].loc[start:end-1]
        #extract_day_time = temp[0]
        DailyMotorActivityReadings_j[i-1] = extract_day_activity.to_numpy()
     
    DailyMotorActivityReadings_j.reset_index()
    DailyMotorActivityReadings_j = DailyMotorActivityReadings_j.transpose()
    DailyMotorActivityReadings_j.columns = np.arange(0,  DailyMotorActivityReadings_j.shape[1], 1)
    #Add time 
    temp = test_file["timestamp"].iloc[day_splitter]
    DailyMotorActivityReadings_j["Time"] = temp.dt.date.iloc[1:-2].to_list()
    first_column = DailyMotorActivityReadings_j.pop('Time')
    DailyMotorActivityReadings_j.insert(0, "Time", first_column)

    #Add other attributes from scores.csv into the daily acitivity dataframe 
    temp_row_index = score_file.index[score_file["number"] == "control_"+str(j)]
    temp_row = score_file.iloc[temp_row_index]
    DailyMotorActivityReadings_j["age"] = np.repeat(temp_row.iloc[0, 3], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["gender"] = np.repeat(temp_row.iloc[0, 4], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["mental_disorder"] = np.repeat(temp_row.iloc[0, 5], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["melanch"] = np.repeat(temp_row.iloc[0, 6], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["inpatient"] = np.repeat(temp_row.iloc[0, 7], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["edu"] = np.repeat(temp_row.iloc[0, 8], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["marriage"] = np.repeat(temp_row.iloc[0, 9], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["madrs1"] = np.repeat(temp_row.iloc[0, 10], DailyMotorActivityReadings_j.shape[0])
    DailyMotorActivityReadings_j["madrs2"] = np.repeat(temp_row.iloc[0, 11], DailyMotorActivityReadings_j.shape[0])

    return DailyMotorActivityReadings_j



#Iterate over all the files, and combine
DailyMotorActivityReadings = daily_data_generator_condition(5)
control_number = np.arange(1, 32+1, 1)
condition_number = np.arange(2, 23+1, 1)
for k in condition_number:
    DailyMotorActivityReadings = pd.concat([DailyMotorActivityReadings, daily_data_generator_condition(k)], axis = 0)

for h in control_number:
    DailyMotorActivityReadings = pd.concat([DailyMotorActivityReadings, daily_data_generator_control(k)], axis = 0)


#Shuffle all the rows, reset index, and save
DailyMotorActivityReadings = DailyMotorActivityReadings.sample(frac = 1)
DailyMotorActivityReadings = DailyMotorActivityReadings.set_index(np.arange(0, DailyMotorActivityReadings.shape[0], 1))
DailyMotorActivityReadings.to_csv(output_file_saving_location+"DailyMotorActivityReadings.csv") #the name of output file is DailyMotorActivityReadings
