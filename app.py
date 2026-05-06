"""
Uber Driver Profit Maximizer Dashboard - Main Streamlit Application

This is the main entry point for the dashboard. It orchestrates:
- Data loading and preprocessing
- Feature engineering
- Profit calculations
- Interactive UI and visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, time
import os
import sys

# Import custom modules
from data_preprocessing import preprocess_data
from feature_engineering import engineer_features
from profit_model import create_profit_calculator
from utils import (
    format_currency, format_time, format_distance, get_hour_label,
    get_time_period_emoji, get_earnings_color, get_surge_color,
    COLOR_SCHEME, smooth_series, detect_peak_hours, create_metadata
)

# Configure page
st.set_page_config(
    page_title="Uber Driver Profit Maximizer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .title-section {
        border-bottom: 3px solid #FF6B35;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .recommendation-box {
        background: #F1FAEE;
        border-left: 4px solid #FF6B35;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
@st.cache_resource
def load_and_process_data():
    """Load and preprocess data once, cache for session."""
    try:
        dataset_path = "UberDataset.csv"
        if not os.path.exists(dataset_path):
            st.error("❌ Dataset file 'UberDataset.csv' not found!")
            return None
        
        # Preprocess data
        df = preprocess_data(dataset_path)
        
        # Engineer features
        features = engineer_features(df)
        
        return features
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None


def create_header():
    """Create dashboard header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("# 🚗 Uber Driver Profit Maximizer Dashboard")
        st.markdown("### Intelligent insights to maximize your earnings")
    
    with col2:
        metadata = create_metadata()
        st.caption(f"v{metadata['version']}")
        st.caption(f"Updated: {metadata['created_date']}")


def create_sidebar_controls(features, all_locations):
    """Create sidebar controls for user input."""
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # Location selector
    selected_location = st.sidebar.selectbox(
        "📍 Select Your Preferred Location",
        options=sorted(all_locations),
        help="Choose the area where you typically drive"
    )
    
    # Time range selector
    st.sidebar.markdown("### ⏰ Working Hours")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_hour = st.slider(
            "Start Hour",
            0, 23, 8,
            help="Hour to start driving (0-23)"
        )
    with col2:
        end_hour = st.slider(
            "End Hour",
            0, 23, 22,
            help="Hour to stop driving (0-23)"
        )
    
    # Adjust if invalid range
    if end_hour <= start_hour:
        end_hour = start_hour + 8
    
    # Surge pricing toggle
    st.sidebar.markdown("### 💰 Pricing Options")
    enable_surge = st.sidebar.checkbox("Enable Surge Pricing Simulation", value=True)
    
    if enable_surge:
        surge_multiplier = st.sidebar.slider(
            "Surge Multiplier",
            min_value=1.0,
            max_value=2.0,
            step=0.1,
            value=1.0,
            help="1.0 = Normal pricing, 2.0 = 2x surge"
        )
    else:
        surge_multiplier = 1.0
    
    # Working hours per day
    shift_hours = st.sidebar.slider(
        "Daily Shift Duration (hours)",
        min_value=1,
        max_value=24,
        value=8,
        help="How many hours you plan to work"
    )
    
    return {
        'location': selected_location,
        'start_hour': start_hour,
        'end_hour': end_hour,
        'surge_multiplier': surge_multiplier,
        'shift_hours': shift_hours
    }


def display_profit_summary(calculator, controls):
    """Display main profit summary cards."""
    st.markdown("## 💰 Profit Summary")
    
    # Calculate profit
    profit_result = calculator.calculate_driver_profit(
        (controls['start_hour'], controls['end_hour']),
        controls['location'],
        controls['surge_multiplier'],
        controls['shift_hours']
    )
    
    # Create metric columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💵 Total Earnings",
            format_currency(profit_result['projected_earnings_full_shift']),
            f"{controls['shift_hours']}h shift"
        )
    
    with col2:
        st.metric(
            "⏱️ Earnings/Hour",
            format_currency(profit_result['earnings_per_hour']),
            help="Projected earnings per hour"
        )
    
    with col3:
        st.metric(
            "🚗 Estimated Trips",
            int(profit_result['projected_trips_full_shift']),
            f"Avg ₹{profit_result['avg_earnings_per_trip']:.0f}/trip"
        )
    
    with col4:
        idle_hours = profit_result['total_idle_time_minutes'] / 60
        st.metric(
            "⏸️ Idle Time",
            format_time(profit_result['total_idle_time_minutes']),
            f"{idle_hours:.1f}h idle"
        )
    
    return profit_result


def display_recommendations(calculator, location):
    """Display recommendations section."""
    st.markdown("## 🎯 Smart Recommendations")
    
    suggestions = calculator.get_optimization_suggestions(location)
    
    for rec in suggestions['recommendations']:
        priority_badge = "🔴" if rec['priority'] == 'HIGH' else "🟡" if rec['priority'] == 'MEDIUM' else "🟢"
        
        with st.container():
            st.markdown(f"""
            <div class="recommendation-box">
                <b>{priority_badge} {rec['suggestion']}</b><br>
                <small>{rec['impact']}</small>
            </div>
            """, unsafe_allow_html=True)


def display_best_hours_location(calculator, controls):
    """Display best hours and locations analysis."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⏰ Best Hours to Drive")
        st.markdown(f"**In {controls['location']}**")
        
        best_hours = calculator.get_best_hours_for_location(controls['location'], top_n=5)
        
        if not best_hours.empty:
            # Create hour performance chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[get_hour_label(h) for h in best_hours.index],
                y=best_hours['avg_earnings_per_trip'],
                marker_color=[get_surge_color(1.0 + i*0.2) for i in range(len(best_hours))],
                name="Avg Earnings/Trip"
            ))
            
            fig.update_layout(
                title="Top 5 Hours by Earnings",
                xaxis_title="Hour",
                yaxis_title="Avg Earnings (₹)",
                height=300,
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display table
            display_df = best_hours.copy()
            display_df.index = [get_hour_label(h) for h in display_df.index]
            st.dataframe(display_df, use_container_width=True)
        else:
            st.warning("No data available for this location")
    
    with col2:
        st.markdown("### 📍 Best Locations to Drive")
        st.markdown("**Overall Top Earners**")
        
        best_locations = calculator.get_best_locations_overall(top_n=5)
        
        if not best_locations.empty:
            # Create location performance chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=best_locations.index,
                y=best_locations['avg_earnings_per_trip'],
                marker_color=COLOR_SCHEME['primary'],
                name="Avg Earnings/Trip"
            ))
            
            fig.update_layout(
                title="Top 5 Locations by Earnings/Trip",
                xaxis_title="Location",
                yaxis_title="Avg Earnings (₹)",
                height=300,
                showlegend=False,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display table
            display_df = best_locations[['total_trips', 'avg_earnings_per_trip', 'earnings_per_hour']].copy()
            st.dataframe(display_df, use_container_width=True)
        else:
            st.warning("No location data available")


def display_demand_heatmap(features):
    """Display demand heatmap visualization."""
    st.markdown("## 🔥 Demand Heatmap")
    st.markdown("**Earnings by Hour and Location**")
    
    hour_location_matrix = features['hour_location_matrix']
    
    if not hour_location_matrix.empty:
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=hour_location_matrix.values,
            x=hour_location_matrix.columns,
            y=[get_hour_label(h) for h in hour_location_matrix.index],
            colorscale='RdYlGn',
            name='Avg Earnings (₹)',
            hovertemplate='Hour: %{y}<br>Location: %{x}<br>Avg Earnings: ₹%{z:.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Average Earnings per Trip by Hour and Location",
            xaxis_title="Location",
            yaxis_title="Hour of Day",
            height=500,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Insufficient data for heatmap")


def display_earnings_trends(features):
    """Display earnings trends over time."""
    st.markdown("## 📈 Earnings Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Hourly Trend")
        hourly_data = features['demand_metrics']['hourly_demand']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=[get_hour_label(h) for h in hourly_data.index],
            y=hourly_data['total_earnings'],
            mode='lines+markers',
            name='Total Earnings',
            line=dict(color=COLOR_SCHEME['primary'], width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Cumulative Earnings by Hour",
            xaxis_title="Hour",
            yaxis_title="Total Earnings (₹)",
            height=350,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Daily Trend")
        daily_data = features['demand_metrics']['daily_demand']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily_data.index,
            y=daily_data['total_earnings'],
            marker=dict(color=daily_data['total_earnings'], 
                       colorscale='Viridis',
                       showscale=False),
            name='Daily Earnings'
        ))
        
        fig.update_layout(
            title="Total Earnings by Day of Week",
            xaxis_title="Day",
            yaxis_title="Total Earnings (₹)",
            height=350,
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)


def display_what_if_analysis(calculator, controls):
    """Display "What If?" scenario analysis."""
    st.markdown("## 🎮 What-If Analysis")
    st.markdown("**Simulate different scenarios and see how your earnings change**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Surge Pricing Impact")
        surge_values = [1.0, 1.3, 1.5, 1.8, 2.0]
        
        scenarios = []
        for surge in surge_values:
            result = calculator.calculate_driver_profit(
                (controls['start_hour'], controls['end_hour']),
                controls['location'],
                surge,
                controls['shift_hours']
            )
            scenarios.append({
                'Surge': f"{surge}x",
                'Earnings': result['projected_earnings_full_shift'],
                'Per Hour': result['earnings_per_hour']
            })
        
        scenario_df = pd.DataFrame(scenarios)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=scenario_df['Surge'],
            y=scenario_df['Earnings'],
            mode='lines+markers',
            name='Total Earnings',
            line=dict(color=COLOR_SCHEME['primary'], width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title="Earnings vs Surge Multiplier",
            xaxis_title="Surge Multiplier",
            yaxis_title="Total Earnings (₹)",
            height=300,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Shift Duration Impact")
        hours_values = [2, 4, 6, 8, 10, 12]
        
        scenarios = []
        for hours in hours_values:
            result = calculator.calculate_driver_profit(
                (controls['start_hour'], controls['end_hour']),
                controls['location'],
                controls['surge_multiplier'],
                hours
            )
            scenarios.append({
                'Hours': f"{hours}h",
                'Earnings': result['projected_earnings_full_shift'],
                'Per Hour': result['earnings_per_hour']
            })
        
        scenario_df = pd.DataFrame(scenarios)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=scenario_df['Hours'],
            y=scenario_df['Earnings'],
            mode='lines+markers',
            name='Total Earnings',
            line=dict(color=COLOR_SCHEME['secondary'], width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title="Earnings vs Shift Duration",
            xaxis_title="Shift Duration",
            yaxis_title="Total Earnings (₹)",
            height=300,
            hovermode='x unified',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)


def display_shift_comparison(calculator, controls):
    """Display shift comparison analysis."""
    st.markdown("## ⚖️ Shift Comparison")
    st.markdown("**Morning vs Afternoon vs Evening vs Night Shifts**")
    
    shift_configs = [
        {'name': '🌅 Morning Shift', 'start_hour': 6, 'end_hour': 14, 'surge_multiplier': 1.2},
        {'name': '☀️ Afternoon Shift', 'start_hour': 12, 'end_hour': 20, 'surge_multiplier': 1.0},
        {'name': '🌆 Evening Shift', 'start_hour': 17, 'end_hour': 1, 'surge_multiplier': 1.5},
        {'name': '🌙 Night Shift', 'start_hour': 20, 'end_hour': 4, 'surge_multiplier': 1.3}
    ]
    
    comparison = calculator.compare_shifts(controls['location'], shift_configs)
    
    # Create comparison visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=comparison['shift_name'],
            y=comparison['projected_earnings_full_shift'],
            marker_color=[COLOR_SCHEME['primary'], COLOR_SCHEME['secondary'], 
                         COLOR_SCHEME['warning'], COLOR_SCHEME['danger']],
            name='Earnings'
        ))
        
        fig.update_layout(
            title="Total Shift Earnings Comparison",
            xaxis_title="Shift Type",
            yaxis_title="Total Earnings (₹)",
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=comparison['shift_name'],
            y=comparison['earnings_per_hour'],
            marker_color=[COLOR_SCHEME['primary'], COLOR_SCHEME['secondary'], 
                         COLOR_SCHEME['warning'], COLOR_SCHEME['danger']],
            name='Per Hour'
        ))
        
        fig.update_layout(
            title="Hourly Rate Comparison",
            xaxis_title="Shift Type",
            yaxis_title="Earnings/Hour (₹)",
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed comparison table
    st.markdown("### Detailed Comparison")
    display_df = comparison[[
        'shift_name', 'projected_trips_full_shift', 'total_active_time_minutes',
        'total_idle_time_minutes', 'projected_earnings_full_shift', 'earnings_per_hour'
    ]].copy()
    
    display_df.columns = ['Shift', 'Trips', 'Active Time (min)', 'Idle Time (min)', 'Total Earnings (₹)', 'Per Hour (₹)']
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def display_analytics_section(features):
    """Display detailed analytics section."""
    st.markdown("## 📊 Detailed Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Demand Analysis", "🗺️ Location Analysis", "📅 Time Analysis"])
    
    with tab1:
        st.markdown("### Demand Metrics by Hour")
        hourly_demand = features['demand_metrics']['hourly_demand']
        
        fig = px.bar(
            hourly_demand.reset_index(),
            x='pickup_hour',
            y='trips_count',
            labels={'pickup_hour': 'Hour', 'trips_count': 'Number of Trips'},
            color='avg_earnings_per_trip',
            color_continuous_scale='Viridis',
            title="Trip Volume and Avg Earnings by Hour"
        )
        
        fig.update_xaxes(tickformat='.0f')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(hourly_demand, use_container_width=True)
    
    with tab2:
        st.markdown("### Location Performance Metrics")
        location_demand = features['demand_metrics']['location_demand']
        
        fig = px.bar(
            location_demand.head(15).reset_index(),
            x='START',
            y='total_earnings',
            labels={'START': 'Location', 'total_earnings': 'Total Earnings (₹)'},
            color='avg_earnings',
            color_continuous_scale='RdYlGn',
            title="Top 15 Locations by Total Earnings"
        )
        
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(location_demand.head(15), use_container_width=True)
    
    with tab3:
        st.markdown("### Performance by Time Period")
        period_demand = features['demand_metrics']['period_demand']
        
        fig = px.pie(
            values=period_demand['total_earnings'],
            names=period_demand.index,
            title="Earnings Distribution by Time Period"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(period_demand, use_container_width=True)


def display_idle_time_analysis(features):
    """Display idle time analysis."""
    st.markdown("## ⏸️ Idle Time Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Idle Time Estimates by Location")
        
        idle_estimates = features['idle_estimates']
        if idle_estimates:
            idle_df = pd.DataFrame.from_dict(idle_estimates, orient='index')
            idle_df = idle_df.sort_values('avg_idle_minutes', ascending=False).head(10)
            st.dataframe(idle_df, use_container_width=True)
        else:
            st.info("Using default idle time estimates (15 min average)")
    
    with col2:
        st.markdown("### Expected Wait Times Distribution")
        
        default_idle = features['default_idle']
        wait_times = {
            'Min Wait': default_idle['min_idle'],
            'Avg Wait': default_idle['avg_idle_minutes'],
            'Max Wait': default_idle['max_idle']
        }
        
        fig = go.Figure(data=[
            go.Bar(x=list(wait_times.keys()), y=list(wait_times.values()),
                   marker_color=[COLOR_SCHEME['success'], COLOR_SCHEME['warning'], COLOR_SCHEME['danger']])
        ])
        
        fig.update_layout(
            title="Typical Wait Time Ranges (minutes)",
            yaxis_title="Minutes",
            showlegend=False,
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Impact Analysis:**
        - Active driving time: Where you earn money
        - Idle time: Where you don't earn but need to wait
        - Optimal areas have low idle time and high demand
        """)


def main():
    """Main application function."""
    # Load data
    features = load_and_process_data()
    
    if features is None:
        st.error("Failed to load dataset. Please ensure 'UberDataset.csv' exists in the current directory.")
        return
    
    # Create header
    create_header()
    
    # Get all locations
    all_locations = sorted(features['location_features'].index.tolist())
    
    # Sidebar controls
    controls = create_sidebar_controls(features, all_locations)
    
    # Create calculator
    calculator = create_profit_calculator(features)
    
    # Main content
    st.markdown("---")
    
    # Display profit summary
    profit_result = display_profit_summary(calculator, controls)
    
    st.markdown("---")
    
    # Display recommendations
    display_recommendations(calculator, controls['location'])
    
    st.markdown("---")
    
    # Best hours and locations
    display_best_hours_location(calculator, controls)
    
    st.markdown("---")
    
    # Demand heatmap
    display_demand_heatmap(features)
    
    st.markdown("---")
    
    # Earnings trends
    display_earnings_trends(features)
    
    st.markdown("---")
    
    # What-if analysis
    display_what_if_analysis(calculator, controls)
    
    st.markdown("---")
    
    # Shift comparison
    display_shift_comparison(calculator, controls)
    
    st.markdown("---")
    
    # Detailed analytics
    display_analytics_section(features)
    
    st.markdown("---")
    
    # Idle time analysis
    display_idle_time_analysis(features)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    ---
    ### 📌 About This Dashboard
    
    **Fare Model (Simulated):**
    - Base Fare: ₹50
    - Per Kilometer: ₹10
    - Per Minute: ₹2
    - Driver Commission: 75% of fare
    
    **Data Source:** Uber trips dataset (2016)
    
    **Disclaimer:** This dashboard uses historical data and simulated fare models. 
    Actual earnings may vary based on actual surge pricing, promotions, and real-time demand.
    
    *Maximize your earnings! 💰*
    """)


if __name__ == "__main__":
    main()
