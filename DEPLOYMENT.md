# Deployment Guide
## AI-Based Question Paper Moderation System

This guide provides comprehensive instructions for deploying the system in various environments.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)

---

## Prerequisites

### Required Software
- Python 3.8 or higher
- Node.js 16+ and npm (for frontend)
- Git (optional, for version control)

### System Requirements
- Minimum 2GB RAM
- 1GB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## Local Development

### Backend Setup

1. **Clone or download the project**
   ```bash
   cd Project
   ```

2. **Install Python dependencies**
   
   **Windows:**
   ```bash
   python -m pip install -r requirements.txt
   ```
   
   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python -c "from core.database import Database; db = Database(); db.initialize()"
   ```

4. **Run the backend server**
   ```bash
   python run.py
   ```
   
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm start
   ```
   
   The frontend will open at `http://localhost:3000`

---

## Production Deployment

### Building for Production

1. **Build the frontend**
   ```bash
   cd frontend
   npm run build
   ```
   
   This creates an optimized production build in `frontend/build/`

2. **Configure environment variables**
   
   Copy `.env.example` to `.env` and update:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key-here
   PORT=5000
   DEBUG=False
   ```

3. **Run production server**
   ```bash
   python run.py
   ```

### Using Gunicorn (Linux/Mac)

For better performance in production:

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

### Using Waitress (Windows)

For Windows production deployment:

1. **Install Waitress**
   ```bash
   pip install waitress
   ```

2. **Run with Waitress**
   ```bash
   waitress-serve --host=0.0.0.0 --port=5000 backend.app:app
   ```

---

## Docker Deployment

### Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data uploads logs

# Initialize database
RUN python -c "from core.database import Database; db = Database(); db.initialize()"

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "run.py"]
```

### Build and Run

```bash
# Build image
docker build -t question-paper-moderator .

# Run container
docker run -d -p 5000:5000 -v $(pwd)/data:/app/data question-paper-moderator
```

---

## Cloud Deployment

### Heroku Deployment

1. **Create `Procfile`**
   ```
   web: gunicorn backend.app:app
   ```

2. **Create `runtime.txt`**
   ```
   python-3.10.12
   ```

3. **Deploy to Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### AWS Deployment (EC2)

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **SSH into instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx -y
   ```

4. **Clone repository and setup**
   ```bash
   git clone your-repo-url
   cd Project
   pip3 install -r requirements.txt
   python3 -c "from core.database import Database; db = Database(); db.initialize()"
   ```

5. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
   ```

6. **Configure Nginx** (optional, for reverse proxy)
   
   Create `/etc/nginx/sites-available/moderator`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

---

## Testing the Deployment

### Health Check
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "version": "1.0.0"
}
```

### Upload Test
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@draft_paper.txt" \
  -F "professor_name=Test Professor" \
  -F "subject=Computer Science"
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in .env or run command
   PORT=8000 python run.py
   ```

2. **Database locked**
   ```bash
   # Remove database and reinitialize
   rm data/moderation.db
   python -c "from core.database import Database; db = Database(); db.initialize()"
   ```

3. **Permission errors (Linux)**
   ```bash
   chmod +x install.sh
   chmod +x run.py
   ```

---

## Security Considerations

### Production Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Configure CORS properly (not `*` in production)
- [ ] Use HTTPS (SSL certificate)
- [ ] Set up firewall rules
- [ ] Regular backups of database
- [ ] Monitor logs for errors
- [ ] Keep dependencies updated

---

## Maintenance

### Database Backup
```bash
cp data/moderation.db data/backup_$(date +%Y%m%d).db
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### View Logs
```bash
tail -f logs/app.log
```

---

## Support

For issues or questions:
- Check existing documentation
- Review error logs in `logs/` directory
- Ensure all dependencies are installed correctly

---

**Last Updated:** 2024
**Version:** 1.0.0
