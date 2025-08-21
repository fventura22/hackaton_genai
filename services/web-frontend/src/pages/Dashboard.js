import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  TrendingUp,
  Security,
  Warning,
  CheckCircle
} from '@mui/icons-material';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const stats = {
    totalTransactions: 1247,
    fraudDetected: 23,
    falsePositives: 5,
    accuracy: 98.2
  };

  const recentAlerts = [
    { id: 1, customerId: 'CUST001', amount: 5000, riskScore: 0.85, status: 'High Risk' },
    { id: 2, customerId: 'CUST002', amount: 1200, riskScore: 0.65, status: 'Medium Risk' },
    { id: 3, customerId: 'CUST003', amount: 850, riskScore: 0.55, status: 'Review Required' }
  ];

  const pieData = [
    { name: 'Safe', value: 1219, color: '#4caf50' },
    { name: 'Fraud', value: 23, color: '#f44336' },
    { name: 'Review', value: 5, color: '#ff9800' }
  ];

  const barData = [
    { name: 'Mon', transactions: 180, fraud: 3 },
    { name: 'Tue', transactions: 220, fraud: 5 },
    { name: 'Wed', transactions: 190, fraud: 2 },
    { name: 'Thu', transactions: 240, fraud: 4 },
    { name: 'Fri', transactions: 280, fraud: 6 },
    { name: 'Sat', transactions: 160, fraud: 2 },
    { name: 'Sun', transactions: 167, fraud: 1 }
  ];

  const getRiskColor = (riskScore) => {
    if (riskScore >= 0.8) return 'error';
    if (riskScore >= 0.6) return 'warning';
    return 'info';
  };

  const StatCard = ({ title, value, icon, color = 'primary' }) => (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
          </Box>
          <Box sx={{ color: `${color}.main` }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Fraud Detection Dashboard
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Real-time monitoring and analysis
      </Typography>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Transactions"
            value={stats.totalTransactions.toLocaleString()}
            icon={<TrendingUp sx={{ fontSize: 40 }} />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Fraud Detected"
            value={stats.fraudDetected}
            icon={<Security sx={{ fontSize: 40 }} />}
            color="error"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="False Positives"
            value={stats.falsePositives}
            icon={<Warning sx={{ fontSize: 40 }} />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Accuracy"
            value={`${stats.accuracy}%`}
            icon={<CheckCircle sx={{ fontSize: 40 }} />}
            color="success"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Charts */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Transaction Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Weekly Fraud Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={barData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="transactions" fill="#1976d2" name="Transactions" />
                  <Bar dataKey="fraud" fill="#f44336" name="Fraud" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => navigate('/analyze')}
                  sx={{ py: 1.5 }}
                >
                  Analyze New Transaction
                </Button>
                <Button
                  variant="outlined"
                  fullWidth
                  sx={{ py: 1.5 }}
                >
                  View Reports
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Alerts */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Alerts
              </Typography>
              <List>
                {recentAlerts.map((alert) => (
                  <ListItem
                    key={alert.id}
                    button
                    onClick={() => navigate(`/transaction/${alert.id}`)}
                    sx={{ border: 1, borderColor: 'divider', borderRadius: 1, mb: 1 }}
                  >
                    <ListItemText
                      primary={alert.customerId}
                      secondary={`$${alert.amount.toLocaleString()}`}
                    />
                    <ListItemSecondaryAction>
                      <Chip
                        label={`${(alert.riskScore * 100).toFixed(0)}%`}
                        color={getRiskColor(alert.riskScore)}
                        size="small"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;