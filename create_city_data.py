import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('CIty,Area,Road names.csv')

# Rename columns to match our expected format
df.columns = ['City', 'Area', 'Road names']

# Create a nested dictionary structure
city_data = {}

# Group by city and area, then create the nested structure
for city in df['City'].unique():
    city_data[city] = {}
    city_df = df[df['City'] == city]
    for area in city_df['Area'].unique():
        area_df = city_df[city_df['Area'] == area]
        city_data[city][area] = area_df['Road names'].tolist()

# Save to JSON file
with open('city_data.json', 'w') as f:
    json.dump(city_data, f, indent=4)

print("City data JSON file has been created successfully!") 