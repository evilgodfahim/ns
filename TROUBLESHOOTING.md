# Troubleshooting Guide

Common issues and their solutions for the New Scientist RSS Scraper.

## Table of Contents

- [FlareSolverr Issues](#flaresolverr-issues)
- [Scraper Issues](#scraper-issues)
- [GitHub Actions Issues](#github-actions-issues)
- [Docker Issues](#docker-issues)
- [Feed Issues](#feed-issues)
- [Network Issues](#network-issues)

---

## FlareSolverr Issues

### FlareSolverr Not Starting

**Symptoms:** Can't connect to FlareSolverr, connection refused

**Solutions:**

```bash
# 1. Check if FlareSolverr is running
docker ps | grep flaresolverr

# 2. Check FlareSolverr logs
docker logs flaresolverr

# 3. Restart FlareSolverr
docker restart flaresolverr

# 4. Check if port 8191 is available
netstat -tuln | grep 8191
# or
lsof -i :8191

# 5. Start FlareSolverr manually
docker run -d --name flaresolverr -p 8191:8191 ghcr.io/flaresolverr/flaresolverr:latest
```

### FlareSolverr Timeout

**Symptoms:** Scraper hangs or times out after 60 seconds

**Solutions:**

1. **Increase timeout** in `scraper.py`:
   ```python
   payload = {
       "cmd": "request.get",
       "url": url,
       "maxTimeout": 120000  # 2 minutes
   }
   ```

2. **Check FlareSolverr memory**:
   ```bash
   docker stats flaresolverr
   # Needs ~500MB RAM
   ```

3. **Restart FlareSolverr**:
   ```bash
   docker restart flaresolverr
   ```

### FlareSolverr Returns Error

**Symptoms:** `status: error` in FlareSolverr response

**Solutions:**

```bash
# 1. Check detailed logs
docker logs flaresolverr --tail 100

# 2. Update FlareSolverr
docker pull ghcr.io/flaresolverr/flaresolverr:latest
docker-compose up -d --build

# 3. Test with curl
curl -X POST http://localhost:8191/v1 \
  -H "Content-Type: application/json" \
  -d '{"cmd": "request.get", "url": "https://www.newscientist.com", "maxTimeout": 60000}'
```

### Cloudflare Still Blocking

**Symptoms:** Gets Cloudflare challenge page even with FlareSolverr

**Solutions:**

1. **Update FlareSolverr** (Cloudflare updates their protection):
   ```bash
   docker pull ghcr.io/flaresolverr/flaresolverr:latest
   docker-compose down
   docker-compose up -d
   ```

2. **Try different browser profile**:
   Add to docker-compose.yml:
   ```yaml
   environment:
     - BROWSER_TIMEOUT=60000
   ```

3. **Check if website blocked your IP**:
   - Try from different IP/VPS
   - Wait a few hours and retry

---

## Scraper Issues

### "No articles found"

**Symptoms:** Scraper runs but finds 0 articles

**Solutions:**

1. **Website structure changed**:
   ```bash
   # Fetch page and inspect HTML
   curl -s https://www.newscientist.com/issues/current/ > page.html
   # Open page.html and look for article containers
   ```

2. **Update CSS selectors** in `scraper.py`:
   - Line 50-75: Article parsing logic
   - Check class names haven't changed

3. **Run with debug logging**:
   ```python
   # Add to scraper.py
   print(f"HTML length: {len(html_content)}")
   print(f"Found sections: {len(subject_sections)}")
   ```

### ImportError or ModuleNotFoundError

**Symptoms:** `ModuleNotFoundError: No module named 'bs4'`

**Solutions:**

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | grep -E "beautifulsoup4|requests|lxml"

# 4. Use Python 3.8+
python --version  # Should be 3.8 or higher
```

### Connection Timeout

**Symptoms:** `requests.exceptions.Timeout`

**Solutions:**

1. **Increase timeout**:
   ```python
   # In scraper.py, line ~120
   response = requests.get(url, headers=self.headers, timeout=60)
   ```

2. **Check internet connection**:
   ```bash
   ping www.newscientist.com
   curl -I https://www.newscientist.com
   ```

3. **Try FlareSolverr**:
   ```bash
   FLARESOLVERR_URL=http://localhost:8191/v1 python scraper.py
   ```

---

## GitHub Actions Issues

### Workflow Failing

**Symptoms:** GitHub Actions shows red X

**Solutions:**

1. **Check logs**:
   - Go to Actions tab
   - Click failed workflow
   - Expand failed step

2. **Common issues**:
   
   **FlareSolverr not ready:**
   ```yaml
   # Increase wait time in update-feed.yml
   for i in {1..60}; do  # Changed from 30 to 60
   ```

   **Permissions error:**
   - Settings → Actions → General
   - Workflow permissions: "Read and write permissions"

   **Python version:**
   ```yaml
   # In update-feed.yml
   python-version: '3.11'  # Ensure 3.8+
   ```

### Feed Not Deploying to GitHub Pages

**Symptoms:** Feed URL returns 404

**Solutions:**

1. **Check gh-pages branch exists**:
   - Go to repository
   - Click branch dropdown
   - Should see `gh-pages`

2. **Enable GitHub Pages**:
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages → / (root)
   - Save

3. **Check deployment**:
   - Settings → Pages
   - Should show "Your site is live at..."
   - Wait 2-3 minutes for first deployment

4. **Force re-deploy**:
   - Actions → Update RSS Feed → Run workflow

### Workflow Not Running on Schedule

**Symptoms:** Cron schedule doesn't trigger workflow

**Solutions:**

1. **GitHub Actions limitations**:
   - Scheduled workflows may be delayed by up to 30 minutes
   - Low-traffic repos may have longer delays

2. **Manual trigger**:
   ```yaml
   # Ensure workflow_dispatch is enabled
   on:
     workflow_dispatch:
   ```

3. **Check cron syntax**:
   ```yaml
   # Use https://crontab.guru to verify
   - cron: '0 6 * * *'  # 6 AM UTC daily
   ```

---

## Docker Issues

### "Cannot connect to Docker daemon"

**Symptoms:** `docker: Cannot connect to the Docker daemon`

**Solutions:**

```bash
# 1. Start Docker
sudo systemctl start docker

# 2. Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# 3. Check Docker status
sudo systemctl status docker
```

### Port Already in Use

**Symptoms:** `port is already allocated`

**Solutions:**

```bash
# 1. Find what's using the port
sudo lsof -i :8080  # or :8191

# 2. Stop the conflicting service
sudo kill <PID>

# 3. Or change port in docker-compose.yml
ports:
  - "8081:80"  # Changed from 8080
```

### Container Keeps Restarting

**Symptoms:** `docker ps` shows container restarting

**Solutions:**

```bash
# 1. Check logs
docker logs newscientist-rss-scraper

# 2. Run interactively to debug
docker run -it --entrypoint /bin/sh newscientist-scraper

# 3. Check resource limits
docker stats

# 4. Increase memory limit
docker run -m 512m newscientist-scraper
```

---

## Feed Issues

### Feed Not Valid RSS

**Symptoms:** RSS readers can't parse feed

**Solutions:**

```bash
# 1. Validate feed
python validate_feed.py

# 2. Check XML syntax
xmllint feed.xml

# 3. Online validator
# Upload feed.xml to https://validator.w3.org/feed/
```

### Images Not Loading in Feed

**Symptoms:** Articles appear but no thumbnails

**Solutions:**

1. **Check image URLs**:
   ```bash
   grep -o 'enclosure url="[^"]*"' feed.xml | head -5
   ```

2. **Test image URLs**:
   ```bash
   curl -I <image_url>
   # Should return 200 OK
   ```

3. **RSS reader cache**:
   - Clear RSS reader cache
   - Re-subscribe to feed

### Feed Shows Old Articles

**Symptoms:** Feed not updating with new articles

**Solutions:**

1. **Check when feed was last generated**:
   ```xml
   <!-- In feed.xml -->
   <lastBuildDate>...</lastBuildDate>
   ```

2. **Manually run scraper**:
   ```bash
   python scraper.py
   ```

3. **GitHub Actions**:
   - Check if workflow is running
   - Actions → Update RSS Feed → Run workflow

4. **Clear browser cache**:
   - Hard refresh: Ctrl+Shift+R (Windows/Linux)
   - Hard refresh: Cmd+Shift+R (Mac)

---

## Network Issues

### DNS Resolution Failed

**Symptoms:** `Failed to resolve hostname`

**Solutions:**

```bash
# 1. Test DNS
nslookup www.newscientist.com

# 2. Use Google DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# 3. Check /etc/hosts
cat /etc/hosts
```

### SSL Certificate Error

**Symptoms:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions:**

```bash
# 1. Update CA certificates
sudo apt update
sudo apt install ca-certificates

# 2. Update Python certifi
pip install --upgrade certifi

# 3. As last resort (not recommended for production)
# In scraper.py:
# requests.get(url, verify=False)
```

### Rate Limited

**Symptoms:** Getting 429 or 403 errors

**Solutions:**

1. **Reduce frequency**:
   ```yaml
   # In update-feed.yml
   - cron: '0 12 * * *'  # Once daily
   ```

2. **Add delays**:
   ```python
   import time
   time.sleep(5)  # Wait between requests
   ```

3. **Use FlareSolverr**:
   - Better handles rate limiting
   - Rotates request patterns

---

## General Debugging Tips

### Enable Verbose Logging

```python
# Add to scraper.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```bash
# 1. Test FlareSolverr
make flaresolverr-test

# 2. Test scraper
python scraper.py

# 3. Validate feed
python validate_feed.py

# 4. Full test
make test
```

### Check Environment

```bash
# Python version
python --version

# Installed packages
pip list

# Docker version
docker --version

# System resources
free -h
df -h
```

---

## Getting Help

If none of these solutions work:

1. **Check existing issues**: https://github.com/YOUR_USERNAME/newscientist-rss-scraper/issues
2. **Open a new issue** with:
   - Error message (full output)
   - Steps to reproduce
   - Your environment (OS, Python version, Docker version)
   - Relevant logs
3. **Enable debug mode** and include output

### Useful Commands for Bug Reports

```bash
# System info
uname -a
python --version
docker --version

# Scraper output
python scraper.py 2>&1 | tee scraper.log

# FlareSolverr logs
docker logs flaresolverr > flaresolverr.log

# Docker environment
docker-compose ps
docker-compose logs > docker.log
```

---

## Quick Fixes Checklist

- [ ] Restart FlareSolverr: `docker restart flaresolverr`
- [ ] Update FlareSolverr: `docker pull ghcr.io/flaresolverr/flaresolverr:latest`
- [ ] Update dependencies: `pip install -r requirements.txt --upgrade`
- [ ] Clear cache: `rm -f feed.xml`
- [ ] Run validation: `python validate_feed.py`
- [ ] Check GitHub Actions permissions
- [ ] Verify GitHub Pages is enabled
- [ ] Test internet connection: `ping www.newscientist.com`
- [ ] Check disk space: `df -h`
- [ ] Review recent changes on New Scientist website

---

**Still stuck?** Open an issue with detailed logs and we'll help you out!
