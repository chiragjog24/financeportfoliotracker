export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export const APP_NAME = 'Finance Portfolio Tracker'
export const APP_VERSION = '1.0.0'

// AWS Cognito configuration (set via environment variables)
export const COGNITO_CONFIG = {
  userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
  appClientId: import.meta.env.VITE_COGNITO_APP_CLIENT_ID || '',
  region: import.meta.env.VITE_AWS_REGION || 'us-east-1',
}
