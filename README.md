# Cyclistic-Case-Study
This is a case study for Google Data Analysis Certification  In this case study I will using dataset from Cyclistic, a fictional bike-share company to give insights to make data-driven decision making. 
## About the Company🏢
Cyclistic was launched in 2016, it is program offers bike-share service in Chicago. The program has 5,824 bicycles and 692 stations. Cyclistc offers customer single-ride passes, full-day passes, and annual memberships. Single-ride pass and full-day passes are considered casual rider and annual membership are considered Cyclistic member.
## Key Stakeholders🧑‍🤝‍🧑
Lily Moreno: The director of marketing, responsible for the development of campaigns and initiatives to promote the bike-share program.
Cyclistic marketing analytics team: A team of data analysts who are responsible for collecting, analyzing, and reporting data that help guide Cyclistic marketing strategy
Cyclistic executive team: The notoriously detail-oriented executive team wil decide 
whether to approve the recommended marketing program.  
## Goal
Design marketing strategies aimed at converting casual riders into annual members.
## Ask❓
To achieve the goal the following questions, need to be answered. 
1. How do annual members and casual riders use Cyclistic bikes differently? 
2. Why would casual riders buy Cyclistic annual memberships? 
3. How can Cyclistic use digital media to influence casual riders to become members?

Moreno has assigned me the first question to answer: How do annual members and casual riders use Cyclistic bikes differently?

## Prepare🖥️
Data Context
The data is provided by Cyclistc, it contains the time and geographic information of each ride in every month. In this case study I will use the last dataset from April 2024 to March 2025.

## Process🔨
Tools 
•	Excel – Used for initial data cleaning
•	Visual studio – Used for execute Python code
•	Python (Pandas) – Performed advanced data cleaning and transformation
•	Microsoft SQL Server Management Studio – Writing SQL queries to extract and analyze data

Excel
Download and open csv file with Excel. Create a column called ride_length. Calculate the length of each ride by subtracting the column started_at from the column ended_at and format as HH:MM:SS.
Create a column called day_of_week and calculate the day of the week that each ride started using the WEEKDAY command.
![image](https://github.com/user-attachments/assets/5c5e4ddf-81d8-4dbc-a012-2606ccd4632a)


Microsoft SQL Server Management Studio
Create database name cyclistic_database and table name BikeRides to store the data. 

Visual Studio and Python (Pandas)

Download packages in termial 
```
pip install pandas
pip install glob
pip install sqlalchemy 
```

Clean and Load data into Microsoft SQL Server Management
## Analyze🔍
Average ride time by rider type

 ![image](https://github.com/user-attachments/assets/8d965d55-bc5f-4d76-b01a-42693cf119f5)

Bike type by member and bike

 ![image](https://github.com/user-attachments/assets/95eac2bf-36b1-4724-839a-9790fd5fb040)

The day of the week with total count by the ride type

 ![image](https://github.com/user-attachments/assets/a1f0a20c-4c25-459e-b8b2-3b98c377ee6d)

The month of the year with total count by the member type

 ![image](https://github.com/user-attachments/assets/7463e51b-8e46-4998-af46-e9cb2f7ee724)

Count most used station by casual rider

 ![image](https://github.com/user-attachments/assets/0f171abd-7d3e-4282-8977-00e715fb26a1)
## Share📈
![image](https://github.com/user-attachments/assets/362a7b52-9ed1-4d41-b3d4-58240f904d54)
![image](https://github.com/user-attachments/assets/7dada62c-64af-4519-b1fb-a3d76e82fe91)
![image](https://github.com/user-attachments/assets/3dfcd1b8-c891-4d36-99d6-2af8bc3ab2d3)
![image](https://github.com/user-attachments/assets/688bee55-e283-4789-8d12-4c7c8c5fea8a)
![image](https://github.com/user-attachments/assets/96aa06da-51a6-46d1-9ac6-7ce49893c037)

## Act📜
Findings
1.	Annual members usually ride during weekdays; casual members prefer to ride during weekends.
2.	Casual members have longer average ride time.
3.	Electric scooters have the least ride trip.
4.	During the summer season there will be more rides. 
5.	Streeter Dr & Grand Ave, DuSable Lake Shor Dr & Monroe St are the most popular station.

Recommendations
1.	Promo a seasonal pass for casual riders that only ride during summer season
2.	Place more advertisements at Streeter Dr & Grand Ave, DuSable Lake Shor Dr & Monroe St stations
3.	Point reward system based on ride length.

