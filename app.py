from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import json

app = Flask(__name__)

# Load the trained model
model = joblib.load('cat.pkl',  mmap_mode='r')

# Load the city data
with open('city_data.json', 'r') as f:
    city_data = json.load(f)

# Weather conditions
weather_conditions = [
    'Clear', 'Rainy', 'Foggy', 'Storm', 'Hazy', 'Overcast', 
    'Rain', 'Stormy', 'Thunderstorms', 'Windy'
]

def get_traffic_multiplier(day_type, time, special_event, weather, roadwork):
    """Calculate traffic multiplier based on intuitive inputs"""
    multiplier = 1.0
    
    # Time of day multiplier
    time_multipliers = {
        '6': 0.7,   # Early morning
        '9': 1.5,   # Morning rush
        '12': 1.2,  # Midday
        '15': 1.3,  # Afternoon
        '18': 1.8,  # Evening rush
        '21': 0.8   # Night
    }
    multiplier *= time_multipliers.get(time, 1.0)
    
    # Day type multiplier
    day_multipliers = {
        'weekday': 1.5,
        'weekend': 0.8,
        'holiday': 0.6
    }
    multiplier *= day_multipliers.get(day_type, 1.0)
    
    # Special event multiplier
    event_multipliers = {
        'none': 1.0,
        'festival': 2.0,
        'sports': 2.5,
        'protest': 2.0
    }
    multiplier *= event_multipliers.get(special_event, 1.0)
    
    # Weather multiplier
    weather_multipliers = {
        'Clear': 1.0,
        'Rainy': 1.5,
        'Foggy': 1.3,
        'Storm': 1.8,
        'Hazy': 1.2,
        'Overcast': 1.1,
        'Rain': 1.5,
        'Stormy': 1.8,
        'Thunderstorms': 2.0,
        'Windy': 1.2
    }
    multiplier *= weather_multipliers.get(weather, 1.0)
    
    # Roadwork multiplier
    if roadwork == 'Yes':
        multiplier *= 1.5
    
    return multiplier

def preprocess_input(input_data):
    # Convert date string to datetime
    date = datetime.strptime(input_data['date'], '%Y-%m-%d')
    
    # Calculate traffic multiplier based on intuitive inputs
    traffic_multiplier = get_traffic_multiplier(
        input_data['day_type'],
        input_data['time'],
        input_data['special_event'],
        input_data['weather_conditions'],
        input_data['roadwork_construction']
    )
    
    # Base values for traffic metrics
    base_traffic_volume = 50
    base_average_speed = 40
    base_travel_time_index = 1.2
    base_capacity_utilization = 60
    
    # Adjust base values based on traffic multiplier
    traffic_volume = base_traffic_volume * traffic_multiplier
    average_speed = base_average_speed / traffic_multiplier  # Inverse relationship
    travel_time_index = base_travel_time_index * traffic_multiplier
    road_capacity_utilization = min(100, base_capacity_utilization * traffic_multiplier)
    
    # Create feature dictionary
    features = {
        'year': date.year,
        'month': date.month,
        'day': date.day,
        'hour': int(input_data['time']),
        'traffic_volume': float(traffic_volume),
        'average_speed': float(average_speed),
        'travel_time_index': float(travel_time_index),
        'road_capacity_utilization': float(road_capacity_utilization),
        'incident_reports': 1 if input_data['special_event'] != 'none' else 0,
        'environmental_impact': float(road_capacity_utilization * 0.8),  # Related to traffic volume
        'public_transport_usage': float(30 * traffic_multiplier),  # Increases with traffic
        'traffic_signal_compliance': float(85 / traffic_multiplier),  # Decreases with traffic
        'parking_usage': float(70 * traffic_multiplier),  # Increases with traffic
        'pedestrian_cyclist_count': int(100 * traffic_multiplier)  # Increases with traffic
    }
    
    # Add one-hot encoded weather conditions
    for condition in weather_conditions:
        features[f'weather_conditions_{condition}'] = 1 if input_data['weather_conditions'] == condition else 0
    
    # Add roadwork construction
    features['roadwork_construction_Yes'] = 1 if input_data['roadwork_construction'] == 'Yes' else 0
    
    # Add area and road name features
    for city, areas in city_data.items():
        for area, roads in areas.items():
            for road in roads:
                features[f'area_name_{area}'] = 1 if area == input_data['area'] else 0
                features[f'road_name_{road}'] = 1 if road == input_data['road'] else 0
    
    # Convert to DataFrame
    df = pd.DataFrame([features])
    
    # Ensure all required columns are present
    required_columns = model.feature_names_in_
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Reorder columns to match model's expected order
    df = df[required_columns]
    
    return df

@app.route('/')
def home():
    return render_template('index.html', city_data=city_data, weather_conditions=weather_conditions)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from request
        input_data = request.json
        
        # Preprocess input data
        processed_data = preprocess_input(input_data)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        
        # Adjust prediction based on traffic multiplier
        traffic_multiplier = get_traffic_multiplier(
            input_data['day_type'],
            input_data['time'],
            input_data['special_event'],
            input_data['weather_conditions'],
            input_data['roadwork_construction']
        )
        
        # Adjust prediction to be more sensitive to traffic conditions
        adjusted_prediction = min(100, prediction * traffic_multiplier)
        
        # Determine congestion level category with adjusted thresholds
        if adjusted_prediction <= 20:
            category = "Low"
        elif adjusted_prediction <= 50:
            category = "Moderate"
        else:
            category = "High"
        
        return jsonify({
            'success': True,
            'prediction': float(adjusted_prediction),
            'category': category
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 