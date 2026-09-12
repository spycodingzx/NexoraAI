# 🐳 Docker Deployment Guide

Complete guide for running Autonomous Business Platform Pro with Docker.

## Quick Start

### 1. Build the Image

```bash
docker build -t nova-system .
```

Build time: ~10-15 minutes (depending on internet speed)

### 2. Run the Container

**Simple run with env file:**
```bash
docker run -p 8501:8501 --env-file .env nova-system
```

**With persistent data volumes:**
```bash
docker run -p 8501:8501 --env-file .env \
  -v $(pwd)/campaigns:/core/campaigns \
  -v $(pwd)/sessions:/core/sessions \
  -v $(pwd)/workflows:/core/workflows \
  nova-system
```

**Background mode (detached):**
```bash
docker run -d -p 8501:8501 --env-file .env \
  --name business-platform \
  nova-system
```

### 3. Access the Platform

Open your browser to: **http://localhost:8501**

---

## Docker Compose (Recommended)

Docker Compose simplifies deployment and management.

### Start the Platform

```bash
docker-compose up -d
```

### View Logs

```bash
docker-compose logs -f
```

### Stop the Platform

```bash
docker-compose down
```

### Rebuild and Restart

```bash
docker-compose up -d --build
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root with your API keys:

```bash
# Required
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxx

# Optional integrations
PRINTIFY_API_TOKEN=your_token
SHOPIFY_API_KEY=your_key
PINTEREST_USERNAME=your_email
PINTEREST_PASSWORD=your_password
```

See `.env.example` for all available options.

### Volume Mounts

The following directories are mounted for persistent data:

- `campaigns/` - Generated marketing campaigns
- `sessions/` - User sessions and chat history
- `workflows/` - Custom automation workflows
- `task_artifacts/` - Task queue outputs
- `runs/` - Execution logs

---

## Docker Commands Reference

### Building

```bash
# Standard build
docker build -t nova-system .

# Build with custom tag
docker build -t my-platform:v1.0 .

# Build without cache (force fresh build)
docker build --no-cache -t nova-system .
```

### Running

```bash
# Run on custom port (8080 instead of 8501)
docker run -p 8080:8501 --env-file .env nova-system

# Run with interactive terminal
docker run -it -p 8501:8501 --env-file .env nova-system

# Run with resource limits
docker run -p 8501:8501 --env-file .env \
  --memory="8g" --cpus="4" \
  nova-system

# Run with YouTube credentials
docker run -p 8501:8501 --env-file .env \
  -v $(pwd)/token.pickle:/core/token.pickle:ro \
  nova-system
```

### Container Management

```bash
# List running containers
docker ps

# Stop nv_container
docker stop business-platform

# Start stopped nv_container
docker start business-platform

# Restart nv_container
docker restart business-platform

# Remove nv_container
docker rm business-platform

# View nv_container logs
docker logs business-platform

# Follow logs in real-time
docker logs -f business-platform

# Execute command in running nv_container
docker exec -it business-platform /bin/bash

# Check nv_container resource usage
docker stats business-platform
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi nova-system

# Prune unused images
docker image prune -a

# Save image to file
docker save nova-system > platform.tar

# Load image from file
docker load < platform.tar

# Tag image for registry
docker tag nova-system username/platform:latest
```

---

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs business-platform
```

**Common issues:**
- Missing `.env` file → Create from `.env.example`
- Port already in use → Use different port: `-p 8080:8501`
- Insufficient memory → Increase Docker memory limit

### Permission Issues

```bash
# Fix volume permissions
sudo chown -R 1000:1000 campaigns/ sessions/ workflows/
```

### Memory Issues

```bash
# Increase memory limit
docker run -p 8501:8501 --env-file .env \
  --memory="16g" --memory-swap="16g" \
  nova-system
```

### Rebuild After Code Changes

```bash
# Stop and remove nv_container
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

---

## Production Deployment

### Using Docker Compose in Production

**docker-compose.prod.yml:**
```yaml
version: '3.8'
services:
  core:
    image: nova-system:latest
    restart: always
    ports:
      - "8501:8501"
    env_file:
      - .env.production
    volumes:
      - core-campaigns:/core/campaigns
      - core-sessions:/core/sessions
      - core-workflows:/core/workflows
    deploy:
      resources:
        limits:
          cpus: '8.0'
          memory: 16G
        reservations:
          cpus: '4.0'
          memory: 8G
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"

volumes:
  core-campaigns:
  core-sessions:
  core-workflows:
```

**Start production:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Behind Nginx Reverse Proxy

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### With SSL (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Sharing Your Docker Image

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag nova-system username/business-platform:latest

# Push to Docker Hub
docker push username/business-platform:latest
```

### Share as File

```bash
# Export image
docker save nova-system | gzip > business-platform.tar.gz

# Import on another system
gunzip -c business-platform.tar.gz | docker load
```

### Create GitHub Container Registry

```bash
# Tag for GitHub
docker tag nova-system ghcr.io/username/business-platform:latest

# Login to GitHub
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push to GitHub
docker push ghcr.io/username/business-platform:latest
```

---

## Health Checks

The nv_container includes automatic health checks:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' business-platform

# View health log
docker inspect --format='{{json .State.Health}}' business-platform | jq
```

---

## Performance Optimization

### Multi-stage Build Benefits

The Dockerfile uses multi-stage builds to:
- Reduce image size (~2GB vs ~5GB)
- Improve security (no build tools in final image)
- Faster nv_container startup

### Resource Recommendations

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Disk: 10GB

**Recommended:**
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 50GB+

**Production:**
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 100GB+
- SSD storage

---

## Security Best Practices

1. **Never commit .env files**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use secrets management in production**
   ```bash
   docker secret create replicate_token replicate_token.txt
   ```

3. **Run as non-root user** (already configured in Dockerfile)

4. **Keep base image updated**
   ```bash
   docker pull python:3.11-slim
   docker build --no-cache -t nova-system .
   ```

5. **Scan for vulnerabilities**
   ```bash
   docker scan nova-system
   ```

---

## Monitoring

### Container Stats

```bash
# Real-time stats
docker stats business-platform

# Container resource usage
docker exec business-platform top

# Disk usage
docker exec business-platform df -h
```

### Logs

```bash
# Last 100 lines
docker logs --tail 100 business-platform

# Since timestamp
docker logs --since 2023-12-01T00:00:00 business-platform

# Filter logs
docker logs business-platform 2>&1 | grep ERROR
```

---

## Backup and Recovery

### Backup Volumes

```bash
# Backup campaigns
docker run --rm \
  -v nova-system_campaigns:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/campaigns-backup.tar.gz /data

# Backup all data
docker-compose down
tar czf backup-$(date +%Y%m%d).tar.gz campaigns/ sessions/ workflows/
```

### Restore Volumes

```bash
# Restore campaigns
docker run --rm \
  -v nova-system_campaigns:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/campaigns-backup.tar.gz -C /
```

---

## Upgrading

### Pull Latest Image

```bash
# Pull from Docker Hub
docker pull username/business-platform:latest

# Restart with new image
docker-compose pull
docker-compose up -d
```

### Upgrade from Local Build

```bash
# Rebuild image
docker-compose build --no-cache

# Restart services
docker-compose up -d
```

---

## Development Mode

### Live Code Reloading

```bash
# Mount source code for development
docker run -p 8501:8501 --env-file .env \
  -v $(pwd):/core \
  nova-system
```

**Note:** Streamlit auto-reloads on file changes.

### Debug Mode

```bash
# Run with interactive shell
docker run -it -p 8501:8501 --env-file .env \
  --entrypoint /bin/bash \
  nova-system

# Inside nv_container:
streamlit run nova_system.py --server.runOnSave true
```

---

## FAQs

**Q: How big is the Docker image?**
A: ~2-3GB (optimized with multi-stage build)

**Q: Can I run multiple instances?**
A: Yes, use different ports: `-p 8502:8501`, `-p 8503:8501`, etc.

**Q: Does it work on Apple Silicon (M1/M2)?**
A: Yes, Docker automatically handles platform compatibility.

**Q: Can I use GPU acceleration?**
A: Possible but not required - all AI models run via Replicate API.

**Q: How do I update environment variables?**
A: Update `.env` file and restart: `docker-compose restart`

---

**Need Help?** Check the main [README.md](README.md) or open an issue on GitHub.
