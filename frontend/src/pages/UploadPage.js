import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Box, Typography, Paper, Button, TextField, CircularProgress,
  Alert, Tabs, Tab, Snackbar
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

function UploadPage() {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [file, setFile] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [professorName, setProfessorName] = useState('');
  const [subject, setSubject] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('professor_name', professorName);
    formData.append('subject', subject);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setSuccess(true);
      setTimeout(() => navigate(`/report/${response.data.paper_id}`), 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!textInput.trim()) {
      setError('Please enter questions');
      return;
    }

    setLoading(true);
    setError('');

    const questions = textInput.split('\n').filter(q => q.trim());

    try {
      const response = await axios.post('/api/analyze', {
        questions,
        professor_name: professorName,
        subject
      });
      setSuccess(true);
      setTimeout(() => navigate(`/report/${response.data.paper_id}`), 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Upload Question Paper</Typography>
      
      <Paper sx={{ p: 3 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 3 }}>
          <Tab label="Upload File" />
          <Tab label="Enter Text" />
        </Tabs>

        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            label="Professor Name"
            value={professorName}
            onChange={(e) => setProfessorName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />
        </Box>

        {tabValue === 0 ? (
          <form onSubmit={handleFileUpload}>
            <Box sx={{ mb: 3, p: 3, border: '2px dashed #ccc', borderRadius: 1, textAlign: 'center' }}>
              <input
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={(e) => setFile(e.target.files[0])}
                style={{ display: 'none' }}
                id="file-input"
              />
              <label htmlFor="file-input">
                <Button variant="outlined" component="span" startIcon={<CloudUploadIcon />}>
                  Select File
                </Button>
              </label>
              {file && <Typography sx={{ mt: 2 }}>{file.name}</Typography>}
            </Box>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading || !file}
              startIcon={loading && <CircularProgress size={20} />}
            >
              {loading ? 'Uploading...' : 'Upload and Analyze'}
            </Button>
          </form>
        ) : (
          <form onSubmit={handleTextSubmit}>
            <TextField
              fullWidth
              multiline
              rows={10}
              placeholder="Enter questions (one per line)"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              sx={{ mb: 2 }}
            />
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading || !textInput.trim()}
              startIcon={loading && <CircularProgress size={20} />}
            >
              {loading ? 'Analyzing...' : 'Analyze Questions'}
            </Button>
          </form>
        )}

        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      </Paper>

      <Snackbar open={success} autoHideDuration={3000} onClose={() => setSuccess(false)}>
        <Alert severity="success">Analysis complete! Redirecting...</Alert>
      </Snackbar>
    </Box>
  );
}

export default UploadPage;
