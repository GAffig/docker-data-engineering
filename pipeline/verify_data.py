import pandas as pd

# Download and read the parquet file
url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet'
print("Downloading data...")
df = pd.read_parquet(url)

# Question 1: Count trips with trip_distance <= 1
count_le_1 = (df['trip_distance'] <= 1).sum()
print(f"\nTrips with distance <= 1 mile: {count_le_1}")

# Question 2: Find pickup day with longest trip distance (< 100 miles)
df_filtered = df[df['trip_distance'] < 100].copy()
df_filtered['pickup_date'] = pd.to_datetime(df_filtered['tpep_pickup_datetime']).dt.date

# Find the max distance for each day
max_distance_per_day = df_filtered.groupby('pickup_date')['trip_distance'].max()

# Find the day with the maximum distance
day_with_max_distance = max_distance_per_day.idxmax()
max_distance_value = max_distance_per_day.max()

print(f"\nPickup day with longest trip distance (< 100 miles): {day_with_max_distance}")
print(f"Trip distance: {max_distance_value} miles")

# Verify by finding the actual row
longest_trip = df_filtered[df_filtered['trip_distance'] == max_distance_value]
print(f"\nTrip details:")
print(longest_trip[['tpep_pickup_datetime', 'trip_distance']])