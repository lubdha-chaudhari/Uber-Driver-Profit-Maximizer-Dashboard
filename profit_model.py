"""
Profit Model Module for Uber Driver Profit Maximizer Dashboard

This module handles:
- Profit calculation for given time ranges and locations
- Surge pricing simulation
- Shift recommendations
- "What if?" scenario analysis
- Optimization suggestions
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfitCalculator:
    """Main class for calculating driver profits and generating recommendations."""
    
    def __init__(self, features_dict):
        """
        Initialize the profit calculator with engineered features.
        
        Args:
            features_dict (dict): Dictionary containing engineered features from feature_engineering module
        """
        self.df = features_dict['dataframe']
        self.demand_metrics = features_dict['demand_metrics']
        self.idle_estimates = features_dict['idle_estimates']
        self.default_idle = features_dict['default_idle']
        self.location_features = features_dict['location_features']
        self.hour_location_matrix = features_dict['hour_location_matrix']
        
        logger.info("ProfitCalculator initialized successfully")
    
    
    def calculate_driver_profit(self, hour_range, location, surge_multiplier=1.0, duration_hours=8):
        """
        Calculate estimated profit for a given time range and location.
        
        Args:
            hour_range (tuple): (start_hour, end_hour) in 24-hour format
            location (str): Pickup location
            surge_multiplier (float): Surge pricing multiplier
            duration_hours (float): How many hours the driver plans to work
            
        Returns:
            dict: Profit analysis including earnings, trips, idle time, etc.
        """
        start_hour, end_hour = hour_range
        
        # Filter data for the given time range and location
        mask = (
            (self.df['pickup_hour'] >= start_hour) & 
            (self.df['pickup_hour'] < end_hour) &
            (self.df['START'] == location)
        )
        
        filtered_data = self.df[mask]
        
        if len(filtered_data) == 0:
            # Return default estimates if no data
            return self._generate_default_profit(hour_range, location, surge_multiplier)
        
        # Calculate metrics
        num_trips = len(filtered_data)
        total_active_time = filtered_data['trip_duration_minutes'].sum()
        avg_earnings_per_trip = filtered_data['driver_earnings'].mean() * surge_multiplier
        total_earnings = num_trips * avg_earnings_per_trip
        
        # Estimate idle time
        location_idle = self.idle_estimates.get(location, self.default_idle)
        estimated_idle_time = num_trips * location_idle['avg_idle_minutes']
        
        # Total time accounting for idle
        total_time_minutes = total_active_time + estimated_idle_time
        total_time_hours = total_time_minutes / 60
        
        # Earnings per hour
        earnings_per_hour = total_earnings / duration_hours if duration_hours > 0 else 0
        
        # Calculate if extended to full shift
        if total_time_hours < duration_hours and total_time_hours > 0:
            trip_rate_per_hour = num_trips / total_time_hours
            projected_trips = int(trip_rate_per_hour * duration_hours)
            projected_earnings = projected_trips * avg_earnings_per_trip
        else:
            projected_trips = num_trips
            projected_earnings = total_earnings
        
        result = {
            'location': location,
            'time_period': f"{start_hour:02d}:00 - {end_hour:02d}:00",
            'hour_range': (start_hour, end_hour),
            'num_trips': num_trips,
            'actual_trips_in_period': num_trips,
            'projected_trips_full_shift': projected_trips,
            'total_active_time_minutes': round(total_active_time, 2),
            'total_idle_time_minutes': round(estimated_idle_time, 2),
            'total_time_minutes': round(total_time_minutes, 2),
            'avg_earnings_per_trip': round(avg_earnings_per_trip, 2),
            'total_earnings': round(total_earnings, 2),
            'projected_earnings_full_shift': round(projected_earnings, 2),
            'earnings_per_hour': round(earnings_per_hour, 2),
            'surge_multiplier': surge_multiplier,
            'has_data': True
        }
        
        return result
    
    
    def _generate_default_profit(self, hour_range, location, surge_multiplier=1.0):
        """
        Generate default profit estimate when no historical data is available.
        
        Args:
            hour_range (tuple): (start_hour, end_hour)
            location (str): Location name
            surge_multiplier (float): Surge multiplier
            
        Returns:
            dict: Default profit estimate
        """
        # Use average across all data
        avg_trips_per_hour = len(self.df) / 24  # Rough estimate
        avg_earnings = self.df['driver_earnings'].mean() * surge_multiplier
        
        start_hour, end_hour = hour_range
        hours = end_hour - start_hour if end_hour > start_hour else 24 - start_hour + end_hour
        
        num_trips = int(avg_trips_per_hour * hours)
        total_earnings = num_trips * avg_earnings
        earnings_per_hour = total_earnings / hours if hours > 0 else 0
        
        return {
            'location': location,
            'time_period': f"{start_hour:02d}:00 - {end_hour:02d}:00",
            'hour_range': hour_range,
            'num_trips': num_trips,
            'actual_trips_in_period': 0,
            'projected_trips_full_shift': num_trips,
            'total_active_time_minutes': num_trips * 15,
            'total_idle_time_minutes': num_trips * 15,
            'total_time_minutes': num_trips * 30,
            'avg_earnings_per_trip': round(avg_earnings, 2),
            'total_earnings': round(total_earnings, 2),
            'projected_earnings_full_shift': round(total_earnings, 2),
            'earnings_per_hour': round(earnings_per_hour, 2),
            'surge_multiplier': surge_multiplier,
            'has_data': False
        }
    
    
    def get_best_hours_for_location(self, location, top_n=5):
        """
        Get the best hours to drive in a specific location.
        
        Args:
            location (str): Location name
            top_n (int): Number of top hours to return
            
        Returns:
            pd.DataFrame: Top N hours with earnings data
        """
        location_data = self.df[self.df['START'] == location]
        
        if len(location_data) == 0:
            return pd.DataFrame()
        
        hourly_earnings = location_data.groupby('pickup_hour').agg({
            'driver_earnings': ['count', 'sum', 'mean'],
            'trip_duration_minutes': 'mean'
        }).round(2)
        
        hourly_earnings.columns = ['trips', 'total_earnings', 'avg_earnings_per_trip', 'avg_duration']
        hourly_earnings = hourly_earnings.sort_values('total_earnings', ascending=False)
        
        return hourly_earnings.head(top_n)
    
    
    def get_best_locations_for_hour(self, hour, top_n=5):
        """
        Get the best locations to drive during a specific hour.
        
        Args:
            hour (int): Hour in 24-hour format
            top_n (int): Number of top locations to return
            
        Returns:
            pd.DataFrame: Top N locations with earnings data
        """
        hour_data = self.df[self.df['pickup_hour'] == hour]
        
        if len(hour_data) == 0:
            return pd.DataFrame()
        
        location_earnings = hour_data.groupby('START').agg({
            'driver_earnings': ['count', 'sum', 'mean'],
            'MILES': 'mean'
        }).round(2)
        
        location_earnings.columns = ['trips', 'total_earnings', 'avg_earnings', 'avg_distance']
        location_earnings = location_earnings.sort_values('total_earnings', ascending=False)
        
        return location_earnings.head(top_n)
    
    
    def get_best_locations_overall(self, top_n=5):
        """
        Get the best locations overall.
        
        Args:
            top_n (int): Number of top locations to return
            
        Returns:
            pd.DataFrame: Top N locations with all features
        """
        return self.location_features.head(top_n)
    
    
    def get_surge_recommendation(self, hour, location):
        """
        Generate surge pricing recommendation for given hour and location.
        
        Args:
            hour (int): Hour in 24-hour format
            location (str): Location name
            
        Returns:
            dict: Surge recommendation with multiplier suggestion
        """
        demand_hour = self.demand_metrics['hourly_demand'].loc[hour] if hour in self.demand_metrics['hourly_demand'].index else None
        demand_location = self.location_features.loc[location] if location in self.location_features.index else None
        
        if demand_hour is None or demand_location is None:
            return {'surge_multiplier': 1.0, 'reason': 'Insufficient data'}
        
        trips_hour = demand_hour['trips_count']
        avg_trips = self.demand_metrics['hourly_demand']['trips_count'].mean()
        
        # Surge multiplier based on demand relative to average
        demand_ratio = trips_hour / avg_trips if avg_trips > 0 else 1.0
        
        if demand_ratio > 1.5:
            surge_multiplier = 2.0
            reason = 'High demand - Peak hours'
        elif demand_ratio > 1.2:
            surge_multiplier = 1.5
            reason = 'Moderate demand - Above average'
        else:
            surge_multiplier = 1.0
            reason = 'Normal demand'
        
        return {
            'surge_multiplier': surge_multiplier,
            'reason': reason,
            'demand_ratio': round(demand_ratio, 2)
        }
    
    
    def compare_shifts(self, location, shift_configs):
        """
        Compare profitability of different shift configurations.
        
        Args:
            location (str): Location name
            shift_configs (list): List of dicts with 'name', 'start_hour', 'end_hour', 'surge_multiplier'
            
        Returns:
            pd.DataFrame: Comparison of different shifts
        """
        comparisons = []
        
        for config in shift_configs:
            result = self.calculate_driver_profit(
                (config['start_hour'], config['end_hour']),
                location,
                config.get('surge_multiplier', 1.0)
            )
            result['shift_name'] = config['name']
            comparisons.append(result)
        
        comparison_df = pd.DataFrame(comparisons)
        return comparison_df.sort_values('earnings_per_hour', ascending=False)
    
    
    def simulate_what_if(self, location, base_hour_range, parameters_to_vary):
        """
        Simulate "What if?" scenarios by varying parameters.
        
        Args:
            location (str): Location name
            base_hour_range (tuple): Base (start_hour, end_hour)
            parameters_to_vary (dict): Parameters to vary and their ranges
                e.g., {'surge_multiplier': [1.0, 1.5, 2.0], 'duration_hours': [4, 6, 8]}
            
        Returns:
            pd.DataFrame: Simulation results for different parameter combinations
        """
        scenarios = []
        
        surge_multipliers = parameters_to_vary.get('surge_multiplier', [1.0])
        durations = parameters_to_vary.get('duration_hours', [8])
        
        for surge in surge_multipliers:
            for duration in durations:
                result = self.calculate_driver_profit(
                    base_hour_range, location, surge, duration
                )
                result['scenario_id'] = f"Surge {surge}x, {duration}h shift"
                scenarios.append(result)
        
        scenario_df = pd.DataFrame(scenarios)
        return scenario_df
    
    
    def get_optimization_suggestions(self, location, available_hours_per_week=40):
        """
        Generate AI-like optimization suggestions for a driver.
        
        Args:
            location (str): Driver's preferred location
            available_hours_per_week (float): Hours available to work per week
            
        Returns:
            dict: Optimization suggestions
        """
        suggestions = {
            'location': location,
            'available_hours': available_hours_per_week,
            'recommendations': []
        }
        
        # Get best hours for this location
        best_hours = self.get_best_hours_for_location(location, top_n=3)
        
        if not best_hours.empty:
            best_hour = best_hours.index[0]
            suggestions['recommendations'].append({
                'priority': 'HIGH',
                'suggestion': f'Peak earning hour: {best_hour:02d}:00-{best_hour+1:02d}:00',
                'impact': f"Avg earnings: ₹{best_hours.iloc[0]['avg_earnings_per_trip']:.0f}/trip"
            })
        
        # Get best locations overall
        best_locations = self.get_best_locations_overall(top_n=3)
        
        if not best_locations.empty and location in best_locations.index:
            rank = list(best_locations.index).index(location) + 1
            suggestions['recommendations'].append({
                'priority': 'MEDIUM',
                'suggestion': f'Your location ranks #{rank} by total earnings',
                'impact': f"Top earner: {best_locations.index[0]}"
            })
        
        # Weekend vs Weekday analysis
        weekend_data = self.df[self.df['is_weekend'] == 1]
        weekday_data = self.df[self.df['is_weekend'] == 0]
        
        if len(weekend_data) > 0 and len(weekday_data) > 0:
            weekend_avg = weekend_data['driver_earnings'].mean()
            weekday_avg = weekday_data['driver_earnings'].mean()
            
            if weekend_avg > weekday_avg:
                suggestions['recommendations'].append({
                    'priority': 'MEDIUM',
                    'suggestion': 'Weekend shifts are more profitable',
                    'impact': f"Weekend avg: ₹{weekend_avg:.0f} vs Weekday: ₹{weekday_avg:.0f}"
                })
        
        # Shift duration recommendation
        suggestions['recommendations'].append({
            'priority': 'LOW',
            'suggestion': f'Optimal shift: 8 hours',
            'impact': 'Balances earnings with fatigue/driving limits'
        })
        
        return suggestions


def create_profit_calculator(features_dict):
    """
    Factory function to create a ProfitCalculator instance.
    
    Args:
        features_dict (dict): Features dictionary from feature_engineering
        
    Returns:
        ProfitCalculator: Initialized calculator
    """
    return ProfitCalculator(features_dict)
