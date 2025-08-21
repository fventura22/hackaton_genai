import React, { useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { Security, CheckCircle, Block } from '@mui/icons-material';
import ApiService from '../services/ApiService';

function FraudAnalysis() {
  const [formData, setFormData] = useState({
    customerId: '',
    transactionId: '',
    amount: '',
    location: '',
    merchantCategory: '',
    description: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleAnalyze = async () => {
    if (!formData.customerId || !formData.transactionId || !formData.amount) {
      setError('Please fill in all required fields');
      return;
    }

    if (isNaN(parseFloat(formData.amount))) {
      setError('Please enter a valid amount');
      return;
    }

    setLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await ApiService.analyzeFraud(formData);
      
      if (response.success) {
        setResult(response.data);
      } else {
        setError(response.error);
      }
    } catch (error) {
      setError('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 0.8) return 'error';
    if (score >= 0.6) return 'warning';
    if (score >= 0.4) return 'info';
    return 'success';
  };

  const getRiskLevel = (score) => {
    if (score >= 0.8) return 'HIGH RISK';
    if (score >= 0.6) return 'MEDIUM RISK';
    if (score >= 0.4) return 'LOW RISK';
    return 'SAFE';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Transaction Analysis
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Analyze transactions for potential fraud
      </Typography>

      <Grid container spacing={3}>
        {/* Input Form */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Transaction Details
              </Typography>
              
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <TextField
                  label="Customer ID"
                  required
                  fullWidth
                  value={formData.customerId}
                  onChange={(e) => handleInputChange('customerId', e.target.value)}
                  placeholder="e.g., CUST001"
                />
                
                <TextField
                  label="Transaction ID"
                  required
                  fullWidth
                  value={formData.transactionId}
                  onChange={(e) => handleInputChange('transactionId', e.target.value)}
                  placeholder="e.g., TXN123"
                />
                
                <TextField
                  label="Amount"
                  required
                  fullWidth
                  type="number"
                  value={formData.amount}
                  onChange={(e) => handleInputChange('amount', e.target.value)}
                  placeholder="e.g., 1500.00"
                />
                
                <TextField
                  label="Location"
                  fullWidth
                  value={formData.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  placeholder="e.g., New York, NY"
                />
                
                <TextField
                  label="Merchant Category"
                  fullWidth
                  value={formData.merchantCategory}
                  onChange={(e) => handleInputChange('merchantCategory', e.target.value)}
                  placeholder="e.g., retail, online_gaming"
                />
                
                <TextField
                  label="Description"
                  fullWidth
                  multiline
                  rows={3}
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  placeholder="Additional transaction details..."
                />

                <Button
                  variant="contained"
                  size="large"
                  onClick={handleAnalyze}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <Security />}
                  sx={{ mt: 2, py: 1.5 }}
                >
                  {loading ? 'Analyzing...' : 'Analyze Transaction'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Results */}
        <Grid item xs={12} md={6}>
          {result ? (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {/* Risk Score */}
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h6" gutterBottom>
                    Risk Assessment
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="h2" color={`${getRiskColor(result.confidence_score)}.main`}>
                      {(result.confidence_score * 100).toFixed(1)}%
                    </Typography>
                    <Chip
                      label={getRiskLevel(result.confidence_score)}
                      color={getRiskColor(result.confidence_score)}
                      size="large"
                      sx={{ mt: 1 }}
                    />
                  </Box>
                </CardContent>
              </Card>

              {/* Recommendation */}
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Recommendation
                  </Typography>
                  <Alert severity={result.is_fraud ? 'error' : 'success'}>
                    {result.recommendation}
                  </Alert>
                </CardContent>
              </Card>

              {/* Risk Factors */}
              {result.risk_factors && result.risk_factors.length > 0 && (
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Risk Factors
                    </Typography>
                    <List dense>
                      {result.risk_factors.map((factor, index) => (
                        <ListItem key={index}>
                          <ListItemText primary={`• ${factor}`} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              )}

              {/* Action Buttons */}
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Actions
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Button
                      variant="contained"
                      color="success"
                      startIcon={<CheckCircle />}
                      onClick={() => alert('Transaction approved')}
                    >
                      Approve
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      startIcon={<Block />}
                      onClick={() => alert('Transaction blocked')}
                    >
                      Block
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() => alert('Marked for review')}
                    >
                      Review
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          ) : (
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 8 }}>
                <Security sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  Enter transaction details to analyze for fraud
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}

export default FraudAnalysis;