import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Box, Typography, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Button, CircularProgress, Alert, Chip
} from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';

function HistoryPage() {
  const navigate = useNavigate();
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPapers();
  }, []);

  const fetchPapers = async () => {
    try {
      const response = await axios.get('/api/papers');
      setPapers(response.data.papers);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load papers');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Analysis History</Typography>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Filename</TableCell>
              <TableCell>Subject</TableCell>
              <TableCell>Professor</TableCell>
              <TableCell>Questions</TableCell>
              <TableCell>Upload Date</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {papers.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">No papers analyzed yet</TableCell>
              </TableRow>
            ) : (
              papers.map((paper) => (
                <TableRow key={paper.id}>
                  <TableCell>{paper.id}</TableCell>
                  <TableCell>{paper.filename}</TableCell>
                  <TableCell><Chip label={paper.subject} size="small" /></TableCell>
                  <TableCell>{paper.professor_name}</TableCell>
                  <TableCell>{paper.total_questions}</TableCell>
                  <TableCell>{new Date(paper.upload_date).toLocaleString()}</TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      startIcon={<VisibilityIcon />}
                      onClick={() => navigate(`/report/${paper.id}`)}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default HistoryPage;
