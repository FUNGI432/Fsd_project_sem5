# Quick Start Guide
## AI-Based Question Paper Moderation System

Get started in 5 minutes!

## Installation

### Option 1: Automated Installation (Recommended)

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

1. **Install Python dependencies:**
   ```bash
   pip install Flask Flask-CORS
   ```

2. **Initialize database:**
   ```bash
   python -c "from core.database import Database; db = Database(); db.initialize()"
   ```

## Running the Application

Start the server:
```bash
python run.py
```

Access the application:
- Web Interface: **http://localhost:5000**
- API Documentation: **http://localhost:5000/api/health**

## First Steps

### 1. Upload a Question Paper

**Via Web Interface:**
1. Open http://localhost:5000
2. Click "Upload Question Paper"
3. Select a text file or enter questions directly
4. Fill in professor name and subject
5. Click "Upload and Analyze"

**Via API:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "questions": ["Define algorithm", "Analyze sorting complexity"],
    "professor_name": "Dr. Smith",
    "subject": "Computer Science"
  }'
```

### 2. View Report

After analysis, you'll see:
- Overall quality score
- Bloom's Taxonomy distribution chart
- Difficulty distribution chart
- Ambiguous questions list
- Actionable suggestions

### 3. Export Report

Click "Export Report" to download a detailed text report.

## Quick Test

Run the test suite to verify installation:
```bash
pip install requests
python test_api.py
```

All tests should pass ✓

## Sample Question File Format

Create a text file `questions.txt`:
```
Define the term "algorithm" and explain its importance.
List the main data structures in computer science.
Analyze the time complexity of quicksort algorithm.
Evaluate the trade-offs between different sorting algorithms.
Create a new data structure for efficient searching.
```

## API Quick Reference

### Analyze Questions
```bash
POST /api/analyze
{
  "questions": ["question1", "question2"],
  "professor_name": "Name",
  "subject": "Subject"
}
```

### Get Report
```bash
GET /api/papers/{id}/report
```

### Get All Papers
```bash
GET /api/papers
```

### System Statistics
```bash
GET /api/statistics
```

## Next Steps

1. **Explore the Web Interface**: Navigate through all pages
2. **Try Different Question Types**: Test with various subjects
3. **Review Suggestions**: See how the system improves question quality
4. **Check History**: View past analyses
5. **Export Reports**: Download detailed analysis

## Troubleshooting

**Port 5000 already in use?**
```bash
PORT=8000 python run.py
```

**Module not found?**
```bash
pip install -r requirements.txt
```

**Database error?**
```bash
rm data/moderation.db
python -c "from core.database import Database; db = Database(); db.initialize()"
```

## Production Deployment

For production deployment with frontend:
1. Install Node.js and npm
2. Build frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
3. Run production server (see DEPLOYMENT.md)

## Need Help?

- Check README.md for detailed documentation
- See DEPLOYMENT.md for deployment guide
- Review API examples in test_api.py

## System Overview

```
┌─────────────────┐
│   Upload Page   │  ← Professor uploads question paper
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  NLP Analyzer   │  ← Analyzes questions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Report Page    │  ← Shows results & suggestions
└─────────────────┘
```

**Ready to moderate question papers! 🎉**
