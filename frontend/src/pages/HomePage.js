import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AssessmentIcon from '@mui/icons-material/Assessment';
import HistoryIcon from '@mui/icons-material/History';
import TipsAndUpdatesIcon from '@mui/icons-material/TipsAndUpdates';

function HomePage() {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Bloom\'s Taxonomy Classification',
      description: 'Automatically classify questions into six cognitive levels',
      icon: <TipsAndUpdatesIcon fontSize="large" color="primary" />,
    },
    {
      title: 'Difficulty Assessment',
      description: 'Estimate question difficulty based on linguistic analysis',
      icon: <AssessmentIcon fontSize="large" color="primary" />,
    },
    {
      title: 'Ambiguity Detection',
      description: 'Identify unclear or ambiguous phrasing in questions',
      icon: <TipsAndUpdatesIcon fontSize="large" color="primary" />,
    },
    {
      title: 'Comprehensive Reports',
      description: 'Get detailed reports with actionable suggestions',
      icon: <AssessmentIcon fontSize="large" color="primary" />,
    },
  ];

  return (
    <Box>
      <Paper
        sx={{
          p: 4,
          mb: 4,
          background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
          color: 'white',
        }}
      >
        <Typography variant="h3" gutterBottom>
          AI-Based Question Paper Moderation System
        </Typography>
        <Typography variant="h6" paragraph>
          Ensure comprehensive cognitive level coverage and balanced difficulty distribution
        </Typography>
        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<UploadFileIcon />}
            onClick={() => navigate('/upload')}
            sx={{ mr: 2, bgcolor: 'white', color: 'primary.main' }}
          >
            Upload Question Paper
          </Button>
          <Button
            variant="outlined"
            size="large"
            startIcon={<HistoryIcon />}
            onClick={() => navigate('/history')}
            sx={{ borderColor: 'white', color: 'white' }}
          >
            View History
          </Button>
        </Box>
      </Paper>

      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Key Features
      </Typography>

      <Grid container spacing={3}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {feature.icon}
                  <Typography variant="h6" sx={{ ml: 2 }}>
                    {feature.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper sx={{ p: 3, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          How It Works
        </Typography>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" color="primary">1. Upload</Typography>
            <Typography variant="body2">Upload your draft question paper</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" color="primary">2. Analyze</Typography>
            <Typography variant="body2">AI analyzes each question comprehensively</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" color="primary">3. Review</Typography>
            <Typography variant="body2">View detailed reports and suggestions</Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" color="primary">4. Improve</Typography>
            <Typography variant="body2">Apply suggestions to enhance quality</Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

export default HomePage;
