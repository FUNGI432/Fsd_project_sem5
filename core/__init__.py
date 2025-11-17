"""
Core module for AI-Based Question Paper Moderation System
Contains NLP analysis and database components
"""

from .nlp_analyzer import NLPAnalyzer
from .database import Database

__all__ = ['NLPAnalyzer', 'Database']
