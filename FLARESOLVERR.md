# FlareSolverr Integration Guide

Complete guide to using FlareSolverr with the New Scientist RSS Scraper to bypass Cloudflare protection.

## 📖 Table of Contents
- [What is FlareSolverr?](#what-is-flaresolverr)
- [When Do You Need It?](#when-do-you-need-it)
- [Quick Start](#quick-start)
- [Setup Options](#setup-options)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Performance](#performance)

---

## What is FlareSolverr?

FlareSolverr is a proxy server that bypasses Cloudflare and other anti-bot protections by using a headless browser to solve challenges automatically.

**How it works:**
```
Your Scraper → FlareSolverr → Headless Chrome → Website
                              ↓ Solves Challenge
             ← Full HTML ←   ← 
```

---

## When Do You Need It?

✅ **Enable FlareSolverr if you see:**
- Cloudflare "Checking your browser" pages
- 403 Forbidden errors
- 503 Service Unavailable errors
- Captcha challenges
- Bot detection blocking

❌ **You don't need it if:**
- Scraper works fine without it
- You're getting 200 OK responses
- No blocking detected

**Default:** FlareSolverr is **disabled** for faster performance.

---

## Quick Start

### Docker Compose (Easiest)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Enable FlareSolverr
echo "FLARESOLVERR_ENABLED=true" > .env

# 3. Start everything
docker-compose up -d

# 4. Check logs
docker-compose logs -f scraper

# 5. Access feed
open http://localhost:8080/feed.xml
```

Done! FlareSolverr is now running on port 8191.

---

## Setup Options

### Option 1: Docker Compose ⭐ Recommended

**Pros:** Easy, automatic, everything included
**Cons:** Requires Docker

```bash
docker-compose up -d
```

Services started:
- ✅ FlareSolverr (port 8191)
- ✅ Scraper (with FlareSolverr)
- ✅ Nginx (port 8080)

### Option 2: Standalone FlareSolverr

**Pros:** Flexible, works with any setup
**Cons:** Manual configuration

```bash
# Start FlareSolverr
docker run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  ghcr.io/flaresolverr/flaresolverr:latest

# Configure scraper
export FLARESOLVERR_ENABLED=true
export FLARESOLVERR_URL=http://localhost:8191/v1

# Run scraper
python scraper.py
```

### Option 3: System Service (VPS/Server)

**Pros:** Production-ready, auto-start
**Cons:** Requires root access

Create `/etc/systemd/system/flaresolverr.service`:
```ini
[Unit]
Description=FlareSolverr
After=docker.service

[Service]
ExecStart=/usr/bin/docker run --rm --name=flaresolverr \
  -p 127.0.0.1:8191:8191 \
  ghcr.io/flaresolverr/flaresolverr:latest
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable flaresolverr
sudo systemctl start flaresolverr
```

### Option 4: GitHub Actions

**Disabled by default** to save time/resources.

To enable, edit `.github/workflows/update-feed.yml`:

```yaml
- name: Start FlareSolverr
  run: |
    docker run -d --name=flaresolverr \
      -p 8191:8191 \
      ghcr.io/flaresolverr/flaresolverr:latest
    sleep 10

- name: Set Environment
  run: |
    echo "FLARESOLVERR_ENABLED=true" >> $GITHUB_ENV
    echo "FLARESOLVERR_URL=http://localhost:8191/v1" >> $GITHUB_ENV
```

⚠️ This adds ~30s to each workflow run.

---

## Configuration

### Environment Variables (.env)

```bash
# Enable/Disable FlareSolverr
FLARESOLVERR_ENABLED=true

# FlareSolverr API endpoint
# Local: http://localhost:8191/v1
# Docker: http://flaresolverr:8191/v1
FLARESOLVERR_URL=http://localhost:8191/v1

# Max timeout (milliseconds)
FLARESOLVERR_TIMEOUT=60000

# User agent
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

### FlareSolverr Container Options

```yaml
environment:
  - LOG_LEVEL=info        # info, debug, error
  - LOG_HTML=false        # Log full HTML (verbose)
  - CAPTCHA_SOLVER=none   # Captcha solver type
  - TZ=UTC                # Timezone
```

---

## Troubleshooting

### Problem: Connection Refused

**Symptom:** `Failed to connect to localhost:8191`

**Solution:**
```bash
# Check if FlareSolverr is running
docker ps | grep flaresolverr

# Check if port is listening
curl http://localhost:8191/v1

# Restart FlareSolverr
docker restart flaresolverr
```

### Problem: Timeout Errors

**Symptom:** `FlareSolverr timeout on attempt X`

**Solution:**
```bash
# Increase timeout in .env
FLARESOLVERR_TIMEOUT=120000

# Or restart with more resources
docker restart flaresolverr
```

### Problem: Still Getting Blocked

**Symptom:** Cloudflare still blocking even with FlareSolverr

**Solutions:**
1. Update FlareSolverr:
   ```bash
   docker pull ghcr.io/flaresolverr/flaresolverr:latest
   docker-compose down
   docker-compose up -d
   ```

2. Change user agent in `.env`:
   ```bash
   USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
   ```

3. Check FlareSolverr logs:
   ```bash
   docker logs flaresolverr -f
   ```

### Problem: High Memory Usage

**Symptom:** FlareSolverr using too much RAM

**Solutions:**
```bash
# Limit memory in docker-compose.yml
services:
  flaresolverr:
    mem_limit: 1g
    memswap_limit: 1g
```

### Problem: Scraper Not Using FlareSolverr

**Symptom:** Logs show "Using direct HTTP requests"

**Check:**
```bash
# Verify .env settings
cat .env | grep FLARESOLVERR

# Should show:
# FLARESOLVERR_ENABLED=true (lowercase, no quotes)

# If wrong, fix:
sed -i 's/FLARESOLVERR_ENABLED=.*/FLARESOLVERR_ENABLED=true/' .env
```

---

## Performance

### Speed Comparison

| Method | Average Time | Success Rate |
|--------|-------------|--------------|
| Direct HTTP | 1-2 seconds | 60-70% |
| FlareSolverr | 10-30 seconds | 95-99% |

### Resource Usage

| Component | CPU | RAM | Disk |
|-----------|-----|-----|------|
| Scraper only | 10% | 50MB | 10MB |
| + FlareSolverr | 50% | 512MB | 500MB |

**Recommendation:** Use FlareSolverr only when needed.

---

## Testing FlareSolverr

### Test 1: Check if FlareSolverr is Running
```bash
curl http://localhost:8191/v1
```

Expected output:
```json
{"error":"Request is missing the cmd parameter"...}
```

### Test 2: Test Fetching a Page
```bash
curl -X POST http://localhost:8191/v1 \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://www.newscientist.com/issues/current/",
    "maxTimeout": 60000
  }' | jq '.status'
```

Expected: `"ok"`

### Test 3: Run Scraper with FlareSolverr
```bash
export FLARESOLVERR_ENABLED=true
python scraper.py
```

Look for:
```
FlareSolverr enabled at: http://localhost:8191/v1
FlareSolverr attempt 1/3...
✓ FlareSolverr successfully fetched page
```

---

## Security Notes

### 🔒 Never Expose FlareSolverr Publicly

FlareSolverr should ONLY be accessible locally:

✅ **Safe:**
```yaml
ports:
  - "127.0.0.1:8191:8191"  # Localhost only
```

❌ **Unsafe:**
```yaml
ports:
  - "0.0.0.0:8191:8191"  # Exposed to internet!
```

### Firewall Rules
```bash
# Block external access
sudo ufw deny 8191

# Allow localhost only
sudo ufw allow from 127.0.0.1 to any port 8191
```

---

## FAQ

**Q: Is FlareSolverr legal?**
A: Yes, for personal use. Always respect robots.txt and ToS.

**Q: Does it work on all websites?**
A: Most websites, including those with Cloudflare.

**Q: Can I use it on free hosting?**
A: If Docker is supported and you have enough resources.

**Q: How often should I update FlareSolverr?**
A: Monthly, or when you encounter blocking issues.

**Q: What's the difference from Selenium?**
A: FlareSolverr is specifically designed for solving challenges, not browser automation.

---

## Advanced Usage

### Using with Proxies
```yaml
environment:
  - PROXY_SERVER=http://proxy:port
  - PROXY_USERNAME=user
  - PROXY_PASSWORD=pass
```

### Session Management
```python
# Create session
session_id = flaresolverr.create_session()

# Use session for multiple requests
response = flaresolverr.get(url, session=session_id)

# Destroy session
flaresolverr.destroy_session(session_id)
```

### Custom Timeout Per Request
```python
# In scraper.py, modify:
self.flaresolverr_timeout = 120000  # 2 minutes
```

---

## Alternatives

If FlareSolverr doesn't work:

1. **cloudscraper** (Python library)
   ```bash
   pip install cloudscraper
   ```

2. **undetected-chromedriver** (Selenium-based)
   ```bash
   pip install undetected-chromedriver
   ```

3. **Playwright** (Node.js/Python)
   ```bash
   pip install playwright
   ```

4. **Residential Proxies** (paid services)

---

## Support

- FlareSolverr Issues: https://github.com/FlareSolverr/FlareSolverr
- Scraper Issues: https://github.com/YOUR_USERNAME/newscientist-rss-scraper

---

**Version:** 2.0  
**Last Updated:** February 2026  
**FlareSolverr:** Latest
