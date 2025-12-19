```js
const path = require('path');
const dotenv = require('dotenv');

// Determine environment
const environment = process.env.NODE_ENV || 'development';

// Load environment-specific .env file
const envPath = path.resolve(__dirname, `../../config/.env.${environment}`);

// Load the .env file
const result = dotenv.config({ path: envPath });

if (result.error) {
  console.error(`Error loading .env file for ${environment}:`, result.error);
  process.exit(1);
}

// Validate required environment variables
const requiredEnvVars = [
  'NODE_ENV',
  'PORT',
  'DB_HOST',
  'DB_PORT',
  'DB_NAME',
  'DB_USER',
  'DB_PASSWORD',
  'JWT_SECRET'
];

const missingEnvVars = requiredEnvVars.filter(envVar => !process.env[envVar]);

if (missingEnvVars.length > 0) {
  console.error('Missing required environment variables:', missingEnvVars.join(', '));
  process.exit(1);
}

// Export configuration object
const config = {
  env: environment,
  isProduction: environment === 'production',
  isDevelopment: environment === 'development',
  isTest: environment === 'test',
  
  app: {
    port: parseInt(process.env.PORT, 10),
    apiVersion: process.env.API_VERSION || 'v1',
  },
  
  database: {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT, 10),
    name: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
  },
  
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT, 10),
  },
  
  jwt: {
    secret: process.env.JWT_SECRET,
    expire: process.env.JWT_EXPIRE || '7d',
  },
  
  logging: {
    level: process.env.LOG_LEVEL || 'info',
  },
  
  externalApi: {
    key: process.env.EXTERNAL_API_KEY,
  },
};

// Freeze config to prevent modifications
Object.freeze(config);

module.exports = config;
```