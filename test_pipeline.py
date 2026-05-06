"""Quick test script to validate all modules work correctly."""

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

from data_preprocessing import preprocess_data
from feature_engineering import engineer_features
from profit_model import create_profit_calculator

print("\n" + "="*60)
print("TESTING COMPLETE UBER PROFIT MAXIMIZER PIPELINE")
print("="*60 + "\n")

try:
    print("1️⃣ Loading and preprocessing data...")
    df = preprocess_data("UberDataset.csv")
    print(f"   ✓ Loaded {len(df)} records")
    print(f"   ✓ Date range: {df['START_DATE'].min()} to {df['START_DATE'].max()}")
    
    print("\n2️⃣ Engineering features...")
    features = engineer_features(df)
    print(f"   ✓ Processed {len(features['dataframe'])} records")
    print(f"   ✓ {len(features['location_features'])} unique locations found")
    
    print("\n3️⃣ Creating profit calculator...")
    calc = create_profit_calculator(features)
    print(f"   ✓ Calculator initialized successfully")
    
    print("\n4️⃣ Testing profit calculations...")
    locations = features['location_features'].index.tolist()[:3]
    for location in locations:
        result = calc.calculate_driver_profit((9, 17), location)
        print(f"   • {location}: ₹{result['projected_earnings_full_shift']:.0f} (₹{result['earnings_per_hour']:.0f}/hr)")
    
    print("\n5️⃣ Testing recommendations engine...")
    suggestions = calc.get_optimization_suggestions(locations[0])
    print(f"   ✓ Generated {len(suggestions['recommendations'])} recommendations")
    
    print("\n6️⃣ Testing shift comparison...")
    shifts = [
        {'name': 'Morning', 'start_hour': 6, 'end_hour': 14, 'surge_multiplier': 1.0},
        {'name': 'Evening', 'start_hour': 17, 'end_hour': 1, 'surge_multiplier': 1.5}
    ]
    comparison = calc.compare_shifts(locations[0], shifts)
    print(f"   ✓ Compared {len(comparison)} shift scenarios")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED - APPLICATION READY!")
    print("="*60)
    print("\nTo run the dashboard, execute:")
    print("   streamlit run app.py")
    print("\nThen navigate to http://localhost:8501")
    print("\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
