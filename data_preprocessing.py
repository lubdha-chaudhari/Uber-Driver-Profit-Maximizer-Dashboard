"""
Data Preprocessing Module for Uber Driver Profit Maximizer Dashboard

This module handles:
- Loading and validating the Uber dataset
- Parsing datetime fields
- Extracting temporal features
- Handling missing and outlier values
- Data cleaning and normalization
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_dataset(filepath):
    """
    Load and validate the Uber dataset.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
        
        # Remove 'Totals' row if present
        df = df[df['START_DATE'] != 'Totals'].copy()
        df = df.dropna(subset=['START_DATE', 'END_DATE'])
        logger.info(f"After removing totals row. Shape: {df.shape}")
        
        # Validate required columns
        required_cols = ['START_DATE', 'END_DATE', 'START', 'STOP', 'MILES']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading dataset: {str(e)}")
        raise


def parse_datetime_columns(df):
    """
    Parse START_DATE and END_DATE columns and handle inconsistent formats.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: DataFrame with parsed datetime columns
    """
    df = df.copy()
    
    # Try multiple datetime formats
    formats = ['%m-%d-%Y %H:%M', '%m/%d/%Y %H:%M', '%d-%m-%Y %H:%M']
    
    for col in ['START_DATE', 'END_DATE']:
        parsed = False
        for fmt in formats:
            try:
                df[col] = pd.to_datetime(df[col], format=fmt)
                logger.info(f"Successfully parsed {col} with format {fmt}")
                parsed = True
                break
            except (ValueError, TypeError):
                continue
        
        # If still not parsed, use pd.to_datetime with mixed format
        if not parsed and not pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], format='mixed')
                logger.info(f"Successfully parsed {col} with mixed format")
                parsed = True
            except Exception as e:
                logger.warning(f"Could not parse {col} with mixed format: {str(e)}")
        
        # Final fallback
        if not parsed and not pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
                logger.info(f"Successfully parsed {col} with default parsing")
            except Exception as e:
                logger.warning(f"Could not parse {col}: {str(e)}")
                df[col] = pd.NaT
    
    return df


def extract_temporal_features(df):
    """
    Extract temporal features from datetime columns.
    
    Args:
        df (pd.DataFrame): DataFrame with parsed datetime
        
    Returns:
        pd.DataFrame: DataFrame with new temporal features
    """
    df = df.copy()
    
    # Ensure datetime parsing
    if not pd.api.types.is_datetime64_any_dtype(df['START_DATE']):
        df = parse_datetime_columns(df)
    
    # Extract features
    df['pickup_hour'] = df['START_DATE'].dt.hour
    df['pickup_day_of_week'] = df['START_DATE'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['pickup_date'] = df['START_DATE'].dt.date
    df['is_weekend'] = df['pickup_day_of_week'].isin([5, 6]).astype(int)
    
    # Calculate trip duration in minutes
    df['trip_duration_minutes'] = (df['END_DATE'] - df['START_DATE']).dt.total_seconds() / 60
    
    # Create time period categories
    def categorize_time_period(hour):
        """Categorize hour into time periods."""
        if 6 <= hour < 12:
            return 'Morning (6-12)'
        elif 12 <= hour < 17:
            return 'Afternoon (12-5)'
        elif 17 <= hour < 22:
            return 'Evening (5-10)'
        else:
            return 'Night (10-6)'
    
    df['time_period'] = df['pickup_hour'].apply(categorize_time_period)
    
    logger.info("Temporal features extracted successfully")
    return df


def handle_missing_values(df):
    """
    Handle missing values in critical columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: DataFrame with missing values handled
    """
    df = df.copy()
    
    # Log missing values
    missing_info = df.isnull().sum()
    if missing_info.sum() > 0:
        logger.info(f"Missing values detected:\n{missing_info[missing_info > 0]}")
    
    # Handle missing values
    df['MILES'].fillna(df['MILES'].median(), inplace=True)
    df['trip_duration_minutes'].fillna(df['trip_duration_minutes'].median(), inplace=True)
    df['PURPOSE'].fillna('Unknown', inplace=True)
    df['CATEGORY'].fillna('Unknown', inplace=True)
    
    # Drop rows with missing critical datetime fields
    df.dropna(subset=['START_DATE', 'END_DATE', 'START', 'STOP'], inplace=True)
    
    logger.info(f"Missing values handled. Final shape: {df.shape}")
    return df


def remove_outliers(df, distance_threshold=100, duration_threshold=480):
    """
    Remove outliers based on distance and duration.
    
    Args:
        df (pd.DataFrame): Input dataframe
        distance_threshold (float): Maximum acceptable distance in miles (default 100)
        duration_threshold (float): Maximum acceptable duration in minutes (default 480=8 hours)
        
    Returns:
        pd.DataFrame: DataFrame with outliers removed
    """
    df = df.copy()
    initial_size = len(df)
    
    # Remove extreme distances
    df = df[df['MILES'] <= distance_threshold]
    
    # Remove extreme durations
    df = df[df['trip_duration_minutes'] <= duration_threshold]
    
    # Remove trips with zero or negative values
    df = df[df['MILES'] > 0]
    df = df[df['trip_duration_minutes'] > 0]
    
    removed_count = initial_size - len(df)
    logger.info(f"Removed {removed_count} outlier records. Remaining: {len(df)}")
    
    return df


def preprocess_data(filepath):
    """
    Complete preprocessing pipeline.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Fully preprocessed dataset
    """
    logger.info("=" * 50)
    logger.info("Starting data preprocessing pipeline...")
    logger.info("=" * 50)
    
    # Load data
    df = load_dataset(filepath)
    
    # Parse datetime
    df = parse_datetime_columns(df)
    
    # Extract temporal features
    df = extract_temporal_features(df)
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Remove outliers
    df = remove_outliers(df)
    
    logger.info("=" * 50)
    logger.info("Preprocessing complete!")
    logger.info(f"Final dataset shape: {df.shape}")
    logger.info("=" * 50)
    
    return df
