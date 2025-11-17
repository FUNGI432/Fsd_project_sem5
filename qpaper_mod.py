#!/usr/bin/env python3
"""
AI-Based Question Paper Moderation System
CLI interface for analyzing question papers against Bloom's Taxonomy
"""

import argparse
import sys
import os
import json
from typing import List, Dict, Tuple
from datetime import datetime

import argparse
import sys
import os
from typing import List, Dict, Tuple


class QuestionPaperModerator:
    """Main class for moderating question papers using AI analysis."""
    
    def __init__(self):
        # Bloom's Taxonomy levels
        self.blooms_levels = [
            "Knowledge", "Comprehension", "Application", 
            "Analysis", "Synthesis", "Evaluation"
        ]
        
        # Sample keywords for difficulty estimation (would be expanded with ML models)
        self.difficulty_keywords = {
            "easy": ["define", "list", "identify", "recall", "name"],
            "medium": ["explain", "describe", "compare", "discuss", "summarize"],
            "hard": ["analyze", "evaluate", "critique", "justify", "assess"]
        }
        
        # Ambiguity indicators
        self.ambiguity_indicators = [
            "etc.", "and so on", "various", "several", "many",
            "some cases", "sometimes", "possibly", "maybe"
        ]
    
    def read_question_paper(self, file_path: str) -> List[str]:
        """Read questions from a file, one question per line."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                questions = [line.strip() for line in f.readlines() if line.strip()]
            return questions
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    def classify_blooms_level(self, question: str) -> str:
        """
        Classify a question according to Bloom's Taxonomy.
        In a full implementation, this would use NLP models.
        """
        question_lower = question.lower()
        
        # Simple keyword-based classification (would be replaced with ML models)
        if any(word in question_lower for word in ["analyze", "compare", "contrast", "distinguish"]):
            return "Analysis"
        elif any(word in question_lower for word in ["create", "design", "compose", "construct"]):
            return "Synthesis"
        elif any(word in question_lower for word in ["evaluate", "judge", "criticize", "justify", "assess"]):
            return "Evaluation"
        elif any(word in question_lower for word in ["apply", "solve", "use", "demonstrate", "calculate"]):
            return "Application"
        elif any(word in question_lower for word in ["explain", "describe", "discuss", "interpret"]):
            return "Comprehension"
        else:
            return "Knowledge"  # Default to Knowledge level
    
    def estimate_difficulty(self, question: str) -> str:
        """Estimate question difficulty based on keywords."""
        question_lower = question.lower()
        
        hard_count = sum(1 for word in self.difficulty_keywords["hard"] if word in question_lower)
        medium_count = sum(1 for word in self.difficulty_keywords["medium"] if word in question_lower)
        easy_count = sum(1 for word in self.difficulty_keywords["easy"] if word in question_lower)
        
        if hard_count > medium_count and hard_count > easy_count:
            return "Hard"
        elif medium_count > easy_count:
            return "Medium"
        else:
            return "Easy"
    
    def detect_ambiguity(self, question: str) -> Tuple[bool, List[str]]:
        """Detect ambiguous phrasing in questions."""
        found_indicators = []
        question_lower = question.lower()
        
        for indicator in self.ambiguity_indicators:
            if indicator in question_lower:
                found_indicators.append(indicator)
        
        return len(found_indicators) > 0, found_indicators
    
    def process_questions(self, questions: List[str]) -> Dict:
        """Process all questions and generate analysis."""
        results = {
            "total_questions": len(questions),
            "blooms_distribution": {level: 0 for level in self.blooms_levels},
            "difficulty_distribution": {"Easy": 0, "Medium": 0, "Hard": 0},
            "ambiguous_questions": [],
            "question_details": []
        }
        
        for i, question in enumerate(questions, 1):
            print(f"Processing question {i}/{len(questions)}: Analyzing...")
            
            # Classify Bloom's level
            blooms_level = self.classify_blooms_level(question)
            results["blooms_distribution"][blooms_level] += 1
            
            # Estimate difficulty
            difficulty = self.estimate_difficulty(question)
            results["difficulty_distribution"][difficulty] += 1
            
            # Check for ambiguity
            is_ambiguous, indicators = self.detect_ambiguity(question)
            if is_ambiguous:
                results["ambiguous_questions"].append({
                    "question_number": i,
                    "question": question,
                    "indicators": indicators
                })
            
            # Store question details
            results["question_details"].append({
                "number": i,
                "text": question,
                "blooms_level": blooms_level,
                "difficulty": difficulty,
                "ambiguous": is_ambiguous
            })
            
            # Print interim results
            print(f"Cognitive Level: {blooms_level}")
            print(f"Difficulty: {difficulty}")
            print(f"Ambiguity: {'High' if is_ambiguous else 'Low'}")
            print("-" * 40)
        
        return results
    
    def generate_report(self, results: Dict, output_file: str = "report_summary.txt"):
        """Generate a summary report of the analysis."""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("AI-Based Question Paper Moderation Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Questions: {results['total_questions']}\n\n")
            
            f.write("Bloom's Taxonomy Distribution:\n")
            for level, count in results["blooms_distribution"].items():
                percentage = (count / results['total_questions']) * 100 if results['total_questions'] > 0 else 0
                f.write(f"- {level}: {count} questions ({percentage:.1f}%)\n")
            f.write("\n")
            
            f.write("Difficulty Distribution:\n")
            for level, count in results["difficulty_distribution"].items():
                percentage = (count / results['total_questions']) * 100 if results['total_questions'] > 0 else 0
                f.write(f"- {level}: {count} questions ({percentage:.1f}%)\n")
            f.write("\n")
            
            if results["ambiguous_questions"]:
                f.write("Ambiguous Questions Detected:\n")
                for item in results["ambiguous_questions"]:
                    f.write(f"- Q{item['question_number']}: {item['question']}\n")
                    f.write(f"  Indicators: {', '.join(item['indicators'])}\n")
                f.write("\n")
            
            # Generate recommendations
            f.write("Recommendations:\n")
            underrepresented = [level for level, count in results["blooms_distribution"].items() 
                              if count == 0]
            if underrepresented:
                f.write(f"- No questions targeting '{', '.join(underrepresented)}' level(s). Consider adding questions that require these skills.\n")
            
            low_representation = [level for level, count in results["blooms_distribution"].items() 
                                if 0 < count < max(1, results['total_questions'] * 0.1)]
            if low_representation:
                f.write(f"- Low representation of '{', '.join(low_representation)}' level questions. Consider adding more questions at these levels.\n")
            
            # Check difficulty balance
            diff_counts = results["difficulty_distribution"]
            total = sum(diff_counts.values())
            if total > 0:
                for level in ["Easy", "Medium", "Hard"]:
                    percentage = (diff_counts[level] / total) * 100
                    if percentage < 20:
                        f.write(f"- Only {percentage:.1f}% of questions are '{level}' difficulty. Consider adding more {level.lower()} questions for better balance.\n")
            
            f.write("\n")
        
        print(f"Report generated: {output_file}")
        return output_file
    
    def suggest_improvements(self, results: Dict) -> List[Dict]:
        """Generate suggestions for improving the question paper."""
        suggestions = []
        
        # Check for underrepresented Bloom's levels
        for level, count in results["blooms_distribution"].items():
            if count == 0:
                suggestions.append({
                    "type": "missing_level",
                    "message": f"No questions targeting '{level}' level. Consider adding questions that require {level.lower()} skills.",
                    "level": level
                })
            elif count < results['total_questions'] * 0.1:
                suggestions.append({
                    "type": "low_representation",
                    "message": f"Low representation of '{level}' level questions ({count}/{results['total_questions']}). Consider adding more questions at this level.",
                    "level": level
                })
        
        # Suggest improvements for ambiguous questions
        for item in results["ambiguous_questions"]:
            suggestions.append({
                "type": "ambiguity",
                "message": f"Question {item['question_number']} contains ambiguous phrasing: '{', '.join(item['indicators'])}'. Consider rephrasing for clarity.",
                "question_number": item['question_number']
            })
        
        # Balance difficulty distribution
        diff_counts = results["difficulty_distribution"]
        total = sum(diff_counts.values())
        if total > 0:
            for level in ["Easy", "Medium", "Hard"]:
                percentage = (diff_counts[level] / total) * 100
                if percentage < 20:
                    suggestions.append({
                        "type": "difficulty_balance",
                        "message": f"Only {percentage:.1f}% of questions are '{level}' difficulty. Consider adding more {level.lower()} questions for better balance.",
                        "level": level
                    })
        
        return suggestions
    
    def collect_feedback(self, suggestions: List[Dict]) -> List[Dict]:
        """Collect user feedback on suggestions."""
        feedback = []
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion['message']}")
            
            # In a real implementation, we would collect actual user input
            # For now, we'll simulate acceptance of all suggestions
            response = input("Accept this suggestion? (y/n/skip): ").strip().lower()
            
            if response in ['y', 'yes']:
                feedback.append({
                    "suggestion_id": i,
                    "suggestion": suggestion,
                    "accepted": True,
                    "feedback": "Accepted"
                })
            elif response in ['n', 'no']:
                feedback.append({
                    "suggestion_id": i,
                    "suggestion": suggestion,
                    "accepted": False,
                    "feedback": input("Please provide feedback on why this suggestion was rejected: ").strip()
                })
            else:  # skip
                feedback.append({
                    "suggestion_id": i,
                    "suggestion": suggestion,
                    "accepted": None,
                    "feedback": "Skipped"
                })
        
        return feedback
    
    def save_feedback(self, feedback: List[Dict], filename: str = "feedback.json"):
        """Save user feedback to a JSON file for future model improvement."""
        try:
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(feedback, f, indent=2, ensure_ascii=False)
            print(f"Feedback saved to {filename}")
        except Exception as e:
            print(f"Error saving feedback: {e}")
    
    def run_interactive_session(self, questions: List[str]):
        """Run an interactive session for processing questions."""
        results = self.process_questions(questions)
        report_file = self.generate_report(results)
        suggestions = self.suggest_improvements(results)
        
        print(f"\nSuggestions available: {len(suggestions)}")
        
        # Collect feedback (commented out for non-interactive environments)
        # feedback = self.collect_feedback(suggestions)
        # self.save_feedback(feedback, f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Display suggestions without collecting feedback for demo purposes
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['message']}")
        
        print("\nSummary:")
        for level, count in results["blooms_distribution"].items():
            print(f"- {level}: {count} questions")
        
        underrepresented = [level for level, count in results["blooms_distribution"].items() 
                          if count == 0]
        if underrepresented:
            print(f"Recommendation: Add questions for {', '.join(underrepresented)} levels")
        
        return results, suggestions


def main():
    parser = argparse.ArgumentParser(description="AI-Based Question Paper Moderation System")
    parser.add_argument("--input", "-i", help="Input file containing questions (one per line)")
    parser.add_argument("--text", "-t", help="Direct text input for a single question")
    
    args = parser.parse_args()
    
    moderator = QuestionPaperModerator()
    
    if args.input:
        questions = moderator.read_question_paper(args.input)
        if not questions:
            print("No questions found in the input file.")
            sys.exit(1)
    elif args.text:
        questions = [args.text]
    else:
        parser.print_help()
        sys.exit(1)
    
    moderator.run_interactive_session(questions)


if __name__ == "__main__":
    main()