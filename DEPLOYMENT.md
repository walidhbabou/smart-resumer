# Deployment Guide

This guide covers deploying SmartResume Analyzer to various cloud platforms.

---

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [AWS Deployment](#aws-deployment)
- [Railway Deployment](#railway-deployment)
- [Render Deployment](#render-deployment)
- [DigitalOcean Deployment](#digitalocean-deployment)
- [Environment Variables](#environment-variables)

---

## Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Domain name (optional, for production)

### Steps

1. **Clone and configure:**
   ```bash
   git clone <repository>
   cd smartresume-analyzer
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Build and run:**
   ```bash
   docker-compose up --build -d
   ```

3. **Verify:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

---

## AWS Deployment

### Option 1: ECS Fargate

1. **Build and push images to ECR:**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Build and tag images
   docker build -t smartresume-backend ./backend
   docker tag smartresume-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/smartresume-backend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/smartresume-backend:latest

   docker build -t smartresume-frontend ./frontend
   docker tag smartresume-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/smartresume-frontend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/smartresume-frontend:latest
   ```

2. **Create ECS Task Definitions:**
   - Define CPU and memory requirements
   - Set environment variables
   - Configure health checks

3. **Create ECS Service:**
   - Use Fargate launch type
   - Configure auto-scaling
   - Set up Application Load Balancer

4. **Configure ALB:**
   - Frontend on port 80/443
   - Backend on /api path

### Option 2: EC2 with Docker Compose

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **SSH into instance and setup:**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose git -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy application:**
   ```bash
   git clone <repository>
   cd smartresume-analyzer
   cp .env.example .env
   # Edit .env
   sudo docker-compose up -d
   ```

4. **Configure security group:**
   - Allow inbound on ports 80, 443, 8000, 3000

---

## Railway Deployment

Railway provides easy deployment from GitHub.

### Steps

1. **Sign up at [Railway.app](https://railway.app)**

2. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize and select your repository

3. **Configure Backend Service:**
   - Railway auto-detects Dockerfile
   - Set root directory: `backend`
   - Add environment variables:
     ```
     AI_PROVIDER=openai
     AI_API_KEY=your-key
     AI_MODEL=gpt-4
     ENVIRONMENT=production
     DEBUG=False
     CORS_ORIGINS=https://your-frontend-url.railway.app
     ```

4. **Configure Frontend Service:**
   - Add new service from same repo
   - Set root directory: `frontend`
   - Add environment variables:
     ```
     VITE_API_URL=https://your-backend-url.railway.app
     ```

5. **Generate domains:**
   - Railway provides automatic HTTPS domains
   - Update CORS_ORIGINS in backend with frontend domain

6. **Deploy:**
   - Automatic deployment on git push

---

## Render Deployment

### Backend Deployment

1. **Create Web Service:**
   - Connect GitHub repository
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment variables:**
   ```
   PYTHON_VERSION=3.11.0
   AI_PROVIDER=openai
   AI_API_KEY=your-key
   AI_MODEL=gpt-4
   ENVIRONMENT=production
   DEBUG=False
   ```

### Frontend Deployment

1. **Create Static Site:**
   - Connect GitHub repository
   - Root directory: `frontend`
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`

2. **Environment variables:**
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

3. **Configure rewrites:**
   Add `render.yaml` in frontend:
   ```yaml
   services:
     - type: web
       name: smartresume-frontend
       env: static
       buildCommand: npm install && npm run build
       staticPublishPath: dist
       routes:
         - type: rewrite
           source: /*
           destination: /index.html
   ```

---

## DigitalOcean Deployment

### App Platform

1. **Create new app:**
   - Connect GitHub repository
   - DigitalOcean auto-detects components

2. **Configure Backend:**
   - Type: Web Service
   - Dockerfile path: `backend/Dockerfile`
   - HTTP port: 8000
   - Environment variables (as above)

3. **Configure Frontend:**
   - Type: Static Site
   - Build command: `cd frontend && npm install && npm run build`
   - Output directory: `frontend/dist`

4. **Deploy:**
   - Auto-deploys on git push
   - Provides HTTPS by default

### Droplet (VPS)

1. **Create Droplet** (Ubuntu 22.04)

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose nginx certbot python3-certbot-nginx -y
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Deploy application:**
   ```bash
   git clone <repository>
   cd smartresume-analyzer
   cp .env.example .env
   # Edit .env
   docker-compose up -d
   ```

4. **Configure Nginx reverse proxy:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Setup SSL with Certbot:**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

---

## Environment Variables

### Production Environment Variables

**Backend:**
```bash
# Required
AI_PROVIDER=openai  # or anthropic
AI_API_KEY=your-production-api-key
ENVIRONMENT=production
DEBUG=False

# CORS - use production frontend URL
CORS_ORIGINS=https://yourdomain.com

# Optional
AI_MODEL=gpt-4
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.3
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10
```

**Frontend:**
```bash
# Required
VITE_API_URL=https://api.yourdomain.com
```

### Security Best Practices

1. **Never commit `.env` files**
2. **Use secrets management** (AWS Secrets Manager, etc.)
3. **Rotate API keys regularly**
4. **Use HTTPS in production**
5. **Set strong CORS policies**
6. **Enable rate limiting**
7. **Monitor logs for suspicious activity**

---

## Monitoring and Logs

### Docker Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### AWS CloudWatch
- Configure ECS to send logs to CloudWatch
- Set up alarms for errors

### Railway/Render
- Built-in log viewing in dashboard
- Metrics and monitoring included

---

## Scaling

### Horizontal Scaling
- Use container orchestration (ECS, Kubernetes)
- Configure auto-scaling based on CPU/memory

### Vertical Scaling
- Increase container resources
- Use larger instance types

### Database (if added)
- Use managed database services (RDS, MongoDB Atlas)
- Enable read replicas for scaling reads

---

## Backup and Disaster Recovery

1. **Regular backups** of configuration and data
2. **Version control** for code (Git)
3. **Database backups** (if applicable)
4. **Disaster recovery plan** documented
5. **Test restore procedures** regularly

---

## Health Checks

Both services include health check endpoints:

- Backend: `GET /health`
- Frontend: `GET /health` (via Nginx)

Configure your load balancer/orchestrator to use these endpoints.

---

## Support

For deployment issues, check:
- Application logs
- Service health endpoints
- Network/firewall configuration
- Environment variables
- API key validity

---

**Happy Deploying! 🚀**
