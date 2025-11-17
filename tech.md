
# AI-Based Question Paper Moderation System

## Background
Ensuring examination fairness and quality by balancing question difficulty and cognitive skill coverage based on Bloom's Taxonomy is crucial for universities. Manual question paper reviews are time-consuming, inconsistent, and biased.

## Problem Statement
- Absence of automated tools to ensure balanced cognitive level coverage.
- Difficulty detecting ambiguous questions and difficulty misalignment.
- Review process is labor-intensive, affecting fairness and workload.

## Objective
Create an AI system to automatically classify questions according to Bloom's Taxonomy using NLP, detect ambiguity, estimate difficulty, highlight gaps, and suggest improvements.

## Features
1. Input Module for draft question papers.
2. NLP Analysis: tokenization, semantic classification, ambiguity detection.
3. Difficulty Estimation using historical data.
4. Coverage Report showing cognitive level distribution and gaps.
5. Suggestion Engine for question modifications.
6. Interactive CLI interface (optional, as a core demo).
7. Feedback Learning for model improvement.

## User Roles
- Professor: Submit, review, and apply suggestions.
- System Admin (optional): Manage system updates.

## Benefits
- Reduces faculty workload.
- Improves exam quality and fairness.
- Ensures comprehensive cognitive level testing.
- Transparent, explainable moderation.

## Tech Stack
- Python with SpaCy, NLTK, or Hugging Face for NLP.
- SQLite or flat files for data storage.
- Python CLI frameworks like argparse or click (for CLI demo).
- Web Framework: Flask or FastAPI for backend API.
- Frontend: React or plain HTML/CSS/JS for simplicity.

## Timeline
- Weeks 1-2: Requirements, dataset, NLP setup.
- Weeks 3-4: CLI and web input/output modules, question parsing & classification.
- Weeks 5-6: Ambiguity detection and difficulty estimation modules.
- Week 7: Reporting and suggestions engine.
- Week 8: Testing, feedback integration, and demo preparation.

---

# Website and Backend Core Structure

## Website
- Homepage: Introduction, project overview, and user login (optional).
- Upload Page: Professors upload draft question papers as text files.
- Report Page: Displays structured analysis
  - Cognitive level classification summary.
  - Difficulty distribution.
  - Ambiguities identified.
  - Suggestions for balancing question paper.
- Feedback Page: Professors can submit feedback on suggestions and report accuracy.

## Backend
- NLP Module: Processes uploaded papers using:
  - Text parsing and tokenization.
  - Semantic classification into Bloom9s Taxonomy cognitive levels.
  - Ambiguity detection via linguistic cues.
- Difficulty Estimator: Scores questions by analyzing keywords and referencing historical student performance data.
- Suggestion Engine: Proposes question modifications or additional questions to balance the paper.
- Database: Stores uploaded papers, analysis reports, and user feedback for iterative improvement.
- API Endpoints:
  - Upload draft paper.
  - Request question analysis.
  - Fetch report and suggestions.
  - Submit feedback on AI suggestions.

## Workflow and Core Operations Demo

1. **Uploading Paper**: Professor uploads draft question paper via website or CLI.
2. **Processing**: Backend NLP module analyzes each question for:
   - Cognitive level classification.
   - Ambiguity detection.
   - Difficulty scoring.
3. **Reporting**: System generates a detailed report on coverage and difficulty spread.
4. **Suggestions**: Displays actionable suggestions for unbalanced or ambiguous questions.
5. **User Interaction**: Professor reviews and accepts or customizes suggestions.
6. **Feedback Loop**: User feedback stored to retrain and improve analysis models over time.

---

This tech.md provides a clear and complete project brief along with an operational website and backend architecture you can use to demonstrate the core functions of your AI-based question paper moderation system. It covers all essential aspects from input handling to AI-driven analysis, reporting, suggestion, and feedback for continuous learning.
