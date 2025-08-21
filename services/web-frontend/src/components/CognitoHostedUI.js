import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

const CognitoHostedUI = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if we're returning from Cognito
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const error = urlParams.get('error');

    if (code) {
      // Exchange code for tokens
      exchangeCodeForTokens(code);
    } else if (error) {
      console.error('Cognito error:', error);
      setLoading(false);
    } else {
      // Redirect to Cognito Hosted UI
      redirectToCognito();
    }
  }, []);

  const redirectToCognito = () => {
    const cognitoDomain = process.env.REACT_APP_COGNITO_DOMAIN;
    const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
    const redirectUri = encodeURIComponent(window.location.origin + '/callback');
    
    const cognitoUrl = `https://${cognitoDomain}/login?client_id=${clientId}&response_type=code&scope=openid+email+profile&redirect_uri=${redirectUri}`;
    
    window.location.href = cognitoUrl;
  };

  const exchangeCodeForTokens = async (code) => {
    try {
      const cognitoDomain = process.env.REACT_APP_COGNITO_DOMAIN;
      const clientId = process.env.REACT_APP_COGNITO_CLIENT_ID;
      const redirectUri = window.location.origin + '/callback';

      const response = await fetch(`https://${cognitoDomain}/oauth2/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          grant_type: 'authorization_code',
          client_id: clientId,
          code: code,
          redirect_uri: redirectUri,
        }),
      });

      if (response.ok) {
        const tokens = await response.json();
        
        // Store tokens
        localStorage.setItem('accessToken', tokens.access_token);
        localStorage.setItem('idToken', tokens.id_token);
        localStorage.setItem('refreshToken', tokens.refresh_token);
        
        // Decode user info from ID token
        const userInfo = JSON.parse(atob(tokens.id_token.split('.')[1]));
        localStorage.setItem('userInfo', JSON.stringify(userInfo));
        
        // Redirect to main app
        window.location.href = '/dashboard';
      } else {
        console.error('Token exchange failed');
        setLoading(false);
      }
    } catch (error) {
      console.error('Token exchange error:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          gap: 2
        }}
      >
        <CircularProgress size={60} />
        <Typography variant="h6">
          Authenticating with Cognito...
        </Typography>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        gap: 2
      }}
    >
      <Typography variant="h6" color="error">
        Authentication failed. Please try again.
      </Typography>
    </Box>
  );
};

export default CognitoHostedUI;