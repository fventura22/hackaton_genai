import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';
const USER_SERVICE_URL = process.env.REACT_APP_USER_SERVICE_URL || '/api';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
    });
    
    this.userClient = axios.create({
      baseURL: USER_SERVICE_URL,
      timeout: 10000,
    });
    
    this.token = null;
  }

  setAuthToken(token) {
    this.token = token;
    if (token) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      this.userClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete this.client.defaults.headers.common['Authorization'];
      delete this.userClient.defaults.headers.common['Authorization'];
    }
  }

  async login(username, password) {
    try {
      const response = await this.userClient.post('/login', {
        username,
        password
      });
      
      if (response.data.access_token) {
        this.setAuthToken(response.data.access_token);
        return { success: true, token: response.data.access_token };
      }
      
      return { success: false, error: 'Invalid response' };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  }

  async analyzeFraud(transactionData) {
    try {
      const response = await this.client.post('/analyze-fraud', {
        customer_id: transactionData.customerId,
        transaction_id: transactionData.transactionId,
        transaction_data: {
          amount: parseFloat(transactionData.amount),
          timestamp: new Date().toISOString(),
          location: transactionData.location,
          merchant_category: transactionData.merchantCategory,
          description: transactionData.description
        }
      });

      return { success: true, data: response.data };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Analysis failed' 
      };
    }
  }

  async getHealthStatus() {
    try {
      const response = await this.client.get('/health');
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: 'Health check failed' };
    }
  }

  async getUserProfile() {
    try {
      const response = await this.userClient.get('/profile');
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: 'Failed to get profile' };
    }
  }
}

export default new ApiService();