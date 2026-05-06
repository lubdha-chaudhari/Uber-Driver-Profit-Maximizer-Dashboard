"""
Feature Engineering Module for Uber Driver Profit Maximizer Dashboard

This module handles:
- Simulated fare calculation
- Demand metrics (hourly, location-based)
- Trip statistics and idle time estimation
- Feature aggregation for different time periods and locations
"""

import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fare Model Constants (in INR)
BASE_FARE = 50
COST_PER_KM = 10
COST_PER_MINUTE = 2


def calculate_simulated_fare(distance, duration_minutes):
    """
    Calculate simulated fare based on distance and duration.
    
    Fare Model:
    fare = base_fare + (distance * cost_per_km) + (duration * cost_per_minute)
    
    Args:
        distance (float): Trip distance in miles
        duration_minutes (float): Trip duration in minutes
        
    Returns:
        float: Calculated fare
    """
    # Convert miles to kilometers (1 mile = 1.60934 km)
    distance_km = distance * 1.60934
    
    fare = BASE_FARE + (distance_km * COST_PER_KM) + (duration_minutes * COST_PER_MINUTE)
    return max(fare, BASE_FARE)  # Ensure fare is at least base fare


def calculate_driver_earnings(distance, duration_minutes, surge_multiplier=1.0):
    """
    Calculate driver earnings with surge pricing.
    
    Drivers typically receive 75% of the fare minus platform fees.
    
    Args:
        distance (float): Trip distance in miles
        duration_minutes (float): Trip duration in minutes
        surge_multiplier (float): Surge pricing multiplier (1.0 = no surge)
        
    Returns:
        float: Driver earnings for this trip
    """
    base_fare = calculate_simulated_fare(distance, duration_minutes)
    fare_with_surge = base_fare * surge_multiplier
    
    # Driver receives 75% of fare
    driver_commission = fare_with_surge * 0.75
    return driver_commission


def add_simulated_fares(df):
    """
    Add simulated fare and earnings columns to dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe with MILES and trip_duration_minutes
        
    Returns:
        pd.DataFrame: DataFrame with added fare columns
    """
    df = df.copy()
    
    df['simulated_fare'] = df.apply(
        lambda row: calculate_simulated_fare(row['MILES'], row['trip_duration_minutes']),
        axis=1
    )
    
    df['driver_earnings'] = df.apply(
        lambda row: calculate_driver_earnings(row['MILES'], row['trip_duration_minutes']),
        axis=1
    )
    
    logger.info("Simulated fares and earnings calculated")
    return df


def calculate_demand_metrics(df):
    """
    Calculate demand metrics per hour and per location.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        dict: Dictionary containing demand metrics
    """
    metrics = {}
    
    # Demand by hour
    hourly_demand = df.groupby('pickup_hour').agg({
        'MILES': 'count',  # Number of trips
        'trip_duration_minutes': 'mean',
        'simulated_fare': 'mean',
        'driver_earnings': ['sum', 'mean']
    }).round(2)
    
    hourly_demand.columns = ['trips_count', 'avg_duration', 'avg_fare', 'total_earnings', 'avg_earnings_per_trip']
    metrics['hourly_demand'] = hourly_demand
    
    # Demand by location
    location_demand = df.groupby('START').agg({
        'MILES': ['count', 'mean'],
        'trip_duration_minutes': 'mean',
        'simulated_fare': 'mean',
        'driver_earnings': ['sum', 'mean']
    }).round(2)
    
    location_demand.columns = ['trips_count', 'avg_distance', 'avg_duration', 'avg_fare', 'total_earnings', 'avg_earnings']
    location_demand = location_demand.sort_values('total_earnings', ascending=False)
    metrics['location_demand'] = location_demand
    
    # Demand by time period
    period_demand = df.groupby('time_period').agg({
        'MILES': 'count',
        'trip_duration_minutes': 'mean',
        'driver_earnings': ['sum', 'mean']
    }).round(2)
    
    period_demand.columns = ['trips_count', 'avg_duration', 'total_earnings', 'avg_earnings']
    metrics['period_demand'] = period_demand
    
    # Demand by day of week
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['day_name'] = df['pickup_day_of_week'].map(day_names)
    
    daily_demand = df.groupby('day_name').agg({
        'MILES': 'count',
        'trip_duration_minutes': 'mean',
        'driver_earnings': ['sum', 'mean']
    }).round(2)
    
    daily_demand.columns = ['trips_count', 'avg_duration', 'total_earnings', 'avg_earnings']
    daily_demand = daily_demand.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                          'Friday', 'Saturday', 'Sunday'])
    metrics['daily_demand'] = daily_demand
    
    logger.info("Demand metrics calculated successfully")
    return metrics


def estimate_idle_time(df):
    """
    Estimate idle time between trips for each location.
    
    Idle time = gap between end of one trip and start of next trip.
    This is a rough estimate based on average gaps in the data.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        pd.DataFrame: DataFrame with idle time estimates by location
    """
    df = df.copy()
    df = df.sort_values('END_DATE')
    
    # Calculate time gap to next trip
    df['next_start'] = df['START_DATE'].shift(-1)
    df['time_to_next_trip'] = (df['next_start'] - df['END_DATE']).dt.total_seconds() / 60
    
    # Filter for same location transitions (realistic idle time)
    same_location_transitions = df[df['STOP'] == df['START'].shift(-1)]
    
    idle_estimates = {}
    
    if len(same_location_transitions) > 0:
        idle_by_location = same_location_transitions.groupby('STOP')['time_to_next_trip'].agg([
            'mean', 'median', 'min', 'max'
        ]).round(2)
        idle_by_location.columns = ['avg_idle_minutes', 'median_idle_minutes', 'min_idle', 'max_idle']
        idle_estimates = idle_by_location.to_dict('index')
    
    # Default idle time if no data
    default_idle = {
        'avg_idle_minutes': 15,
        'median_idle_minutes': 10,
        'min_idle': 0,
        'max_idle': 60
    }
    
    logger.info(f"Idle time estimates calculated for {len(idle_estimates)} locations")
    return idle_estimates, default_idle


def calculate_location_features(df):
    """
    Calculate comprehensive features for each location.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        pd.DataFrame: DataFrame with location-level features
    """
    location_features = df.groupby('START').agg({
        'MILES': ['count', 'mean', 'sum'],
        'trip_duration_minutes': ['mean', 'sum'],
        'driver_earnings': ['mean', 'sum', 'std'],
        'pickup_hour': lambda x: x.mode()[0] if len(x.mode()) > 0 else 9,
        'is_weekend': 'mean'
    }).round(2)
    
    location_features.columns = [
        'total_trips', 'avg_distance', 'total_distance',
        'avg_trip_duration', 'total_trip_time',
        'avg_earnings_per_trip', 'total_earnings', 'earnings_std',
        'peak_hour', 'weekend_ratio'
    ]
    
    # Calculate earnings per hour (assuming 1 hour + idle time)
    location_features['earnings_per_hour'] = (
        location_features['avg_earnings_per_trip'] / 
        (location_features['avg_trip_duration'] + 15) * 60
    ).round(2)
    
    location_features = location_features.sort_values('total_earnings', ascending=False)
    
    logger.info(f"Location features calculated for {len(location_features)} locations")
    return location_features


def calculate_hour_location_matrix(df):
    """
    Create a pivot table of earnings by hour and location.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        pd.DataFrame: Pivot table with hours as rows and locations as columns
    """
    matrix = df.pivot_table(
        values='driver_earnings',
        index='pickup_hour',
        columns='START',
        aggfunc='mean'
    ).round(2)
    
    logger.info("Hour-Location matrix created successfully")
    return matrix


def engineer_features(df):
    """
    Complete feature engineering pipeline.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        dict: Dictionary containing engineered features and datasets
    """
    logger.info("=" * 50)
    logger.info("Starting feature engineering pipeline...")
    logger.info("=" * 50)
    
    # Add simulated fares
    df = add_simulated_fares(df)
    
    # Calculate demand metrics
    demand_metrics = calculate_demand_metrics(df)
    
    # Estimate idle time
    idle_estimates, default_idle = estimate_idle_time(df)
    
    # Calculate location features
    location_features = calculate_location_features(df)
    
    # Calculate hour-location matrix
    hour_location_matrix = calculate_hour_location_matrix(df)
    
    features = {
        'dataframe': df,
        'demand_metrics': demand_metrics,
        'idle_estimates': idle_estimates,
        'default_idle': default_idle,
        'location_features': location_features,
        'hour_location_matrix': hour_location_matrix
    }
    
    logger.info("=" * 50)
    logger.info("Feature engineering complete!")
    logger.info("=" * 50)
    
    return features
