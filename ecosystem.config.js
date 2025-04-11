module.exports = {
  apps: [
    {
      name: 'adneura-server',
      script: '/root/adneura/venv/bin/python',
      args: '/root/adneura/manage.py runserver 0.0.0.0:8000',
      interpreter: 'none', // Ensures PM2 doesn't try to use a Node.js interpreter
      cwd: '/root/adneura', // Optional: Working directory
      watch: false, // Set to true if you want PM2 to watch for changes
      autorestart: true, // Automatically restart on crash
    },
  ],
};

