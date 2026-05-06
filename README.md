# 🚗 Uber Driver Profit Maximizer Dashboard

A comprehensive Streamlit-based intelligent dashboard that helps Uber drivers make data-driven decisions about when, where, and how to drive to maximize earnings.

## 📋 Project Overview

This project transforms raw Uber trip data into actionable insights and profit recommendations through:
- **Smart Analytics**: Demand patterns, peak hours, best locations
- **Profit Prediction**: Earnings forecasts with surge pricing simulation
- **What-If Scenarios**: Interactive "what if?" analysis to explore different strategies
- **Shift Optimization**: Automatic recommendations for optimal driving patterns
- **Interactive Visualizations**: Heatmaps, charts, and trend analysis

---

## 🎯 Key Features

### 1. **Profit Summary Dashboard**
- Total estimated earnings for selected time and location
- Hourly earnings rate
- Trip count projections
- Idle time analysis

### 2. **Smart Recommendations**
- Personalized suggestions based on historical data
- Peak hour identification
- Best location rankings
- Optimal shift timing

### 3. **Best Hours & Locations Analysis**
- Top performing hours in selected location
- Best locations overall
- Performance metrics by time period

### 4. **Demand Heatmap**
- Visual representation of earnings by hour and location
- Color-coded demand intensity
- Interactive exploration

### 5. **Earnings Trends**
- Hourly trend analysis
- Day-of-week breakdown
- Time period comparison

### 6. **What-If Scenarios**
- Surge pricing impact simulation
- Shift duration impact analysis
- Compare different working patterns

### 7. **Shift Comparison**
- Morning, Afternoon, Evening, Night shifts
- Side-by-side profitability comparison
- Hourly rate comparison

### 8. **Detailed Analytics**
- Demand metrics by hour
- Location performance rankings
- Time period analysis

### 9. **Idle Time Analysis**
- Location-based idle time estimates
- Wait time distribution
- Impact on overall earnings

---

## 📁 Project Structure

```
uber/
├── app.py                      # Main Streamlit application
├── data_preprocessing.py        # Data loading and cleaning
├── feature_engineering.py       # Feature creation and aggregation
├── profit_model.py              # Profit calculation and recommendations
├── utils.py                     # Utility functions and helpers
├── requirements.txt             # Python dependencies
├── UberDataset.csv             # Input dataset
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd uber
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

---

## 📊 Dataset Format

The application expects a CSV file named `UberDataset.csv` with the following columns:

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| START_DATE | datetime | 01-01-2016 21:11 | Trip start time |
| END_DATE | datetime | 01-01-2016 21:17 | Trip end time |
| START | string | Fort Pierce | Pickup location |
| STOP | string | Fort Pierce | Dropoff location |
| MILES | float | 5.1 | Trip distance in miles |
| CATEGORY | string | Business | Trip category |
| PURPOSE | string | Meal/Entertain | Trip purpose |

---

## 💰 Fare Model

The application uses a simulated fare model (as actual fare data is not provided):

```
Fare Calculation:
fare = base_fare + (distance_km × cost_per_km) + (duration_minutes × cost_per_minute)

Where:
- Base Fare: ₹50
- Cost per km: ₹10
- Cost per minute: ₹2
- Distance conversion: 1 mile = 1.60934 km

Driver Earnings:
driver_earnings = fare × surge_multiplier × 0.75
(Driver receives 75% of fare as commission)
```

---

## 🔧 Module Documentation

### 1. **data_preprocessing.py**
Handles data loading, cleaning, and temporal feature extraction.

**Key Functions:**
- `load_dataset(filepath)` - Load CSV with validation
- `parse_datetime_columns(df)` - Handle multiple datetime formats
- `extract_temporal_features(df)` - Create hour, day, weekend flags
- `handle_missing_values(df)` - Imputation and cleanup
- `remove_outliers(df)` - Remove extreme values
- `preprocess_data(filepath)` - Complete pipeline

### 2. **feature_engineering.py**
Creates predictive features and aggregations.

**Key Functions:**
- `calculate_simulated_fare()` - Compute fare based on distance/duration
- `add_simulated_fares()` - Add fare columns to dataframe
- `calculate_demand_metrics()` - Hourly, location, and time-period aggregations
- `estimate_idle_time()` - Calculate wait times between trips
- `calculate_location_features()` - Location-level feature engineering
- `engineer_features()` - Complete feature pipeline

### 3. **profit_model.py**
Calculates profits and generates recommendations.

**Key Classes:**
- `ProfitCalculator` - Main calculation engine

**Key Methods:**
- `calculate_driver_profit()` - Profit for time/location/surge combo
- `get_best_hours_for_location()` - Top earning hours
- `get_best_locations_for_hour()` - Top earning locations
- `compare_shifts()` - Compare different shift patterns
- `simulate_what_if()` - Scenario analysis
- `get_optimization_suggestions()` - AI recommendations

### 4. **utils.py**
Utility functions for formatting and visualization.

**Key Functions:**
- `format_currency()` - Format as currency
- `format_time()` - Format minutes to hours/minutes
- `get_earnings_color()` - Color based on earnings level
- `get_hour_label()` - 12-hour format
- `detect_peak_hours()` - Find peak demand periods

### 5. **app.py**
Main Streamlit application orchestrating the dashboard.

**Sections:**
1. Profit Summary Cards
2. Recommendations
3. Best Hours & Locations
4. Demand Heatmap
5. Earnings Trends
6. What-If Analysis
7. Shift Comparison
8. Detailed Analytics
9. Idle Time Analysis

---

## 🎮 Using the Dashboard

### Sidebar Configuration

1. **Select Your Preferred Location**
   - Choose from list of all locations in dataset
   - Analysis will be specific to this location

2. **Working Hours**
   - Set start hour (0-23)
   - Set end hour (0-23)
   - Defines your shift window

3. **Pricing Options**
   - Toggle surge pricing ON/OFF
   - Adjust surge multiplier (1.0 = normal, 2.0 = 2x surge)

4. **Daily Shift Duration**
   - Set how many hours you plan to work
   - Affects earnings projections

### Main Dashboard

**Profit Summary Cards:**
- Shows estimated total earnings
- Hourly rate
- Trip count
- Idle time

**Recommendations:**
- Data-driven suggestions prioritized by impact
- Multiple recommendation types

**Best Hours/Locations:**
- Top performing hours in your location
- Best locations overall
- Interactive charts

**Demand Heatmap:**
- 2D visualization of demand patterns
- Hours vs Locations
- Color intensity = earnings

**Earnings Trends:**
- Hourly trend line
- Daily bar chart
- Identify patterns

**What-If Analysis:**
- See earnings vs surge multiplier
- See earnings vs shift duration
- Interactive exploration

**Shift Comparison:**
- Morning vs Afternoon vs Evening vs Night
- Total earnings and hourly rate
- Detailed metrics table

**Analytics:**
- 3 tabs: Demand, Location, Time Analysis
- Detailed metrics and rankings

---

## 📈 Expected Output

### Sample Dashboard Metrics

```
💵 Total Earnings: ₹4,200
⏱️ Earnings/Hour: ₹525
🚗 Estimated Trips: 18
⏸️ Idle Time: 4h 30m

🎯 Recommendations:
🔴 Peak earning hour: 18:00-19:00 (Avg earnings: ₹850/trip)
🟡 Weekend shifts are more profitable
🟢 Optimal shift: 8 hours
```

---

## ⚙️ Advanced Features

### 1. **Simulation Engine**
```python
# Example: What-if analysis
scenario_results = calculator.simulate_what_if(
    location='Midtown',
    base_hour_range=(9, 17),
    parameters_to_vary={
        'surge_multiplier': [1.0, 1.5, 2.0],
        'duration_hours': [4, 6, 8]
    }
)
```

### 2. **Shift Comparison**
```python
# Example: Compare shifts
comparison = calculator.compare_shifts(
    'Midtown',
    [
        {'name': 'Morning', 'start_hour': 6, 'end_hour': 14, 'surge_multiplier': 1.2},
        {'name': 'Evening', 'start_hour': 17, 'end_hour': 1, 'surge_multiplier': 1.5}
    ]
)
```

### 3. **Optimization Suggestions**
```python
# Example: Get recommendations
suggestions = calculator.get_optimization_suggestions(
    location='Downtown',
    available_hours_per_week=40
)
```

---

## 🐛 Troubleshooting

### Issue: "Dataset file 'UberDataset.csv' not found"
**Solution:** Ensure `UberDataset.csv` is in the same directory as `app.py`

### Issue: "ModuleNotFoundError"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: Datetime parsing errors
**Solution:** The app handles multiple date formats. Ensure dates are in MM-DD-YYYY or MM/DD/YYYY format

### Issue: Slow performance with large dataset
**Solution:** 
- Use `@st.cache_resource` (already implemented)
- Reduce dataframe size by filtering dates
- Consider aggregating old data

---

## 📊 Data Quality Notes

- **Missing Values:** Handled with median imputation for numeric fields
- **Outliers:** Removed trips > 100 miles or > 480 minutes duration
- **Date Formats:** Automatically detects and parses multiple formats
- **Null Locations:** Dropouts removed from analysis

---

## 🎓 Understanding the Metrics

### Earnings per Hour
- Projected total earnings divided by shift duration
- Higher = better hourly rate
- Target: ₹400-600+ for competitive locations

### Idle Time
- Estimated wait time between consecutive trips
- Affects overall shift efficiency
- Lower = more driving, more earnings opportunity

### Surge Multiplier
- 1.0 = Base fare (normal demand)
- 1.5 = 50% higher fare (high demand)
- 2.0 = 100% higher fare (peak demand)

### Trip Count
- Projected number of trips during shift
- Depends on location demand and time window

---

## 🔐 Production Considerations

For deployment, consider:

1. **Security:** Add authentication if sharing publicly
2. **Scalability:** Use data warehouse for large datasets
3. **Real-time:** Integrate live API for actual demand data
4. **Database:** Store results for historical comparison
5. **Alerts:** Email/SMS notifications for peak hours

---

## 📝 License

This project is provided as-is for educational and analytical purposes.

---

## 👨‍💻 Technical Stack

- **Frontend:** Streamlit 1.28+
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Folium
- **Analysis:** Scikit-learn
- **Backend:** Python 3.8+

---

## 🚀 Future Enhancements

- [ ] Real-time Uber API integration
- [ ] Machine learning demand forecasting
- [ ] Driver comparison/leaderboard
- [ ] Route optimization
- [ ] Weather impact analysis
- [ ] Event-based demand analysis
- [ ] Multi-language support
- [ ] Mobile app version

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the module documentation
3. Inspect the data preprocessing logs

---

## 🎯 Summary

This dashboard provides Uber drivers with:
- **Data-driven insights** into when and where to drive
- **Profit projections** based on historical patterns
- **Scenario analysis** for decision-making
- **Optimization recommendations** for maximizing earnings

By leveraging historical trip data and intelligent analysis, drivers can make informed decisions to significantly improve their profitability. 💰

---

**Happy driving! 🚗💨**
