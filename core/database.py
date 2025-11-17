#!/usr/bin/env python3
"""
Database module for AI-Based Question Paper Moderation System
Handles all database operations using SQLite
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os


class Database:
    """Database handler for the question paper moderation system"""
    
    def __init__(self, db_path: str = 'data/moderation.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = None
        self.cursor = None
    
    def _get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        return self.conn
    
    def initialize(self):
        """Initialize database tables"""
        conn = self._get_connection()
        
        # Papers table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                professor_name TEXT,
                subject TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_questions INTEGER,
                analysis_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Questions table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER,
                question_number INTEGER,
                question_text TEXT NOT NULL,
                blooms_level TEXT,
                difficulty TEXT,
                is_ambiguous BOOLEAN,
                cognitive_load REAL,
                quality_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES papers (id)
            )
        ''')
        
        # Feedback table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER,
                feedback_data TEXT,
                rating INTEGER,
                comments TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paper_id) REFERENCES papers (id)
            )
        ''')
        
        # Statistics table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_date DATE,
                total_papers INTEGER,
                total_questions INTEGER,
                avg_quality_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
    
    def save_paper(self, filename: str, professor_name: str, subject: str, 
                   questions: List[str], analysis: Dict) -> int:
        """Save paper and its analysis to database"""
        conn = self._get_connection()
        
        # Insert paper
        cursor = conn.execute('''
            INSERT INTO papers (filename, professor_name, subject, total_questions, analysis_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (filename, professor_name, subject, len(questions), json.dumps(analysis)))
        
        paper_id = cursor.lastrowid
        
        # Insert questions
        for detail in analysis.get('question_details', []):
            conn.execute('''
                INSERT INTO questions (
                    paper_id, question_number, question_text, blooms_level, 
                    difficulty, is_ambiguous, cognitive_load, quality_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                paper_id,
                detail['number'],
                detail['text'],
                detail['blooms_level'],
                detail['difficulty'],
                detail['ambiguous'],
                detail['cognitive_load'],
                detail['quality_score']
            ))
        
        conn.commit()
        return int(paper_id) if paper_id is not None else 0
    
    def get_paper(self, paper_id: int) -> Optional[Dict]:
        """Get paper by ID"""
        conn = self._get_connection()
        
        cursor = conn.execute('''
            SELECT * FROM papers WHERE id = ?
        ''', (paper_id,))
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        paper = dict(row)
        paper['analysis'] = json.loads(paper['analysis_data']) if paper['analysis_data'] else {}
        
        # Get questions
        cursor = conn.execute('''
            SELECT * FROM questions WHERE paper_id = ? ORDER BY question_number
        ''', (paper_id,))
        
        paper['questions'] = [dict(row) for row in cursor.fetchall()]
        
        return paper
    
    def get_all_papers(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all papers with pagination"""
        conn = self._get_connection()
        
        cursor = conn.execute('''
            SELECT id, filename, professor_name, subject, upload_date, 
                   total_questions, created_at
            FROM papers
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def save_feedback(self, paper_id: int, feedback_data: Dict, 
                     rating: int, comments: str) -> int:
        """Save feedback for a paper"""
        conn = self._get_connection()
        
        cursor = conn.execute('''
            INSERT INTO feedback (paper_id, feedback_data, rating, comments)
            VALUES (?, ?, ?, ?)
        ''', (paper_id, json.dumps(feedback_data), rating, comments))
        
        conn.commit()
        return int(cursor.lastrowid) if cursor.lastrowid is not None else 0
    
    def get_feedback(self, paper_id: int) -> List[Dict]:
        """Get all feedback for a paper"""
        conn = self._get_connection()
        
        cursor = conn.execute('''
            SELECT * FROM feedback WHERE paper_id = ? ORDER BY created_at DESC
        ''', (paper_id,))
        
        feedbacks = []
        for row in cursor.fetchall():
            feedback = dict(row)
            feedback['feedback_data'] = json.loads(feedback['feedback_data']) if feedback['feedback_data'] else {}
            feedbacks.append(feedback)
        
        return feedbacks
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        conn = self._get_connection()
        
        # Total papers
        cursor = conn.execute('SELECT COUNT(*) as count FROM papers')
        total_papers = cursor.fetchone()['count']
        
        # Total questions
        cursor = conn.execute('SELECT COUNT(*) as count FROM questions')
        total_questions = cursor.fetchone()['count']
        
        # Average quality score
        cursor = conn.execute('SELECT AVG(quality_score) as avg_score FROM questions')
        avg_quality = cursor.fetchone()['avg_score'] or 0
        
        # Papers by subject
        cursor = conn.execute('''
            SELECT subject, COUNT(*) as count 
            FROM papers 
            GROUP BY subject
        ''')
        papers_by_subject = {row['subject']: row['count'] for row in cursor.fetchall()}
        
        # Bloom's level distribution
        cursor = conn.execute('''
            SELECT blooms_level, COUNT(*) as count 
            FROM questions 
            GROUP BY blooms_level
        ''')
        blooms_distribution = {row['blooms_level']: row['count'] for row in cursor.fetchall()}
        
        # Difficulty distribution
        cursor = conn.execute('''
            SELECT difficulty, COUNT(*) as count 
            FROM questions 
            GROUP BY difficulty
        ''')
        difficulty_distribution = {row['difficulty']: row['count'] for row in cursor.fetchall()}
        
        return {
            'total_papers': total_papers,
            'total_questions': total_questions,
            'average_quality_score': round(avg_quality, 2),
            'papers_by_subject': papers_by_subject,
            'blooms_distribution': blooms_distribution,
            'difficulty_distribution': difficulty_distribution
        }
    
    def search_papers(self, search_term: str) -> List[Dict]:
        """Search papers by filename, professor, or subject"""
        conn = self._get_connection()
        
        search_pattern = f'%{search_term}%'
        cursor = conn.execute('''
            SELECT id, filename, professor_name, subject, upload_date, 
                   total_questions, created_at
            FROM papers
            WHERE filename LIKE ? OR professor_name LIKE ? OR subject LIKE ?
            ORDER BY created_at DESC
        ''', (search_pattern, search_pattern, search_pattern))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_paper(self, paper_id: int) -> bool:
        """Delete a paper and its associated data"""
        conn = self._get_connection()
        
        try:
            # Delete questions
            conn.execute('DELETE FROM questions WHERE paper_id = ?', (paper_id,))
            
            # Delete feedback
            conn.execute('DELETE FROM feedback WHERE paper_id = ?', (paper_id,))
            
            # Delete paper
            conn.execute('DELETE FROM papers WHERE id = ?', (paper_id,))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error deleting paper: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
