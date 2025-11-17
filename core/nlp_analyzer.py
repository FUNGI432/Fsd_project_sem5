#!/usr/bin/env python3
"""
Enhanced NLP Analyzer for Question Paper Moderation
Production-ready implementation with advanced analysis capabilities
"""

from typing import List, Dict, Tuple
import re
from datetime import datetime


class NLPAnalyzer:
    """Advanced NLP analyzer for question classification and analysis"""
    
    def __init__(self):
        """Initialize the analyzer with keyword mappings and patterns"""
        
        # Bloom's Taxonomy keyword mappings
        self.blooms_keywords = {
            "Knowledge": [
                "define", "list", "identify", "recall", "name", "label", "match",
                "state", "describe", "relate", "outline", "who", "what", "when", "where"
            ],
            "Comprehension": [
                "explain", "describe", "discuss", "interpret", "summarize", "classify",
                "paraphrase", "illustrate", "translate", "recognize", "express", "why", "how"
            ],
            "Application": [
                "apply", "solve", "use", "demonstrate", "calculate", "illustrate",
                "show", "complete", "examine", "modify", "relate", "change", "discover"
            ],
            "Analysis": [
                "analyze", "compare", "contrast", "distinguish", "examine", "investigate",
                "categorize", "differentiate", "separate", "infer", "arrange", "relationship"
            ],
            "Synthesis": [
                "create", "design", "compose", "construct", "formulate", "propose",
                "develop", "integrate", "combine", "compile", "devise", "generate", "hypothesize"
            ],
            "Evaluation": [
                "evaluate", "judge", "criticize", "justify", "assess", "appraise",
                "argue", "defend", "support", "value", "critique", "weigh", "recommend"
            ]
        }
        
        # Difficulty indicators
        self.difficulty_keywords = {
            "Easy": [
                "define", "list", "identify", "recall", "name", "what is", "who is",
                "label", "match", "choose", "find", "show", "spell", "tell"
            ],
            "Medium": [
                "explain", "describe", "compare", "discuss", "why", "how",
                "summarize", "interpret", "classify", "estimate", "organize"
            ],
            "Hard": [
                "analyze", "evaluate", "justify", "assess", "critique", "hypothesize",
                "synthesize", "design", "compose", "create", "prove", "formulate"
            ]
        }
        
        # Ambiguity indicators
        self.ambiguity_patterns = [
            "etc.", "and so on", "various", "several", "many", "some",
            "sometimes", "possibly", "maybe", "approximately", "about",
            "often", "usually", "generally", "mostly", "rarely"
        ]
        
        # Question quality indicators
        self.quality_issues = [
            ("double negative", r"\b(not\s+un|not\s+in|never\s+un|never\s+in)"),
            ("leading question", r"\b(wouldn't you|don't you think|isn't it true)"),
            ("complex sentence", r"[,;]{3,}"),  # Multiple clauses
            ("vague pronoun", r"\b(it|they|them|this|that)\b(?!\s+\w+\s+(is|are|was|were))"),
        ]
    
    def analyze_questions(self, questions: List[str]) -> Dict:
        """
        Analyze a list of questions comprehensively
        
        Args:
            questions: List of question strings
            
        Returns:
            Dictionary containing complete analysis results
        """
        results = {
            "total_questions": len(questions),
            "blooms_distribution": {level: 0 for level in self.blooms_keywords.keys()},
            "difficulty_distribution": {"Easy": 0, "Medium": 0, "Hard": 0},
            "ambiguous_questions": [],
            "quality_issues": [],
            "question_details": []
        }
        
        for i, question in enumerate(questions, 1):
            # Classify Bloom's level
            blooms_level = self._classify_blooms_level(question)
            results["blooms_distribution"][blooms_level] += 1
            
            # Estimate difficulty
            difficulty = self._estimate_difficulty(question)
            results["difficulty_distribution"][difficulty] += 1
            
            # Check for ambiguity
            is_ambiguous, indicators = self._detect_ambiguity(question)
            if is_ambiguous:
                results["ambiguous_questions"].append({
                    "question_number": i,
                    "question": question,
                    "indicators": indicators
                })
            
            # Check quality issues
            issues = self._check_quality_issues(question)
            if issues:
                results["quality_issues"].append({
                    "question_number": i,
                    "question": question,
                    "issues": issues
                })
            
            # Calculate cognitive load
            cognitive_load = self._estimate_cognitive_load(question)
            
            # Store question details
            results["question_details"].append({
                "number": i,
                "text": question,
                "blooms_level": blooms_level,
                "difficulty": difficulty,
                "ambiguous": is_ambiguous,
                "cognitive_load": cognitive_load,
                "word_count": len(question.split()),
                "quality_score": self._calculate_question_score(question, is_ambiguous, issues)
            })
        
        return results
    
    def _classify_blooms_level(self, question: str) -> str:
        """Classify question according to Bloom's Taxonomy"""
        question_lower = question.lower()
        scores = {level: 0 for level in self.blooms_keywords.keys()}
        
        # Score based on keyword presence
        for level, keywords in self.blooms_keywords.items():
            for keyword in keywords:
                if f" {keyword} " in f" {question_lower} " or question_lower.startswith(keyword):
                    scores[level] += 1
        
        # Return level with highest score, default to Knowledge
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=lambda x: scores[x])
        return "Knowledge"
    
    def _estimate_difficulty(self, question: str) -> str:
        """Estimate question difficulty"""
        question_lower = question.lower()
        scores = {"Easy": 0, "Medium": 0, "Hard": 0}
        
        for level, keywords in self.difficulty_keywords.items():
            for keyword in keywords:
                if keyword in question_lower:
                    scores[level] += 1
        
        # Consider question length as well
        word_count = len(question.split())
        if word_count > 20:
            scores["Hard"] += 1
        elif word_count > 10:
            scores["Medium"] += 1
        else:
            scores["Easy"] += 1
        
        # Return difficulty with highest score
        return max(scores, key=lambda x: scores[x])
    
    def _detect_ambiguity(self, question: str) -> Tuple[bool, List[str]]:
        """Detect ambiguous phrasing"""
        found_indicators = []
        question_lower = question.lower()
        
        for indicator in self.ambiguity_patterns:
            if indicator in question_lower:
                found_indicators.append(indicator)
        
        return len(found_indicators) > 0, found_indicators
    
    def _check_quality_issues(self, question: str) -> List[str]:
        """Check for common question quality issues"""
        issues = []
        question_lower = question.lower()
        
        for issue_name, pattern in self.quality_issues:
            if re.search(pattern, question_lower):
                issues.append(issue_name)
        
        return issues
    
    def _estimate_cognitive_load(self, question: str) -> float:
        """Estimate cognitive load required"""
        word_count = len(question.split())
        complexity_keywords = ["analyze", "evaluate", "compare", "contrast", "synthesize"]
        
        base_load = word_count / 10.0
        complexity_factor = sum(1 for word in complexity_keywords if word in question.lower())
        
        return min(base_load + complexity_factor, 10.0)
    
    def _calculate_question_score(self, question: str, is_ambiguous: bool, issues: List[str]) -> float:
        """Calculate overall quality score for a question"""
        score = 100.0
        
        # Deduct for ambiguity
        if is_ambiguous:
            score -= 20.0
        
        # Deduct for quality issues
        score -= len(issues) * 10.0
        
        # Deduct for very short or very long questions
        word_count = len(question.split())
        if word_count < 5:
            score -= 15.0
        elif word_count > 40:
            score -= 10.0
        
        return max(0.0, score)
    
    def generate_suggestions(self, analysis: Dict) -> List[Dict]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        total = analysis['total_questions']
        
        # Check Bloom's distribution
        for level, count in analysis['blooms_distribution'].items():
            percentage = (count / total * 100) if total > 0 else 0
            
            if count == 0:
                suggestions.append({
                    "type": "missing_level",
                    "priority": "high",
                    "category": "blooms_taxonomy",
                    "message": f"No questions at '{level}' level. Add questions requiring {level.lower()} skills.",
                    "level": level
                })
            elif percentage < 10:
                suggestions.append({
                    "type": "low_representation",
                    "priority": "medium",
                    "category": "blooms_taxonomy",
                    "message": f"Only {percentage:.1f}% questions at '{level}' level. Consider adding more.",
                    "level": level
                })
        
        # Check difficulty distribution
        for level, count in analysis['difficulty_distribution'].items():
            percentage = (count / total * 100) if total > 0 else 0
            
            if percentage < 20:
                suggestions.append({
                    "type": "difficulty_imbalance",
                    "priority": "medium",
                    "category": "difficulty",
                    "message": f"Only {percentage:.1f}% of questions are '{level}' difficulty. Add more {level.lower()} questions.",
                    "level": level
                })
        
        # Suggestions for ambiguous questions
        for item in analysis.get('ambiguous_questions', []):
            suggestions.append({
                "type": "ambiguity",
                "priority": "high",
                "category": "quality",
                "message": f"Question {item['question_number']} contains ambiguous terms: {', '.join(item['indicators'])}. Rephrase for clarity.",
                "question_number": item['question_number']
            })
        
        # Suggestions for quality issues
        for item in analysis.get('quality_issues', []):
            suggestions.append({
                "type": "quality_issue",
                "priority": "high",
                "category": "quality",
                "message": f"Question {item['question_number']} has quality issues: {', '.join(item['issues'])}. Please review.",
                "question_number": item['question_number']
            })
        
        return suggestions
    
    def calculate_overall_score(self, analysis: Dict) -> Dict:
        """Calculate overall quality score for the paper"""
        total_questions = analysis['total_questions']
        
        if total_questions == 0:
            return {"score": 0, "grade": "N/A", "feedback": "No questions to analyze"}
        
        # Calculate component scores
        blooms_score = self._calculate_blooms_score(analysis['blooms_distribution'], total_questions)
        difficulty_score = self._calculate_difficulty_score(analysis['difficulty_distribution'], total_questions)
        quality_score = self._calculate_quality_score(analysis, total_questions)
        
        # Weighted average
        overall_score = (blooms_score * 0.4 + difficulty_score * 0.3 + quality_score * 0.3)
        
        # Determine grade
        if overall_score >= 90:
            grade = "Excellent"
        elif overall_score >= 75:
            grade = "Good"
        elif overall_score >= 60:
            grade = "Fair"
        else:
            grade = "Needs Improvement"
        
        return {
            "score": round(overall_score, 2),
            "grade": grade,
            "blooms_score": round(blooms_score, 2),
            "difficulty_score": round(difficulty_score, 2),
            "quality_score": round(quality_score, 2),
            "feedback": self._generate_feedback(overall_score, grade)
        }
    
    def _calculate_blooms_score(self, distribution: Dict, total: int) -> float:
        """Calculate score based on Bloom's taxonomy distribution"""
        # Ideal: all levels represented
        represented_levels = sum(1 for count in distribution.values() if count > 0)
        representation_score = (represented_levels / 6) * 50
        
        # Balance: no level dominates
        percentages = [(count / total * 100) for count in distribution.values()]
        balance_score = 50 - (max(percentages) - min(percentages)) if percentages else 0
        
        return max(0, representation_score + balance_score)
    
    def _calculate_difficulty_score(self, distribution: Dict, total: int) -> float:
        """Calculate score based on difficulty distribution"""
        # Ideal: balanced distribution
        ideal_percentages = {"Easy": 30, "Medium": 40, "Hard": 30}
        score = 100
        
        for level, ideal_pct in ideal_percentages.items():
            actual_pct = (distribution[level] / total * 100) if total > 0 else 0
            deviation = abs(actual_pct - ideal_pct)
            score -= deviation * 0.5
        
        return max(0, score)
    
    def _calculate_quality_score(self, analysis: Dict, total: int) -> float:
        """Calculate score based on question quality"""
        score = 100
        
        # Deduct for ambiguous questions
        ambiguous_count = len(analysis.get('ambiguous_questions', []))
        score -= (ambiguous_count / total * 100) * 0.5 if total > 0 else 0
        
        # Deduct for quality issues
        issues_count = len(analysis.get('quality_issues', []))
        score -= (issues_count / total * 100) * 0.5 if total > 0 else 0
        
        return max(0, score)
    
    def _generate_feedback(self, score: float, grade: str) -> str:
        """Generate textual feedback based on score"""
        if score >= 90:
            return "Excellent question paper with comprehensive cognitive level coverage and good balance."
        elif score >= 75:
            return "Good question paper. Minor improvements suggested for better balance."
        elif score >= 60:
            return "Fair question paper. Several improvements needed for comprehensive coverage."
        else:
            return "Significant improvements needed. Review suggestions carefully."
    
    def generate_text_report(self, paper_id: int, filename: str, subject: str, 
                            analysis: Dict, suggestions: List[Dict]) -> str:
        """Generate a formatted text report"""
        report = []
        report.append("=" * 70)
        report.append("AI-BASED QUESTION PAPER MODERATION REPORT")
        report.append("=" * 70)
        report.append("")
        report.append(f"Report ID: {paper_id}")
        report.append(f"Filename: {filename}")
        report.append(f"Subject: {subject}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Questions: {analysis['total_questions']}")
        report.append("")
        
        # Overall score
        overall = self.calculate_overall_score(analysis)
        report.append("OVERALL ASSESSMENT")
        report.append("-" * 70)
        report.append(f"Overall Score: {overall['score']}/100")
        report.append(f"Grade: {overall['grade']}")
        report.append(f"Feedback: {overall['feedback']}")
        report.append("")
        
        # Bloom's taxonomy distribution
        report.append("BLOOM'S TAXONOMY DISTRIBUTION")
        report.append("-" * 70)
        for level, count in analysis['blooms_distribution'].items():
            pct = (count / analysis['total_questions'] * 100) if analysis['total_questions'] > 0 else 0
            report.append(f"{level:15}: {count:3} questions ({pct:5.1f}%)")
        report.append("")
        
        # Difficulty distribution
        report.append("DIFFICULTY DISTRIBUTION")
        report.append("-" * 70)
        for level, count in analysis['difficulty_distribution'].items():
            pct = (count / analysis['total_questions'] * 100) if analysis['total_questions'] > 0 else 0
            report.append(f"{level:15}: {count:3} questions ({pct:5.1f}%)")
        report.append("")
        
        # Ambiguous questions
        if analysis.get('ambiguous_questions'):
            report.append("AMBIGUOUS QUESTIONS DETECTED")
            report.append("-" * 70)
            for item in analysis['ambiguous_questions']:
                report.append(f"Q{item['question_number']}: {item['question']}")
                report.append(f"  Indicators: {', '.join(item['indicators'])}")
                report.append("")
        
        # Quality issues
        if analysis.get('quality_issues'):
            report.append("QUALITY ISSUES")
            report.append("-" * 70)
            for item in analysis['quality_issues']:
                report.append(f"Q{item['question_number']}: {item['question']}")
                report.append(f"  Issues: {', '.join(item['issues'])}")
                report.append("")
        
        # Suggestions
        if suggestions:
            report.append("RECOMMENDATIONS")
            report.append("-" * 70)
            for i, suggestion in enumerate(suggestions, 1):
                priority_marker = "⚠" if suggestion['priority'] == 'high' else "ℹ"
                report.append(f"{i}. [{priority_marker}] {suggestion['message']}")
            report.append("")
        
        report.append("=" * 70)
        report.append("End of Report")
        report.append("=" * 70)
        
        return "\n".join(report)
