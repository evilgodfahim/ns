# Quick Start Guide

Get your New Scientist RSS feed up and running in 5 minutes!

## 🚀 Quick Setup (GitHub)

**Note:** GitHub Actions automatically includes FlareSolverr to bypass Cloudflare - no extra setup needed!

### 1. Create Repository

Click the green "Use this template" button on GitHub, or:

```bash
git clone https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
cd newscientist-rss-scraper
git remote set-url origin https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
git push -u origin main
```

### 2. Enable GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions", select **Read and write permissions**
3. Click **Save**

### 3. Run Initial Scrape

1. Go to **Actions** tab
2. Click "Update RSS Feed" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait ~30 seconds for completion

### 4. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **gh-pages** → **/ (root)**
4. Click **Save**
5. Wait 2-3 minutes for deployment

### 5. Access Your Feed

Your feed will be available at:
```
https://YOUR_USERNAME.github.io/newscientist-rss-scraper/feed.xml
```

## 💻 Local Testing

### Option 1: With FlareSolverr (Recommended)

```bash
# Start FlareSolverr
docker run -d -p 8191:8191 ghcr.io/flaresolverr/flaresolverr:latest

# Setup and run
chmod +x setup.sh
./setup.sh
FLARESOLVERR_URL=http://localhost:8191/v1 python scraper.py
python validate_feed.py
```

### Option 2: Without FlareSolverr

```bash
chmod +x setup.sh
./setup.sh
python scraper.py  # May fail if Cloudflare blocks
python validate_feed.py
```

### Option 3: Using Docker Compose

```bash
# Starts FlareSolverr, scraper, and nginx
docker-compose up -d

# View feed at http://localhost:8080/feed.xml
```

## 🔧 Customization

### Enable FlareSolverr (Optional)

If you encounter Cloudflare blocking:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
FLARESOLVERR_ENABLED=true
```

Then use Docker Compose:
```bash
docker-compose up -d
```

See [FLARESOLVERR.md](FLARESOLVERR.md) for details.

### Change Update Schedule

Edit `.github/workflows/update-feed.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

Common schedules:
- `0 */12 * * *` - Every 12 hours
- `0 0 * * *` - Daily at midnight
- `0 0 * * 1` - Weekly on Monday

### Modify Feed Title/Description

Edit `scraper.py` around line 100:

```python
SubElement(channel, 'title').text = 'Your Custom Title'
SubElement(channel, 'description').text = 'Your custom description'
```

## 📱 Adding to RSS Reader

### Feedly
1. Click "Add Content"
2. Paste your feed URL
3. Click "Follow"

### Inoreader
1. Click "Add new subscription"
2. Paste feed URL
3. Click "Subscribe"

### Apple News/NetNewsWire
1. File → New Feed Subscription
2. Paste URL
3. Click "Subscribe"

## ❓ Troubleshooting

### Feed not updating?
- Check Actions tab for errors
- Verify workflow permissions
- Ensure gh-pages branch exists

### No articles in feed?
- Run locally to debug: `python scraper.py`
- Check for website changes
- View scraper output for errors

### Images not showing?
- Some RSS readers cache images
- Clear reader cache
- Check image URLs are valid

## 🆘 Need Help?

- [Open an issue](https://github.com/YOUR_USERNAME/newscientist-rss-scraper/issues)
- Check [README.md](README.md) for detailed docs
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development

## 🎉 You're Done!

Your feed will now update automatically every day. Add it to your RSS reader and enjoy your science news!
