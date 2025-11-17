import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box, Typography, Paper, Grid, Card, CardContent, CircularProgress, Alert
} from '@mui/material';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function StatisticsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await axios.get('/api/statistics');
      setStats(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!stats) return null;

  const bloomsChartData = {
    labels: Object.keys(stats.blooms_distribution || {}),
    datasets: [{
      label: 'Total Questions',
      data: Object.values(stats.blooms_distribution || {}),
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
    }]
  };

  const difficultyChartData = {
    labels: Object.keys(stats.difficulty_distribution || {}),
    datasets: [{
      label: 'Total Questions',
      data: Object.values(stats.difficulty_distribution || {}),
      backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
    }]
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>System Statistics</Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>Total Papers</Typography>
              <Typography variant="h2">{stats.total_papers}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>Total Questions</Typography>
              <Typography variant="h2">{stats.total_questions}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>Avg Quality Score</Typography>
              <Typography variant="h2">{stats.average_quality_score}</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Overall Bloom's Distribution</Typography>
            <Pie data={bloomsChartData} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Overall Difficulty Distribution</Typography>
            <Bar data={difficultyChartData} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default StatisticsPage;
