# Quick Reference Card

Essential commands and configurations for the New Scientist RSS Scraper.

## 🚀 Quick Start

```bash
# GitHub (fastest)
git clone <repo> && cd <repo>
# Enable Actions → Run workflow → Enable Pages

# Docker (self-hosted)
docker-compose up -d

# Local
./setup.sh && python scraper.py
```

## 📋 Common Commands

### Docker

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Update and rebuild
docker-compose pull && docker-compose up -d --build
```

### Python

```bash
# Run scraper
python scraper.py

# With FlareSolverr
FLARESOLVERR_URL=http://localhost:8191/v1 python scraper.py

# Validate feed
python validate_feed.py
```

### Make

```bash
make help           # Show all commands
make install        # Install dependencies
make run            # Run scraper
make validate       # Validate feed
make docker-up      # Start Docker
make test           # Run and validate
```

### Git

```bash
# Deploy update
git add .
git commit -m "Update"
git push

# Check status
git status

# View remote
git remote -v
```

## 🔧 Configuration

### Environment Variables

```bash
# FlareSolverr URL
export FLARESOLVERR_URL=http://localhost:8191/v1

# Or create .env file
cp .env.example .env
# Edit .env with your settings
```

### Update Frequency

```yaml
# .github/workflows/update-feed.yml
schedule:
  - cron: '0 6 * * *'  # 6 AM UTC daily

# Common patterns:
# - cron: '0 */12 * * *'  # Every 12 hours
# - cron: '0 0 * * *'     # Daily at midnight
# - cron: '0 12 * * 1'    # Weekly on Monday
```

## 🌐 URLs

### Local Development

```
FlareSolverr:    http://localhost:8191
Feed:            http://localhost:8080/feed.xml
Landing page:    http://localhost:8080/
```

### GitHub Pages

```
Feed:            https://USERNAME.github.io/REPO/feed.xml
Landing page:    https://USERNAME.github.io/REPO/
```

## 🐛 Quick Fixes

```bash
# FlareSolverr not working
docker restart flaresolverr

# Update everything
docker-compose pull
pip install -r requirements.txt --upgrade

# Clean and restart
make clean
make docker-down
make docker-up

# Check FlareSolverr health
curl http://localhost:8191/health
```

## 📊 File Locations

```
Config:              docker-compose.yml
Scraper:             scraper.py
Workflow:            .github/workflows/update-feed.yml
Generated feed:      feed.xml
Landing page:        index.html
```

## 🔍 Debugging

```bash
# View scraper output
python scraper.py

# View FlareSolverr logs
docker logs flaresolverr

# View all container logs
docker-compose logs

# Validate feed
python validate_feed.py

# Test FlareSolverr
curl -X POST http://localhost:8191/v1 \
  -H "Content-Type: application/json" \
  -d '{"cmd":"request.get","url":"https://www.newscientist.com","maxTimeout":60000}'
```

## 📖 Documentation

| Doc | Purpose |
|-----|---------|
| README.md | Main overview |
| QUICKSTART.md | 5-minute setup |
| DEPLOYMENT.md | All deployment options |
| FLARESOLVERR.md | FlareSolverr guide |
| TROUBLESHOOTING.md | Fix common issues |
| CONTRIBUTING.md | How to contribute |

## 🆘 Getting Help

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [FLARESOLVERR.md](FLARESOLVERR.md)
3. Search [existing issues](https://github.com/USER/REPO/issues)
4. Open new issue with logs

## 🎯 Common Tasks

### Add to RSS Reader

1. Copy feed URL
2. Open RSS reader
3. Add new feed
4. Paste URL

### Update Feed Manually

```bash
# GitHub Actions
Actions → Update RSS Feed → Run workflow

# Docker
docker-compose up scraper

# Local
python scraper.py
```

### Change Schedule

Edit `.github/workflows/update-feed.yml`:

```yaml
schedule:
  - cron: 'MIN HOUR DAY MONTH WEEKDAY'
```

### Test Locally

```bash
# With FlareSolverr
docker run -d -p 8191:8191 ghcr.io/flaresolverr/flaresolverr:latest
FLARESOLVERR_URL=http://localhost:8191/v1 python scraper.py

# Without FlareSolverr (may fail)
python scraper.py
```

---

**Tip:** Run `make help` to see all available commands!
