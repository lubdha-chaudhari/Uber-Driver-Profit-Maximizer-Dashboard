# 🚀 QUICK START GUIDE - Uber Driver Profit Maximizer Dashboard

## 5-Minute Setup

### For Windows Users 🪟

1. **Open Command Prompt/PowerShell** in the project directory

2. **Run the setup script:**
   ```bash
   setup.bat
   ```

3. **Start the dashboard:**
   ```bash
   venv\Scripts\activate.bat
   streamlit run app.py
   ```

4. **Open browser:** Navigate to `http://localhost:8501`

---

### For macOS/Linux Users 🍎🐧

1. **Open Terminal** in the project directory

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the dashboard:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

4. **Open browser:** Navigate to `http://localhost:8501`

---

## Manual Installation (If Scripts Don't Work)

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Tests
```bash
python test_pipeline.py
```

### Step 4: Launch Dashboard
```bash
streamlit run app.py
```

---

## 🎯 First Steps with the Dashboard

1. **Sidebar Configuration**
   - Select your preferred location
   - Set working hours (e.g., 9 AM - 5 PM)
   - Toggle surge pricing
   - Set daily shift duration

2. **View Results**
   - Check profit summary cards
   - Read personalized recommendations
   - Explore demand heatmap
   - Analyze earnings trends

3. **Experiment**
   - Try "What-If" scenarios
   - Compare different shifts
   - Check best hours/locations
   - Review idle time analysis

---

## 📊 Understanding the Dashboard

### Profit Summary (Top)
- **Total Earnings**: Your projected daily earnings
- **Earnings/Hour**: Average hourly rate
- **Estimated Trips**: Number of trips projected
- **Idle Time**: Waiting time between trips

### Recommendations Section
- **🔴 HIGH**: Critical for maximizing earnings
- **🟡 MEDIUM**: Good to implement
- **🟢 LOW**: Optional optimizations

### Charts & Visualizations
- **Demand Heatmap**: See where/when to earn most
- **Earnings Trends**: Identify patterns
- **Shift Comparison**: Morning vs Evening profitability

---

## 🧪 Verify Installation

Run the test to confirm everything works:
```bash
python test_pipeline.py
```

Expected output:
```
✅ ALL TESTS PASSED - APPLICATION READY!

To run the dashboard, execute:
   streamlit run app.py
```

---

## ⚠️ Common Issues & Solutions

### Issue: "Module not found" error
**Solution:** Make sure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### Issue: Port 8501 already in use
**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow performance
**Solution:** 
- Close other applications
- Reduce browser tabs
- Streamlit caches data, first load takes 10-15 seconds

### Issue: Data not loading
**Solution:** 
- Ensure `UberDataset.csv` is in the same directory as `app.py`
- Run `python test_pipeline.py` to diagnose

---

## 📱 Using the Dashboard

### Change Location
- Use sidebar dropdown to select different locations
- Dashboard updates instantly

### Adjust Working Hours
- Drag sliders to set start/end hours
- See how earnings change in real-time

### Toggle Surge Pricing
- Turn on to simulate surge multiplier
- Adjust multiplier (1.0 to 2.0x)
- See impact on earnings

### Explore What-If Scenarios
- Adjust shift duration
- Vary surge multiplier
- See instant projections

---

## 💾 File Structure
```
uber/
├── app.py                      # Main dashboard
├── data_preprocessing.py        # Data loading
├── feature_engineering.py       # Feature creation
├── profit_model.py              # Calculations
├── utils.py                     # Helper functions
├── test_pipeline.py             # Validation script
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── QUICKSTART.md               # This file
├── setup.bat                   # Windows setup
├── setup.sh                    # macOS/Linux setup
└── UberDataset.csv             # Your data
```

---

## 🚀 Next Steps

1. **Explore the data** - Check different locations and hours
2. **Run simulations** - Test different working patterns
3. **Get recommendations** - Follow AI suggestions
4. **Optimize your schedule** - Use insights to maximize earnings

---

## 💬 Support

- Check README.md for detailed documentation
- Review inline code comments in each module
- Run test_pipeline.py to verify setup

---

## 🎉 Ready to Maximize Your Earnings!

The dashboard is now ready. Start earning smarter! 💰

**Happy driving! 🚗**
