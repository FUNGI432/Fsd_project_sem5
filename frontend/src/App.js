import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Button, Box } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import DescriptionIcon from '@mui/icons-material/Description';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import ReportPage from './pages/ReportPage';
import HistoryPage from './pages/HistoryPage';
import StatisticsPage from './pages/StatisticsPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <DescriptionIcon sx={{ mr: 2 }} />
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                Question Paper Moderator
              </Typography>
              <Button color="inherit" component={Link} to="/">
                Home
              </Button>
              <Button color="inherit" component={Link} to="/upload">
                Upload
              </Button>
              <Button color="inherit" component={Link} to="/history">
                History
              </Button>
              <Button color="inherit" component={Link} to="/statistics">
                Statistics
              </Button>
            </Toolbar>
          </AppBar>

          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/report/:paperId" element={<ReportPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/statistics" element={<StatisticsPage />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
