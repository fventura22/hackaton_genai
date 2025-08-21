class CognitoService {
  constructor() {
    this.userPoolId = process.env.REACT_APP_COGNITO_USER_POOL_ID || 'us-east-1_XXXXXXXXX';
    this.clientId = process.env.REACT_APP_COGNITO_CLIENT_ID || 'your-client-id';
    this.region = process.env.REACT_APP_AWS_REGION || 'us-east-1';
  }

  async login(username, password) {
    // Simple demo authentication
    if (username === 'demo' && password === 'demo') {
      const mockUser = {
        username: 'demo',
        email: 'demo@example.com',
        'cognito:groups': ['analyst']
      };
      
      localStorage.setItem('accessToken', 'demo-token');
      localStorage.setItem('userInfo', JSON.stringify(mockUser));
      
      return {
        success: true,
        user: mockUser
      };
    }
    
    return { success: false, error: 'Invalid credentials' };
  }

  decodeToken(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      
      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Token decode error:', error);
      return null;
    }
  }

  getCurrentUser() {
    const userInfo = localStorage.getItem('userInfo');
    return userInfo ? JSON.parse(userInfo) : null;
  }

  getAccessToken() {
    return localStorage.getItem('accessToken');
  }

  getUserGroups() {
    const user = this.getCurrentUser();
    return user?.['cognito:groups'] || [];
  }

  isAdmin() {
    return this.getUserGroups().includes('admin');
  }

  isAnalyst() {
    return this.getUserGroups().includes('analyst');
  }

  isAuthenticated() {
    const token = this.getAccessToken();
    if (!token) return false;
    
    try {
      const decoded = this.decodeToken(token);
      return decoded && decoded.exp > Date.now() / 1000;
    } catch {
      return false;
    }
  }

  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('idToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userInfo');
  }
}

export default new CognitoService();