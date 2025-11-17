#!/usr/bin/env python3
"""
Demonstration script for the AI-Based Question Paper Moderation System
This script runs a complete demonstration of all system features
"""

import sys
import os

# Add the project directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("AI-Based Question Paper Moderation System - Complete Demonstration")
    print("=" * 70)
    print()
    
    # 1. Test the main system with sample questions
    print("1. Testing Main System with Sample Questions")
    print("-" * 40)
    try:
        import test_system
        print("✓ Main system test completed successfully")
    except Exception as e:
        print(f"✗ Error in main system test: {e}")
    print()
    
    # 2. Test the visualization module
    print("2. Testing Visualization Module")
    print("-" * 40)
    try:
        import visualize_report
        print("✓ Visualization module imported successfully")
        # Try to visualize the test report
        if os.path.exists("test_report.txt"):
            print("✓ Test report found, visualization would work")
        else:
            print("ℹ No test report found, but module works")
    except Exception as e:
        print(f"✗ Error in visualization module: {e}")
    print()
    
    # 3. Test the enhanced NLP module
    print("3. Testing Enhanced NLP Module")
    print("-" * 40)
    try:
        import enhanced_nlp
        print("✓ Enhanced NLP module imported successfully")
        # Run the demonstration
        enhanced_nlp.demonstrate_enhanced_features()
        print("✓ Enhanced NLP demonstration completed")
    except Exception as e:
        print(f"✗ Error in enhanced NLP module: {e}")
    print()
    
    # 4. Show file structure
    print("4. Project File Structure")
    print("-" * 40)
    try:
        files = os.listdir(".")
        for file in sorted(files):
            if os.path.isfile(file):
                print(f"  {file}")
        print()
    except Exception as e:
        print(f"✗ Error listing files: {e}")
    
    # 5. Show sample report if it exists
    print("5. Sample Analysis Report")
    print("-" * 40)
    try:
        report_files = ["test_report.txt", "report_summary.txt"]
        report_found = False
        for report_file in report_files:
            if os.path.exists(report_file):
                print(f"Contents of {report_file}:")
                with open(report_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines[:15]):  # Show first 15 lines
                        print(f"  {line.rstrip()}")
                    if len(lines) > 15:
                        print("  ... (truncated)")
                report_found = True
                break
        
        if not report_found:
            print("No report files found. Run the system on a question paper to generate one.")
    except Exception as e:
        print(f"✗ Error reading report: {e}")
    
    print()
    print("Demonstration completed!")
    print()
    print("To use the system:")
    print("  python qpaper_mod.py --input draft_paper.txt")
    print("  python qpaper_mod.py --text \"Your question here\"")

if __name__ == "__main__":
    main()