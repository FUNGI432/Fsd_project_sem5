#!/usr/bin/env python3
"""
Flask Backend for AI-Based Question Paper Moderation System
Production-ready API with database integration
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import sqlite3
from pathlib import Path

# Import our NLP modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from core.nlp_analyzer import NLPAnalyzer
from core.database import Database

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'doc', 'docx'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database and NLP analyzer
db = Database()
analyzer = NLPAnalyzer()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/upload', methods=['POST'])
def upload_paper():
    """Upload and analyze a question paper"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Get optional metadata
        professor_name = request.form.get('professor_name', 'Anonymous')
        subject = request.form.get('subject', 'General')
        
        # Save file
        filename = secure_filename(file.filename or 'unnamed.txt')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Read questions from file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            questions = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not questions:
            return jsonify({'error': 'No questions found in file'}), 400
        
        # Analyze questions
        analysis_results = analyzer.analyze_questions(questions)
        
        # Save to database
        paper_id = db.save_paper(
            filename=unique_filename,
            professor_name=professor_name,
            subject=subject,
            questions=questions,
            analysis=analysis_results
        )
        
        # Generate suggestions
        suggestions = analyzer.generate_suggestions(analysis_results)
        
        return jsonify({
            'paper_id': paper_id,
            'filename': filename,
            'total_questions': len(questions),
            'analysis': analysis_results,
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze questions from direct text input"""
    try:
        data = request.get_json()
        
        if not data or 'questions' not in data:
            return jsonify({'error': 'No questions provided'}), 400
        
        questions = data['questions']
        if not isinstance(questions, list):
            questions = [questions]
        
        # Get optional metadata
        professor_name = data.get('professor_name', 'Anonymous')
        subject = data.get('subject', 'General')
        
        # Analyze questions
        analysis_results = analyzer.analyze_questions(questions)
        
        # Save to database
        paper_id = db.save_paper(
            filename=f"text_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            professor_name=professor_name,
            subject=subject,
            questions=questions,
            analysis=analysis_results
        )
        
        # Generate suggestions
        suggestions = analyzer.generate_suggestions(analysis_results)
        
        return jsonify({
            'paper_id': paper_id,
            'total_questions': len(questions),
            'analysis': analysis_results,
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/papers', methods=['GET'])
def get_papers():
    """Get all analyzed papers"""
    try:
        papers = db.get_all_papers()
        return jsonify({
            'papers': papers,
            'count': len(papers)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/papers/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    """Get specific paper details"""
    try:
        paper = db.get_paper(paper_id)
        if not paper:
            return jsonify({'error': 'Paper not found'}), 404
        
        return jsonify(paper), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/papers/<int:paper_id>/report', methods=['GET'])
def get_report(paper_id):
    """Generate detailed report for a paper"""
    try:
        paper = db.get_paper(paper_id)
        if not paper:
            return jsonify({'error': 'Paper not found'}), 404
        
        analysis = paper['analysis']
        suggestions = analyzer.generate_suggestions(analysis)
        
        report = {
            'paper_id': paper_id,
            'filename': paper['filename'],
            'subject': paper['subject'],
            'professor_name': paper['professor_name'],
            'upload_date': paper['upload_date'],
            'total_questions': analysis['total_questions'],
            'blooms_distribution': analysis['blooms_distribution'],
            'difficulty_distribution': analysis['difficulty_distribution'],
            'ambiguous_questions': analysis.get('ambiguous_questions', []),
            'suggestions': suggestions,
            'overall_score': analyzer.calculate_overall_score(analysis)
        }
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback on suggestions"""
    try:
        data = request.get_json()
        
        if not data or 'paper_id' not in data:
            return jsonify({'error': 'Paper ID required'}), 400
        
        paper_id = data['paper_id']
        feedback_data = data.get('feedback', {})
        rating = data.get('rating', 0)
        comments = data.get('comments', '')
        
        feedback_id = db.save_feedback(
            paper_id=paper_id,
            feedback_data=feedback_data,
            rating=rating,
            comments=comments
        )
        
        return jsonify({
            'feedback_id': feedback_id,
            'message': 'Feedback submitted successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    try:
        stats = db.get_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<int:paper_id>', methods=['GET'])
def export_report(paper_id):
    """Export report as text file"""
    try:
        paper = db.get_paper(paper_id)
        if not paper:
            return jsonify({'error': 'Paper not found'}), 404
        
        analysis = paper['analysis']
        suggestions = analyzer.generate_suggestions(analysis)
        
        # Generate report text
        report_text = analyzer.generate_text_report(
            paper_id=paper_id,
            filename=paper['filename'],
            subject=paper['subject'],
            analysis=analysis,
            suggestions=suggestions
        )
        
        # Ensure uploads directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save report to file
        report_filename = f"report_{paper_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_path = os.path.join(app.config['UPLOAD_FOLDER'], report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        # Return the file
        return send_from_directory(
            directory=os.path.abspath(app.config['UPLOAD_FOLDER']),
            path=report_filename,
            as_attachment=True,
            mimetype='text/plain'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve React frontend in production or fallback HTML
@app.route('/')
def index():
    """Serve main page"""
    # Check if React build exists
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        # Serve a simple HTML page with API links
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question Paper Moderator - API Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { font-size: 16px; opacity: 0.9; }
        .content { padding: 40px; }
        .status { 
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 4px;
        }
        .status h3 { color: #2e7d32; margin-bottom: 5px; }
        .endpoint {
            background: #f5f5f5;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 3px solid #1976d2;
        }
        .endpoint code {
            background: #263238;
            color: #aed581;
            padding: 3px 8px;
            border-radius: 3px;
            font-family: monospace;
        }
        .method {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }
        .get { background: #4caf50; color: white; }
        .post { background: #ff9800; color: white; }
        .button {
            display: inline-block;
            background: #1976d2;
            color: white;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            margin: 10px 10px 10px 0;
            transition: background 0.3s;
        }
        .button:hover { background: #1565c0; }
        h2 { color: #333; margin: 30px 0 15px 0; }
        p { line-height: 1.6; color: #666; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Question Paper Moderator</h1>
            <p>AI-Based Analysis System - API Server Running</p>
        </div>
        <div class="content">
            <div class="status">
                <h3>✅ Server Status: RUNNING</h3>
                <p>The API server is active and ready to accept requests.</p>
            </div>
            
            <h2>Quick Test</h2>
            <a href="/api/health" class="button" target="_blank">Health Check</a>
            <a href="/api/statistics" class="button" target="_blank">View Statistics</a>
            <a href="/api/papers" class="button" target="_blank">All Papers</a>
            
            <h2>API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/health</code>
                <p>Check server health status</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/upload</code>
                <p>Upload and analyze a question paper file</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/analyze</code>
                <p>Analyze questions from text input</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/papers</code>
                <p>Get list of all analyzed papers</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/papers/:id</code>
                <p>Get specific paper details</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/papers/:id/report</code>
                <p>Get detailed analysis report</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/statistics</code>
                <p>Get system statistics</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/feedback</code>
                <p>Submit feedback on suggestions</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/export/:id</code>
                <p>Export report as text file</p>
            </div>
            
            <h2>Example cURL Commands</h2>
            <div class="endpoint">
                <p><strong>Analyze Questions:</strong></p>
                <code>curl -X POST http://localhost:5000/api/analyze -H "Content-Type: application/json" -d "{\"questions\": [\"Define algorithm\"], \"professor_name\": \"Dr. Smith\", \"subject\": \"CS\"}"</code>
            </div>
            
            <h2>Frontend Setup</h2>
            <p>To enable the web interface:</p>
            <ol style="margin-left: 20px; color: #666;">
                <li style="margin: 10px 0;">Install Node.js and npm</li>
                <li style="margin: 10px 0;">Navigate to <code>frontend/</code> directory</li>
                <li style="margin: 10px 0;">Run <code>npm install</code></li>
                <li style="margin: 10px 0;">Run <code>npm run build</code></li>
                <li style="margin: 10px 0;">Restart the server</li>
            </ol>
        </div>
    </div>
</body>
</html>
        '''

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files if they exist"""
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return jsonify({'error': 'File not found'}), 404


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize database tables
    db.initialize()
    
    # Run server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
