
# Product Requirement Document (PRD)
## AI-Based Question Paper Moderation System

### Background
Examination fairness and quality are critical for universities. Professors face challenges balancing question difficulty and cognitive skill coverage defined by Bloom's Taxonomy (Knowledge, Comprehension, Application, Analysis, Synthesis, Evaluation). Manual review is time-intensive and prone to inconsistency and bias.

### Problem Statement
- Lack of automated tools to ensure comprehensive question paper coverage across cognitive skill levels.
- Hard to detect ambiguous phrasing, difficulty misalignment, and cognitive level gaps manually.
- Time-consuming review process impacts faculty workload and fairness.

### Objective
Develop an AI-powered system to:
- Automatically analyze and classify each question using NLP against Bloom's Taxonomy.
- Detect ambiguous phrasing and unclear questions.
- Estimate and balance question difficulty leveraging historical student performance data.
- Highlight underrepresented cognitive levels and suggest modifications.
- Allow faculty to submit draft papers, receive detailed reports and improve question quality iteratively.

### Key Features (Core Operations to Demonstrate)
1. **Input Module:** Accept draft question papers via CLI input or file upload.
2. **NLP Analysis:** Process each question line-by-line (cursor-like iteration), performing:
   - Text parsing and tokenization
   - Semantic classification into Bloom's cognitive levels
   - Ambiguity detection via linguistic cues
3. **Difficulty Estimation:** Assign difficulty scores based on keywords and/or historical data pattern matching.
4. **Coverage Report:** Aggregate results to show question distribution across cognitive levels, difficulty spread, identified gaps.
5. **Suggestion Engine:** Propose question modifications or additional questions to balance the paper.
6. **Interactive CLI Interface:** Show progress of questions being processed, interim results, options to accept or modify suggestions live.
7. **Feedback Learning:** Store user feedback to retrain/improve NLP models over time (optional extension for future versions).

### User Roles
- **Professor:** Creates and submits question papers, reviews AI feedback, applies suggestions.
- **System Admin (optional):** Manages model training data and system updates.

### Benefits
- Reduces faculty workload drastically.
- Improves quality, fairness, and balance of exams.
- Ensures comprehensive cognitive level coverage.
- Facilitates transparent and explainable question paper moderation.

### Technical Stack Suggestions
- Programming Language: Python (for rich NLP libraries and ease of CLI implementation)
- NLP Tools: SpaCy, NLTK, or Hugging Face Transformers for question classification and ambiguity detection.
- Data Storage: SQLite or flat files to store question papers, feedback records.
- CLI Framework: Python's `argparse` or `click` for interactive terminal UI.

### Example CLI Usage Flow
```bash
$ python qpaper_mod.py --input draft_paper.txt
Processing question 1/20: Analyzing...
Cognitive Level: Application
Difficulty: Medium
Ambiguity: Low
...
Report generated: report_summary.txt
Suggestions available: 3
Accept suggestion 1? (y/n): y
...
Summary:
- Knowledge: 4 questions
- Comprehension: 3 questions
- Application: 5 questions
- Analysis, Synthesis, Evaluation: Underrepresented
Recommendation: Add 2 higher cognitive-level questions
```

### Timeline and Milestones
- Week 1-2: Requirement analysis, dataset collection, NLP model setup
- Week 3-4: Develop CLI input/output modules, implement question parsing & classification
- Week 5-6: Implement ambiguity detection and difficulty estimation
- Week 7: Develop reporting and suggestion engine
- Week 8: Testing, feedback integration, and final demo preparation

---
This PRD focuses on core operations visible and explainable at the command line level, ideal for your video coding and professor demo.
