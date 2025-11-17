import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import {
  Box, Typography, Paper, Grid, Card, CardContent, CircularProgress,
  Chip, Alert, Button, LinearProgress
} from '@mui/material';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import DownloadIcon from '@mui/icons-material/Download';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function ReportPage() {
  const { paperId } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchReport();
  }, [paperId]);

  const fetchReport = async () => {
    try {
      const response = await axios.get(`/api/papers/${paperId}/report`);
      setReport(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load report');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    window.open(`/api/export/${paperId}`, '_blank');
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!report) return null;

  const bloomsData = {
    labels: Object.keys(report.blooms_distribution),
    datasets: [{
      data: Object.values(report.blooms_distribution),
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    }]
  };

  const difficultyData = {
    labels: Object.keys(report.difficulty_distribution),
    datasets: [{
      label: 'Questions',
      data: Object.values(report.difficulty_distribution),
      backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
    }]
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Analysis Report</Typography>
        <Button variant="outlined" startIcon={<DownloadIcon />} onClick={handleExport}>
          Export Report
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Overall Score</Typography>
              <Typography variant="h2" color="primary">{report.overall_score.score}</Typography>
              <Typography variant="body2" color="text.secondary">{report.overall_score.grade}</Typography>
              <LinearProgress variant="determinate" value={report.overall_score.score} sx={{ mt: 2 }} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Total Questions</Typography>
              <Typography variant="h2">{report.total_questions}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Subject</Typography>
              <Typography variant="h5">{report.subject}</Typography>
              <Typography variant="body2" color="text.secondary">by {report.professor_name}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Bloom's Taxonomy Distribution</Typography>
            <Pie data={bloomsData} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Difficulty Distribution</Typography>
            <Bar data={difficultyData} />
          </Paper>
        </Grid>

        {report.ambiguous_questions?.length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>Ambiguous Questions</Typography>
              {report.ambiguous_questions.map((item, idx) => (
                <Alert severity="warning" key={idx} sx={{ mb: 1 }}>
                  <strong>Q{item.question_number}:</strong> {item.question}
                  <br />
                  <small>Indicators: {item.indicators.join(', ')}</small>
                </Alert>
              ))}
            </Paper>
          </Grid>
        )}

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Suggestions</Typography>
            {report.suggestions.map((suggestion, idx) => (
              <Alert
                severity={suggestion.priority === 'high' ? 'error' : 'info'}
                key={idx}
                sx={{ mb: 1 }}
              >
                <Chip label={suggestion.category} size="small" sx={{ mr: 1 }} />
                {suggestion.message}
              </Alert>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default ReportPage;
