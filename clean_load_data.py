import pandas as pd
import glob 
from sqlalchemy import create_engine

# Connection parameters
server = 'servername' 
database = 'cyclistic_database'

engine = create_engine(
    f"mssql+pyodbc://{server}/{database}?"
    "driver=ODBC+Driver+17+for+SQL+Server&"
    "trusted_connection=yes"
)

#get data from different csv files
folder_path = 'processed_data'
file_list = glob.glob(folder_path + "/*.csv") 

main_df = pd.read_csv(file_list[0]) 

for i in range(1,len(file_list)): 
    data = pd.read_csv(file_list[i]) 
    df = pd.DataFrame(data) 
    print(f"current dataframe has {df.shape[0]} rows")

    main_df = pd.concat([main_df, df], ignore_index=True)
    print(f"main dataframe has {main_df.shape[0]} rows")
    print("---------------------------------------------------")

#drop duplicate 
main_df = main_df.drop_duplicates()
print(f"dropped duplicate, main dataframe has {main_df.shape[0]} rows")

# print number of null values
print("Number of null values before removing:")
print(main_df.isnull().sum().sum())

# remove null values
main_df = main_df.dropna()

# Print number of null values after removing
print("Number of null values after removing:")
print(main_df.isnull().sum().sum())

#remove rows 
main_df = main_df[main_df['ride_length'].astype(str).str.match(r'^([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d)$')]
print(f"drop ride_length in wrong format, main dataframe has {main_df.shape[0]} rows")

#reformat datetime
main_df['started_at'] = pd.to_datetime(main_df['started_at'])
main_df['ended_at'] = pd.to_datetime(main_df['ended_at'])
main_df['ride_length'] = pd.to_datetime(main_df['ride_length'], format='%H:%M:%S').dt.time

#load data to SQL sever
main_df.to_sql("BikeRides", engine, index=False, if_exists='append')
print("data loaded to database")
print("---------------------------------------------------")
    





