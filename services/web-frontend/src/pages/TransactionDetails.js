import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Paper
} from '@mui/material';
import { CheckCircle, Block, Visibility } from '@mui/icons-material';
import { useParams } from 'react-router-dom';

function TransactionDetails() {
  const { id } = useParams();

  // Mock data - in real app, fetch based on ID
  const transactionData = {
    id: id,
    customerId: 'CUST001',
    transactionId: 'TXN001',
    amount: 5000,
    riskScore: 0.85,
    timestamp: '2024-01-15T14:30:00Z',
    merchant: 'Online Electronics Store',
    merchantCategory: 'Electronics',
    paymentMethod: 'Credit Card',
    cardLast4: '4532',
    location: 'New York, NY',
    ipAddress: '192.168.1.100',
    deviceType: 'Mobile',
    status: 'Under Review'
  };

  const riskFactors = [
    'High transaction amount ($5,000)',
    'New merchant for customer',
    'Unusual time of transaction (2:30 AM)',
    'Different location than usual patterns',
    'Mobile device with new fingerprint'
  ];

  const customerProfile = {
    accountAge: '2 years',
    averageTransaction: '$150',
    frequentLocations: ['Boston, MA', 'New York, NY'],
    riskHistory: 'Low',
    totalTransactions: 247,
    fraudHistory: 0
  };

  const getRiskColor = (riskScore) => {
    if (riskScore >= 0.8) return 'error';
    if (riskScore >= 0.6) return 'warning';
    return 'info';
  };

  const getRiskLevel = (score) => {
    if (score >= 0.8) return 'HIGH RISK';
    if (score >= 0.6) return 'MEDIUM RISK';
    return 'LOW RISK';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Transaction Details
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Detailed analysis for transaction {transactionData.transactionId}
      </Typography>

      <Grid container spacing={3}>
        {/* Transaction Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Transaction Overview
              </Typography>
              
              <TableContainer>
                <Table size="small">
                  <TableBody>
                    <TableRow>
                      <TableCell><strong>Customer ID</strong></TableCell>
                      <TableCell>{transactionData.customerId}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Transaction ID</strong></TableCell>
                      <TableCell>{transactionData.transactionId}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Amount</strong></TableCell>
                      <TableCell>
                        <Typography variant="h6" color="primary">
                          ${transactionData.amount.toLocaleString()}
                        </Typography>
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Risk Score</strong></TableCell>
                      <TableCell>
                        <Chip
                          label={`${(transactionData.riskScore * 100).toFixed(0)}% - ${getRiskLevel(transactionData.riskScore)}`}
                          color={getRiskColor(transactionData.riskScore)}
                        />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Status</strong></TableCell>
                      <TableCell>
                        <Chip label={transactionData.status} color="warning" />
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Transaction Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Transaction Information
              </Typography>
              
              <TableContainer>
                <Table size="small">
                  <TableBody>
                    <TableRow>
                      <TableCell><strong>Timestamp</strong></TableCell>
                      <TableCell>
                        {new Date(transactionData.timestamp).toLocaleString()}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Merchant</strong></TableCell>
                      <TableCell>{transactionData.merchant}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Category</strong></TableCell>
                      <TableCell>{transactionData.merchantCategory}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Payment Method</strong></TableCell>
                      <TableCell>
                        {transactionData.paymentMethod} ****{transactionData.cardLast4}
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Location</strong></TableCell>
                      <TableCell>{transactionData.location}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Device</strong></TableCell>
                      <TableCell>{transactionData.deviceType}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Risk Factors */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Risk Factors Detected
              </Typography>
              
              <List>
                {riskFactors.map((factor, index) => (
                  <ListItem key={index} sx={{ py: 0.5 }}>
                    <ListItemText 
                      primary={`• ${factor}`}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Customer Profile */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Customer Profile
              </Typography>
              
              <TableContainer>
                <Table size="small">
                  <TableBody>
                    <TableRow>
                      <TableCell><strong>Account Age</strong></TableCell>
                      <TableCell>{customerProfile.accountAge}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Average Transaction</strong></TableCell>
                      <TableCell>{customerProfile.averageTransaction}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Total Transactions</strong></TableCell>
                      <TableCell>{customerProfile.totalTransactions}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Fraud History</strong></TableCell>
                      <TableCell>
                        <Chip 
                          label={customerProfile.fraudHistory === 0 ? 'Clean' : customerProfile.fraudHistory}
                          color={customerProfile.fraudHistory === 0 ? 'success' : 'error'}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell><strong>Frequent Locations</strong></TableCell>
                      <TableCell>
                        {customerProfile.frequentLocations.join(', ')}
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Actions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Decision Actions
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  color="success"
                  size="large"
                  startIcon={<CheckCircle />}
                  onClick={() => alert('Transaction approved')}
                >
                  Approve Transaction
                </Button>
                
                <Button
                  variant="contained"
                  color="error"
                  size="large"
                  startIcon={<Block />}
                  onClick={() => alert('Transaction blocked')}
                >
                  Block Transaction
                </Button>
                
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<Visibility />}
                  onClick={() => alert('Marked for further review')}
                >
                  Request Review
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default TransactionDetails;