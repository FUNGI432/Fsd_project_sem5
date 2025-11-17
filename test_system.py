#!/usr/bin/env python3
"""
Test script for the AI-Based Question Paper Moderation System
This script demonstrates the functionality without requiring installation
"""

import sys
import os

# Add the project directory to the path so we can import qpaper_mod
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from qpaper_mod import QuestionPaperModerator
    
    def test_system():
        """Test the question paper moderation system with sample data"""
        print("Testing AI-Based Question Paper Moderation System")
        print("=" * 50)
        
        # Create sample questions
        sample_questions = [
            "Define the term photosynthesis and explain its importance in the ecosystem.",
            "List the main components of a computer system.",
            "Describe the process of cell division in plants.",
            "Analyze the impact of climate change on biodiversity in tropical rainforests.",
            "Evaluate the effectiveness of renewable energy sources compared to fossil fuels.",
            "Create a hypothesis explaining the relationship between temperature and enzyme activity.",
            "Solve the quadratic equation: x² - 5x + 6 = 0.",
            "Explain the concept of supply and demand in economics.",
            "Identify the major causes of World War I.",
            "Discuss the role of DNA in heredity."
        ]
        
        print(f"Processing {len(sample_questions)} sample questions...\n")
        
        # Initialize the moderator
        moderator = QuestionPaperModerator()
        
        # Process questions
        results = moderator.process_questions(sample_questions)
        
        # Generate report
        report_file = moderator.generate_report(results, "test_report.txt")
        
        # Generate suggestions
        suggestions = moderator.suggest_improvements(results)
        
        print(f"\nSuggestions available: {len(suggestions)}")
        for i, suggestion in enumerate(suggestions[:5], 1):  # Show first 5 suggestions
            print(f"{i}. {suggestion['message']}")
            
        if len(suggestions) > 5:
            print(f"... and {len(suggestions) - 5} more suggestions")
        
        print("\nSummary:")
        for level, count in results["blooms_distribution"].items():
            print(f"- {level}: {count} questions")
        
        underrepresented = [level for level, count in results["blooms_distribution"].items() 
                          if count == 0]
        if underrepresented:
            print(f"Recommendation: Add questions for {', '.join(underrepresented)} levels")
        
        print(f"\nDetailed report saved to: {report_file}")
        return True
        
    if __name__ == "__main__":
        test_system()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("This test requires the qpaper_mod.py file to be present in the same directory.")
except Exception as e:
    print(f"Error running test: {e}")