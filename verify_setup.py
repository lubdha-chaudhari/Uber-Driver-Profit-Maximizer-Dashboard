"""
VERIFICATION CHECKLIST - Uber Driver Profit Maximizer Dashboard

Run this to verify all components are working correctly.
"""

import os
import sys

def check_files():
    """Check if all required files exist."""
    print("\n" + "="*60)
    print("FILE VERIFICATION")
    print("="*60)
    
    required_files = {
        'Core Application': [
            'app.py',
            'data_preprocessing.py',
            'feature_engineering.py',
            'profit_model.py',
            'utils.py'
        ],
        'Configuration': [
            'requirements.txt',
            'setup.bat',
            'setup.sh'
        ],
        'Documentation': [
            'README.md',
            'QUICKSTART.md',
            'ARCHITECTURE.md',
            'USAGE_GUIDE.md',
            'PROJECT_SUMMARY.md'
        ],
        'Testing & Data': [
            'test_pipeline.py',
            'UberDataset.csv'
        ]
    }
    
    all_present = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for filename in files:
            exists = os.path.exists(filename)
            status = "✅" if exists else "❌"
            print(f"  {status} {filename}")
            if not exists:
                all_present = False
    
    return all_present


def check_imports():
    """Check if all modules can be imported."""
    print("\n" + "="*60)
    print("IMPORT VERIFICATION")
    print("="*60)
    
    modules = {
        'data_preprocessing': ['preprocess_data', 'parse_datetime_columns'],
        'feature_engineering': ['engineer_features', 'calculate_simulated_fare'],
        'profit_model': ['create_profit_calculator', 'ProfitCalculator'],
        'utils': ['format_currency', 'create_metadata']
    }
    
    all_importable = True
    for module_name, functions in modules.items():
        try:
            module = __import__(module_name)
            status = "✅"
            print(f"\n{status} {module_name}")
            for func in functions:
                try:
                    getattr(module, func)
                    print(f"    ✅ {func}")
                except AttributeError:
                    print(f"    ❌ {func}")
                    all_importable = False
        except ImportError as e:
            print(f"\n❌ {module_name}: {str(e)}")
            all_importable = False
    
    return all_importable


def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "="*60)
    print("DEPENDENCY VERIFICATION")
    print("="*60)
    
    dependencies = {
        'streamlit': '1.28+',
        'pandas': '2.0+',
        'numpy': '1.24+',
        'plotly': '5.16+',
        'scikit-learn': '1.3+',
        'pytz': 'any',
        'python-dateutil': 'any',
        'folium': 'any',
        'streamlit-folium': 'any'
    }
    
    print("\nChecking installed packages:")
    all_installed = True
    for package in dependencies.keys():
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_data():
    """Check if dataset exists and has data."""
    print("\n" + "="*60)
    print("DATA VERIFICATION")
    print("="*60)
    
    import pandas as pd
    
    if not os.path.exists('UberDataset.csv'):
        print("  ❌ UberDataset.csv not found")
        return False
    
    try:
        df = pd.read_csv('UberDataset.csv')
        print(f"  ✅ Dataset found")
        print(f"  ✅ Records: {len(df)}")
        print(f"  ✅ Columns: {len(df.columns)}")
        
        required_cols = ['START_DATE', 'END_DATE', 'START', 'STOP', 'MILES']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            print(f"  ❌ Missing columns: {missing}")
            return False
        else:
            print(f"  ✅ All required columns present")
            return True
    except Exception as e:
        print(f"  ❌ Error reading dataset: {str(e)}")
        return False


def check_documentation():
    """Check if all documentation files exist."""
    print("\n" + "="*60)
    print("DOCUMENTATION VERIFICATION")
    print("="*60)
    
    docs = {
        'README.md': 'Technical documentation',
        'QUICKSTART.md': 'Quick start guide',
        'ARCHITECTURE.md': 'System architecture',
        'USAGE_GUIDE.md': 'Usage scenarios',
        'PROJECT_SUMMARY.md': 'Project summary'
    }
    
    all_present = True
    for filename, description in docs.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename} ({size:,} bytes)")
        else:
            print(f"  ❌ {filename} - {description}")
            all_present = False
    
    return all_present


def main():
    """Run all verification checks."""
    print("\n" + "="*60)
    print("UBER DRIVER PROFIT MAXIMIZER - VERIFICATION")
    print("="*60)
    
    checks = [
        ("Files", check_files),
        ("Dependencies", check_dependencies),
        ("Data", check_data),
        ("Imports", check_imports),
        ("Documentation", check_documentation)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error in {name} check: {str(e)}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - READY TO USE!")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Open: http://localhost:8501")
        print("  3. Explore: Try different locations and hours")
        print("\nFor help:")
        print("  - Read: QUICKSTART.md (5-minute setup)")
        print("  - Read: USAGE_GUIDE.md (real-world scenarios)")
        print("  - Read: README.md (comprehensive guide)")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nTo fix:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Check file structure: All files should be in same directory")
        print("  3. Verify data: UberDataset.csv must be present")
        print("  4. Rerun verification: python verify_setup.py")
    
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
