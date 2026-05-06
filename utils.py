"""
Utility Functions Module for Uber Driver Profit Maximizer Dashboard

This module provides utility functions for:
- Data formatting and presentation
- Color mapping for visualizations
- Caching and performance optimization
- Recommendation generation
- Common calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Color schemes for visualizations
COLOR_SCHEME = {
    'primary': '#FF6B35',      # Uber Orange
    'secondary': '#004E89',    # Uber Blue
    'success': '#00A86B',      # Green for good earnings
    'warning': '#FFA500',      # Orange for moderate
    'danger': '#E63946',       # Red for low earnings
    'neutral': '#F1FAEE'       # Light background
}

SURGE_COLORS = {
    1.0: '#4CAF50',   # Green - Normal
    1.5: '#FFC107',   # Yellow - Moderate surge
    2.0: '#F44336'    # Red - High surge
}


def format_currency(value, currency='₹'):
    """
    Format a numeric value as currency.
    
    Args:
        value (float): Value to format
        currency (str): Currency symbol (default ₹ for INR)
        
    Returns:
        str: Formatted currency string
    """
    if pd.isna(value) or value is None:
        return f"{currency}0"
    return f"{currency}{value:,.2f}"


def format_time(minutes):
    """
    Format minutes into human-readable time format.
    
    Args:
        minutes (float): Time in minutes
        
    Returns:
        str: Formatted time string (e.g., "2h 30m")
    """
    if pd.isna(minutes):
        return "0m"
    
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    
    if hours > 0:
        return f"{hours}h {mins}m"
    else:
        return f"{mins}m"


def format_distance(miles):
    """
    Format distance in miles with consistent precision.
    
    Args:
        miles (float): Distance in miles
        
    Returns:
        str: Formatted distance string
    """
    if pd.isna(miles):
        return "0 mi"
    return f"{miles:.1f} mi"


def get_earnings_color(earnings_per_hour):
    """
    Get color based on earnings per hour level.
    
    Args:
        earnings_per_hour (float): Earnings per hour
        
    Returns:
        str: Hex color code
    """
    if earnings_per_hour >= 500:
        return COLOR_SCHEME['success']
    elif earnings_per_hour >= 300:
        return COLOR_SCHEME['warning']
    else:
        return COLOR_SCHEME['danger']


def get_surge_color(surge_multiplier):
    """
    Get color based on surge multiplier level.
    
    Args:
        surge_multiplier (float): Surge multiplier value
        
    Returns:
        str: Hex color code
    """
    if surge_multiplier >= 1.8:
        return SURGE_COLORS[2.0]
    elif surge_multiplier >= 1.3:
        return SURGE_COLORS[1.5]
    else:
        return SURGE_COLORS[1.0]


def get_hour_label(hour):
    """
    Convert 24-hour format to 12-hour format with AM/PM.
    
    Args:
        hour (int): Hour in 24-hour format (0-23)
        
    Returns:
        str: Formatted hour string (e.g., "9 AM", "2 PM")
    """
    if hour == 0:
        return "12 AM"
    elif hour < 12:
        return f"{hour} AM"
    elif hour == 12:
        return "12 PM"
    else:
        return f"{hour - 12} PM"


def get_time_period_emoji(hour):
    """
    Get an emoji representing the time period.
    
    Args:
        hour (int): Hour in 24-hour format
        
    Returns:
        str: Emoji representing the time
    """
    if 6 <= hour < 12:
        return "🌅"  # Morning
    elif 12 <= hour < 17:
        return "☀️"   # Afternoon
    elif 17 <= hour < 22:
        return "🌆"  # Evening
    else:
        return "🌙"  # Night


def calculate_idle_to_active_ratio(total_active_minutes, total_idle_minutes):
    """
    Calculate the ratio of active time to idle time.
    
    Args:
        total_active_minutes (float): Total active/driving time
        total_idle_minutes (float): Total idle/waiting time
        
    Returns:
        float: Ratio of active to idle time
    """
    if total_idle_minutes == 0:
        return float('inf')
    return total_active_minutes / total_idle_minutes if total_active_minutes > 0 else 0


def get_day_name(day_of_week):
    """
    Convert numeric day of week (0-6) to day name.
    
    Args:
        day_of_week (int): Day of week (0=Monday, 6=Sunday)
        
    Returns:
        str: Day name
    """
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if 0 <= day_of_week <= 6:
        return day_names[day_of_week]
    return "Unknown"


def is_weekend(day_of_week):
    """
    Check if day of week is weekend.
    
    Args:
        day_of_week (int): Day of week (0=Monday, 6=Sunday)
        
    Returns:
        bool: True if weekend, False otherwise
    """
    return day_of_week >= 5


def get_recommendation_badge(priority):
    """
    Get a badge/emoji for recommendation priority.
    
    Args:
        priority (str): Priority level ('HIGH', 'MEDIUM', 'LOW')
        
    Returns:
        str: Badge emoji
    """
    badges = {
        'HIGH': '🔴',
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }
    return badges.get(priority, '◯')


def interpolate_value(values, target):
    """
    Interpolate a value within a list of values.
    
    Args:
        values (list): List of known values
        target (float): Target value to interpolate
        
    Returns:
        float: Interpolated value
    """
    if not values or len(values) == 0:
        return 0
    
    sorted_values = sorted(values)
    
    if target <= sorted_values[0]:
        return sorted_values[0]
    elif target >= sorted_values[-1]:
        return sorted_values[-1]
    else:
        # Linear interpolation
        for i in range(len(sorted_values) - 1):
            if sorted_values[i] <= target <= sorted_values[i + 1]:
                ratio = (target - sorted_values[i]) / (sorted_values[i + 1] - sorted_values[i])
                return sorted_values[i] + ratio * (sorted_values[i + 1] - sorted_values[i])
    
    return sorted_values[-1]


def generate_summary_stats(df):
    """
    Generate summary statistics from a dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe with earnings data
        
    Returns:
        dict: Summary statistics
    """
    if len(df) == 0:
        return {
            'total_trips': 0,
            'total_earnings': 0,
            'avg_earnings_per_trip': 0,
            'avg_trip_duration': 0,
            'max_earnings': 0,
            'min_earnings': 0
        }
    
    return {
        'total_trips': len(df),
        'total_earnings': round(df['driver_earnings'].sum(), 2),
        'avg_earnings_per_trip': round(df['driver_earnings'].mean(), 2),
        'avg_trip_duration': round(df['trip_duration_minutes'].mean(), 2),
        'max_earnings': round(df['driver_earnings'].max(), 2),
        'min_earnings': round(df['driver_earnings'].min(), 2),
        'std_dev': round(df['driver_earnings'].std(), 2)
    }


def get_time_range_description(start_hour, end_hour):
    """
    Get human-readable description of a time range.
    
    Args:
        start_hour (int): Start hour (0-23)
        end_hour (int): End hour (0-23)
        
    Returns:
        str: Formatted description
    """
    start_label = get_hour_label(start_hour)
    end_label = get_hour_label(end_hour)
    return f"{start_label} - {end_label}"


def categorize_location_tier(earnings, all_earnings):
    """
    Categorize location tier based on earnings percentile.
    
    Args:
        earnings (float): Location's total earnings
        all_earnings (pd.Series): All locations' earnings
        
    Returns:
        str: Tier category ('Tier 1', 'Tier 2', 'Tier 3', 'Tier 4')
    """
    if len(all_earnings) == 0:
        return 'Unknown'
    
    percentile = (all_earnings <= earnings).sum() / len(all_earnings) * 100
    
    if percentile >= 75:
        return 'Tier 1 (Top Earner)'
    elif percentile >= 50:
        return 'Tier 2 (Above Average)'
    elif percentile >= 25:
        return 'Tier 3 (Average)'
    else:
        return 'Tier 4 (Emerging)'


def create_time_slots(hours=24):
    """
    Create hourly time slots for a day.
    
    Args:
        hours (int): Number of hours in a day (default 24)
        
    Returns:
        list: List of (start_hour, end_hour) tuples
    """
    return [(i, i + 1) for i in range(hours)]


def smooth_series(series, window=3):
    """
    Smooth a time series using rolling mean.
    
    Args:
        series (pd.Series): Input series
        window (int): Window size for rolling mean
        
    Returns:
        pd.Series: Smoothed series
    """
    return series.rolling(window=window, center=True).mean()


def detect_peak_hours(hourly_data, threshold_percentile=75):
    """
    Detect peak hours from hourly data.
    
    Args:
        hourly_data (pd.DataFrame): Hourly demand/earnings data
        threshold_percentile (float): Percentile for peak detection
        
    Returns:
        list: List of peak hour indices
    """
    if len(hourly_data) == 0:
        return []
    
    threshold = hourly_data.quantile(threshold_percentile / 100).values[0]
    peak_hours = hourly_data[hourly_data.iloc[:, 0] > threshold].index.tolist()
    
    return peak_hours


def create_metadata():
    """
    Create metadata about the dashboard.
    
    Returns:
        dict: Metadata dictionary
    """
    return {
        'app_name': 'Uber Driver Profit Maximizer Dashboard',
        'version': '1.0.0',
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'currency': 'INR (₹)',
        'fare_model': {
            'base_fare': 50,
            'cost_per_km': 10,
            'cost_per_minute': 2,
            'driver_commission': 0.75
        }
    }


logger.info("Utility functions module loaded successfully")
