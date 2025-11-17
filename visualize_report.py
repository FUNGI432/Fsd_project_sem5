#!/usr/bin/env python3
"""
Visualization script for the AI-Based Question Paper Moderation System
Creates simple ASCII charts for better understanding of distributions
"""

import sys
import os

# Add the project directory to the path so we can import qpaper_mod
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from qpaper_mod import QuestionPaperModerator
    
    def create_bar_chart(data, title, max_width=50):
        """Create a simple ASCII bar chart"""
        if not data:
            return ""
            
        max_value = max(data.values())
        if max_value == 0:
            max_value = 1
            
        chart = f"\n{title}\n"
        chart += "=" * len(title) + "\n"
        
        for label, value in data.items():
            bar_length = int((value / max_value) * max_width)
            bar = "█" * bar_length
            chart += f"{label:15}: {bar} {value}\n"
            
        return chart
    
    def visualize_report(report_file="report_summary.txt"):
        """Visualize the report data with ASCII charts"""
        print("AI-Based Question Paper Moderation System - Visualization")
        print("=" * 60)
        
        # Read the report file
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Report file '{report_file}' not found.")
            return False
        except Exception as e:
            print(f"Error reading report file: {e}")
            return False
            
        # Parse the report data
        blooms_data = {}
        difficulty_data = {}
        parsing_blooms = False
        parsing_difficulty = False
        
        for line in lines:
            line = line.strip()
            if line == "Bloom's Taxonomy Distribution:":
                parsing_blooms = True
                parsing_difficulty = False
                continue
            elif line == "Difficulty Distribution:":
                parsing_blooms = False
                parsing_difficulty = True
                continue
            elif line.startswith("- ") and parsing_blooms:
                # Parse Bloom's level data
                parts = line[2:].split(": ")
                if len(parts) >= 2:
                    level = parts[0]
                    count_part = parts[1].split(" ")[0]
                    try:
                        count = int(count_part)
                        blooms_data[level] = count
                    except ValueError:
                        pass
            elif line.startswith("- ") and parsing_difficulty:
                # Parse difficulty data
                parts = line[2:].split(": ")
                if len(parts) >= 2:
                    level = parts[0]
                    count_part = parts[1].split(" ")[0]
                    try:
                        count = int(count_part)
                        difficulty_data[level] = count
                    except ValueError:
                        pass
            elif line.startswith("Recommendations:") or line.startswith("Ambiguous Questions Detected:"):
                parsing_blooms = False
                parsing_difficulty = False
        
        # Create visualizations
        print(create_bar_chart(blooms_data, "Bloom's Taxonomy Distribution"))
        print(create_bar_chart(difficulty_data, "Difficulty Distribution"))
        
        # Show recommendations
        print("\nKey Recommendations:")
        print("-" * 20)
        recommendations_found = False
        in_recommendations = False
        
        for line in lines:
            line = line.strip()
            if line == "Recommendations:":
                in_recommendations = True
                continue
            elif in_recommendations and line.startswith("- "):
                print(line)
                recommendations_found = True
            elif in_recommendations and (line.startswith("Ambiguous Questions Detected:") or 
                                        line.startswith("Report Generated:")):
                break
                
        if not recommendations_found:
            print("No major recommendations. The question paper looks well-balanced!")
            
        print(f"\nDetailed report: {report_file}")
        return True
    
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            visualize_report(sys.argv[1])
        else:
            visualize_report()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("This visualization script requires the qpaper_mod.py file to be present.")
except Exception as e:
    print(f"Error running visualization: {e}")