import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
import calendar


# Set style
sns.set_style("whitegrid")  
plt.style.use('default')    
sns.set_palette("colorblind")
plt.rcParams['figure.facecolor'] = 'white'


# Connection parameters
server = 'servername' 
database = 'cyclistic_database'


engine = create_engine(
    f"mssql+pyodbc://{server}/{database}?"
    "driver=ODBC+Driver+17+for+SQL+Server&"
    "trusted_connection=yes"
)

## 1. Original Ride Length Visualization
def plot_ride_length():
    query = """
    SELECT 
        member_casual, 
        CONVERT(TIME, DATEADD(SECOND, AVG(CAST(DATEDIFF(SECOND, '00:00:00', ride_length) AS BIGINT)), '00:00:00')) AS avg_ride_length
    FROM BikeRides
    GROUP BY member_casual;
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    
    # Convert time string to total minutes - UPDATED METHOD
    def time_to_minutes(time_obj):
        if isinstance(time_obj, str):
            # Handle string format if needed
            hours, minutes, seconds = map(int, time_obj.split(':'))
        else:
            # Handle time object
            hours = time_obj.hour
            minutes = time_obj.minute
            seconds = time_obj.second
        return hours * 60 + minutes + seconds / 60
    
    df['avg_minutes'] = df['avg_ride_length'].apply(time_to_minutes)
    
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(data=df, x='member_casual', y='avg_minutes')
    
    plt.title('Average Ride Duration by Rider Type', fontsize=14)
    plt.xlabel('Rider Type', fontsize=12)
    plt.ylabel('Average Duration (minutes)', fontsize=12)
    
    # Add time labels in HH:MM format
    for i, row in df.iterrows():
        if isinstance(row['avg_ride_length'], str):
            time_str = row['avg_ride_length'][:7]  # Format as HH:MM:SS
        else:
            time_str = row['avg_ride_length'].strftime('%H:%M:%S')[:7]
        ax.text(i, row['avg_minutes'] + 0.5, time_str, 
                ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('ride_length.png', dpi=300, bbox_inches='tight')
    plt.show()

## 2. Bike Type by Member/Casual Visualization
def plot_bike_type_usage():
    query = """
    SELECT 
        member_casual,
        rideable_type,
        COUNT(*) AS trip_count
    FROM BikeRides
    GROUP BY member_casual, rideable_type
    ORDER BY member_casual, rideable_type;
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='rideable_type', y='trip_count', hue='member_casual')
    
    plt.title('Bike Type Usage by Rider Category', fontsize=14)
    plt.xlabel('Bike Type', fontsize=12)
    plt.ylabel('Number of Trips (log scale)', fontsize=12)
    plt.yscale('log')  # Log scale for better visualization of large counts
    plt.xticks(rotation=45)
    
    # Add value labels
    for p in ax.patches:
        ax.annotate(f"{p.get_height():,.0f}", 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', xytext=(0, 5), textcoords='offset points',
                   fontsize=10)
    
    plt.legend(title='Rider Type')
    plt.tight_layout()
    plt.savefig('bike_type_usage.png', dpi=300, bbox_inches='tight')
    plt.show()

## 3. Day of Week Visualization
def plot_weekly_patterns():
    query = """
    SELECT 
        day_of_week,
        SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) AS member_rides,
        SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) AS casual_rides,
        COUNT(*) AS total_rides
    FROM BikeRides
    GROUP BY day_of_week
    ORDER BY day_of_week;
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    
    # Convert day numbers to names and reorder
    df['day_name'] = df['day_of_week'].apply(lambda x: calendar.day_name[x-1])
    day_order = list(calendar.day_name)
    df['day_name'] = pd.Categorical(df['day_name'], categories=day_order, ordered=True)
    df = df.sort_values('day_name')
    
    plt.figure(figsize=(12, 6))
    
    # Calculate percentages for stacked area plot
    df['member_pct'] = df['member_rides'] / df['total_rides'] * 100
    df['casual_pct'] = df['casual_rides'] / df['total_rides'] * 100
    
    plt.stackplot(df['day_name'], 
                 [df['member_pct'], df['casual_pct']],
                 labels=['Members', 'Casual Riders'],
                 colors=['#1f77b4', '#ff7f0e'],
                 alpha=0.7)
    
    plt.title('Weekly Riding Patterns by Rider Type', fontsize=14)
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Percentage of Rides', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('weekly_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()

## 4. Monthly Patterns Visualization
def plot_monthly_trends():
    query = """
    SELECT
        YEAR(started_at) AS ride_year,
        MONTH(started_at) AS ride_month,
        DATENAME(month, started_at) AS month_name, 
        SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) AS member_rides,
        SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) AS casual_rides,
        COUNT(*) AS total_rides
    FROM BikeRides
    GROUP BY YEAR(started_at), MONTH(started_at), DATENAME(month, started_at)
    ORDER BY ride_year, ride_month;
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    
    # Create year-month label and proper datetime for ordering
    df['date'] = pd.to_datetime(df['ride_year'].astype(str) + '-' + df['ride_month'].astype(str))
    df = df.sort_values('date')
    df['period'] = df['month_name'] + ' ' + df['ride_year'].astype(str)
    
    plt.figure(figsize=(14, 6))
    
    # Plot with markers for data points
    plt.plot(df['period'], df['member_rides'], 
             marker='o', label='Members', linewidth=2.5)
    plt.plot(df['period'], df['casual_rides'], 
             marker='o', label='Casual Riders', linewidth=2.5)
    
    plt.title('Monthly Riding Trends', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Rides', fontsize=12)
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    
    # Add data labels for max points
    max_member = df.loc[df['member_rides'].idxmax()]
    max_casual = df.loc[df['casual_rides'].idxmax()]
    plt.annotate(f"Max: {max_member['member_rides']:,}",
                 xy=(max_member['period'], max_member['member_rides']),
                 xytext=(0, 10), textcoords='offset points',
                 ha='center', va='bottom')
    plt.annotate(f"Max: {max_casual['casual_rides']:,}",
                 xy=(max_casual['period'], max_casual['casual_rides']),
                 xytext=(0, 10), textcoords='offset points',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('monthly_trends.png', dpi=300, bbox_inches='tight')
    plt.show()

## 5. Top Stations for Casual Riders
def plot_top_stations():
    # Start stations query
    start_query = """
    SELECT TOP 10
        COUNT(start_station_name) AS total_trip,
        start_station_name
    FROM BikeRides
    WHERE member_casual = 'casual'
    GROUP BY start_station_name
    ORDER BY total_trip DESC;
    """
    
    # End stations query
    end_query = """
    SELECT TOP 10
        COUNT(end_station_name) AS total_trip,
        end_station_name
    FROM BikeRides
    WHERE member_casual = 'casual'
    GROUP BY end_station_name
    ORDER BY total_trip DESC;
    """
    
    with engine.connect() as conn:
        start_df = pd.read_sql(text(start_query), conn)
        end_df = pd.read_sql(text(end_query), conn)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Start stations plot
    sns.barplot(data=start_df, y='start_station_name', x='total_trip', 
                ax=ax1, palette='Blues_r', saturation=0.8)
    ax1.set_title('Top 10 Start Stations for Casual Riders', fontsize=14)
    ax1.set_xlabel('Number of Trips', fontsize=12)
    ax1.set_ylabel('Station Name', fontsize=12)
    
    # Add value labels
    for p in ax1.patches:
        width = p.get_width()
        ax1.text(width + 0.02*width, p.get_y() + p.get_height()/2,
                f'{int(width):,}', va='center', fontsize=10)
    
    # End stations plot
    sns.barplot(data=end_df, y='end_station_name', x='total_trip', 
                ax=ax2, palette='Greens_r', saturation=0.8)
    ax2.set_title('Top 10 End Stations for Casual Riders', fontsize=14)
    ax2.set_xlabel('Number of Trips', fontsize=12)
    ax2.set_ylabel('')
    
    # Add value labels
    for p in ax2.patches:
        width = p.get_width()
        ax2.text(width + 0.02*width, p.get_y() + p.get_height()/2,
                f'{int(width):,}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('top_stations.png', dpi=300, bbox_inches='tight')
    plt.show()

# Generate all visualizations
if __name__ == "__main__":
    plot_ride_length()
    plot_bike_type_usage()
    plot_weekly_patterns()
    plot_monthly_trends()
    plot_top_stations()
