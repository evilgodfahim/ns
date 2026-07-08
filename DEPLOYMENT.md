# Deployment Guide

Multiple ways to deploy your New Scientist RSS feed scraper.

## 🌐 Option 1: GitHub Pages (Recommended)

**Free, automatic updates, no server needed**

### Setup Steps:

1. **Fork/Create Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
   cd newscientist-rss-scraper
   git remote set-url origin https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
   git push -u origin main
   ```

2. **Enable GitHub Actions**
   - Settings → Actions → General
   - Workflow permissions: "Read and write permissions"
   - Save

3. **Run First Scrape**
   - Actions tab → "Update RSS Feed"
   - "Run workflow" → "Run workflow"

4. **Enable GitHub Pages**
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages → / (root)
   - Save

5. **Access Feed**
   - Feed: `https://YOUR_USERNAME.github.io/newscientist-rss-scraper/feed.xml`
   - Web: `https://YOUR_USERNAME.github.io/newscientist-rss-scraper/`

**Pros:** Free, automatic, no maintenance, SSL
**Cons:** Public repository required

---

## 🐳 Option 2: Docker (Self-Hosted)

**Full control, private, can run anywhere, includes FlareSolverr for Cloudflare bypass**

### Quick Start:

```bash
# Build and run with docker-compose (includes FlareSolverr)
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f scraper
docker-compose logs -f flaresolverr

# Access feed at http://localhost:8080/feed.xml
```

This starts three services:
1. **FlareSolverr** - Bypasses Cloudflare protection (port 8191)
2. **Scraper** - Fetches articles and generates RSS
3. **Nginx** - Serves the feed (port 8080)

### Manual Docker:

```bash
# Start FlareSolverr first
docker run -d \
  --name byparr \
  -p 8191:8191 \
  ghcr.io/thephaseless/byparr:latest

# Build scraper image
docker build -t newscientist-scraper .

# Run scraper with FlareSolverr
docker run -v $(pwd):/app \
  -e FLARESOLVERR_URL=http://localhost:8191/v1 \
  newscientist-scraper

# Serve with nginx
docker run -d -p 8080:80 \
  -v $(pwd)/feed.xml:/usr/share/nginx/html/feed.xml:ro \
  -v $(pwd)/index.html:/usr/share/nginx/html/index.html:ro \
  nginx:alpine
```

### Automated Updates with Cron:

```bash
# Add to crontab (crontab -e)
0 6 * * * cd /path/to/newscientist-rss-scraper && docker-compose up scraper
```

**Pros:** Full control, private, portable, Cloudflare bypass included
**Cons:** Requires server/VPS, manual setup

---

## ☁️ Option 3: Cloud Platforms

### Heroku

```bash
# Install Heroku CLI
heroku login
heroku create newscientist-rss

# Add Procfile
echo "web: python -m http.server 8000" > Procfile
echo "worker: python scraper.py" >> Procfile

# Deploy
git push heroku main

# Add scheduler
heroku addons:create scheduler:standard
# Configure to run: python scraper.py
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `python scraper.py && python -m http.server 8080`
4. Add cron job via GitHub Actions

### Railway

1. Connect GitHub repo
2. Auto-detects Python
3. Add cron via GitHub Actions
4. Serves static files automatically

**Pros:** Managed, scalable, SSL included
**Cons:** May cost money, vendor lock-in

---

## 💻 Option 4: VPS (Linux Server)

**Traditional server deployment with FlareSolverr**

### Setup:

```bash
# SSH into server
ssh user@your-server.com

# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nginx docker.io -y

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Run FlareSolverr
sudo docker run -d \
  --name byparr \
  --restart unless-stopped \
  -p 8191:8191 \
  ghcr.io/thephaseless/byparr:latest

# Clone repository
git clone https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
cd newscientist-rss-scraper

# Install Python packages
pip3 install -r requirements.txt

# Run scraper
FLARESOLVERR_URL=http://localhost:8191/v1 python3 scraper.py

# Configure nginx
sudo cp nginx.conf /etc/nginx/sites-available/newscientist-rss
sudo ln -s /etc/nginx/sites-available/newscientist-rss /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Add to crontab
crontab -e
# Add: 0 6 * * * cd /path/to/newscientist-rss-scraper && FLARESOLVERR_URL=http://localhost:8191/v1 python3 scraper.py
```

**Pros:** Full control, cheap ($5/mo), customizable, Cloudflare bypass
**Cons:** Requires Linux knowledge, manual updates

---

## 🏠 Option 5: Home Server / Raspberry Pi

**Run locally on your network**

### Setup on Raspberry Pi:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip git nginx -y

# Clone and setup
git clone https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
cd newscientist-rss-scraper
pip3 install -r requirements.txt

# Test run
python3 scraper.py

# Setup systemd service
sudo nano /etc/systemd/system/newscientist-rss.service
```

Service file:
```ini
[Unit]
Description=New Scientist RSS Scraper
After=network.target

[Service]
Type=oneshot
User=pi
WorkingDirectory=/home/pi/newscientist-rss-scraper
ExecStart=/usr/bin/python3 scraper.py

[Install]
WantedBy=multi-user.target
```

Setup timer:
```bash
sudo nano /etc/systemd/system/newscientist-rss.timer
```

```ini
[Unit]
Description=Run New Scientist RSS Scraper Daily

[Timer]
OnCalendar=daily
OnCalendar=06:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
sudo systemctl enable newscientist-rss.timer
sudo systemctl start newscientist-rss.timer
```

**Pros:** Free, private, full control
**Cons:** Requires hardware, local network only (unless port forwarded)

---

## 📊 Comparison Table

| Method | Cost | Ease | Auto-Update | Public | SSL |
|--------|------|------|-------------|--------|-----|
| GitHub Pages | Free | ⭐⭐⭐⭐⭐ | ✅ | Yes | ✅ |
| Docker | $5-20/mo | ⭐⭐⭐ | Manual | No | Manual |
| Heroku | $7/mo | ⭐⭐⭐⭐ | ✅ | Optional | ✅ |
| VPS | $5/mo | ⭐⭐ | Manual | Yes | Manual |
| Home Server | Free | ⭐⭐ | Manual | No | No |

---

## 🔒 Security Considerations

### For Public Deployments:
- Keep repository public (GitHub Pages requirement)
- No sensitive data in code
- Rate limit scraping (currently 1x/day)
- Respect robots.txt

### For Private Deployments:
- Use environment variables for configs
- Enable firewall on VPS
- Use HTTPS (Let's Encrypt)
- Regular security updates

---

## 🔄 Updating Your Deployment

### GitHub Pages:
```bash
git pull origin main
git push origin main
# GitHub Actions handles the rest
```

### Docker:
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### VPS:
```bash
git pull origin main
pip3 install -r requirements.txt --upgrade
sudo systemctl restart nginx
```

---

## 📈 Monitoring

### Check Feed Health:
```bash
# Validate XML
python validate_feed.py

# Check feed size
ls -lh feed.xml

# Test HTTP access
curl -I http://localhost:8080/feed.xml
```

### GitHub Actions:
- Check Actions tab for workflow status
- Email notifications for failures
- View logs for debugging

### Server Monitoring:
- Use `cron` logs: `grep CRON /var/log/syslog`
- Check disk space: `df -h`
- Monitor nginx: `sudo tail -f /var/log/nginx/access.log`

---

## 🆘 Troubleshooting

### GitHub Actions failing?
1. Check workflow permissions
2. View action logs
3. Verify gh-pages branch exists

### Feed not updating?
1. Run manually: `python scraper.py`
2. Check for errors
3. Verify website structure hasn't changed

### Docker issues?
1. Check logs: `docker-compose logs scraper`
2. Rebuild: `docker-compose up --build`
3. Verify volume mounts

---

Choose the deployment method that best fits your needs and technical comfort level!
