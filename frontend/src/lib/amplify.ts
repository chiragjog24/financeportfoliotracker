import { Amplify } from 'aws-amplify'

const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
      userPoolClientId: import.meta.env.VITE_COGNITO_APP_CLIENT_ID || '',
      region: import.meta.env.VITE_AWS_REGION || 'us-east-1',
      loginWith: {
        email: true,
        username: false,
      },
      signUpVerificationMethod: 'code',
    },
  },
}

Amplify.configure(amplifyConfig)

export default amplifyConfig
