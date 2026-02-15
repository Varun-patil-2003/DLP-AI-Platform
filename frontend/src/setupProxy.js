/**
 * Development proxy configuration
 * Routes API requests to Flask backend
 * Works for both localhost and network access
 */

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
      logLevel: 'debug',
      onError: function(err, req, res) {
        console.log('Proxy Error:', err);
      }
    })
  );
};
