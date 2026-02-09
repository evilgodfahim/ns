# New Scientist RSS Feed Scraper

A Python-based web scraper that fetches articles from New Scientist's current magazine issue and generates an RSS feed with thumbnails. The feed updates automatically every day via GitHub Actions. **Now with FlareSolverr integration to bypass Cloudflare protection!**

## Features

- ✨ Scrapes New Scientist's current issue page
- 🛡️ **Bypasses Cloudflare protection with FlareSolverr**
- 📰 Generates RSS 2.0 compliant XML feed
- 🖼️ Includes article thumbnails in the feed
- 🔄 Automatically updates daily via GitHub Actions
- 📱 Compatible with all RSS readers
- 🌐 Hosted on GitHub Pages
- 🐳 Docker support with FlareSolverr included

## RSS Feed URL

Once deployed, your RSS feed will be available at:
```
https://YOUR_USERNAME.github.io/newscientist-rss-scraper/feed.xml
```

## Setup Instructions

### 1. Fork/Clone this Repository

```bash
git clone https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
cd newscientist-rss-scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python scraper.py
```

This will generate `feed.xml` in the root directory.

### 4. Enable GitHub Actions

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Under "Workflow permissions", select **Read and write permissions**
4. Click **Save**

### 5. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under "Source", select **Deploy from a branch**
3. Select branch: `gh-pages`, folder: `/ (root)`
4. Click **Save**

The feed will automatically update daily at 6 AM UTC.

## FlareSolverr Integration

This scraper includes **optional** FlareSolverr support to bypass Cloudflare protection and other anti-bot measures.

### When to Use FlareSolverr

✅ Enable if you encounter:
- Cloudflare "Checking your browser" challenges
- 403 Forbidden errors
- 503 Service Unavailable errors
- Bot detection blocking

❌ You don't need it if the scraper works fine without it.

### Quick Start with FlareSolverr

```bash
# Copy environment file
cp .env.example .env

# Enable FlareSolverr (edit .env)
FLARESOLVERR_ENABLED=true

# Start with Docker Compose (includes FlareSolverr)
docker-compose up -d
```

📚 **Full documentation:** See [FLARESOLVERR.md](FLARESOLVERR.md) for detailed setup instructions, troubleshooting, and configuration options.

## How It Works

1. **FlareSolverr**: Bypasses Cloudflare protection using a headless Chrome browser
2. **Scraper**: `scraper.py` fetches the current issue page from New Scientist
3. **Parser**: Extracts article titles, URLs, categories, and thumbnail images
4. **RSS Generator**: Creates an RSS 2.0 XML feed with enclosures for images
5. **GitHub Actions**: Runs daily to update the feed (includes FlareSolverr service)
6. **GitHub Pages**: Hosts the static RSS feed file

### FlareSolverr Integration

This project uses [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) to bypass Cloudflare protection:

- **GitHub Actions**: FlareSolverr runs automatically as a service
- **Docker**: FlareSolverr included in `docker-compose.yml`
- **Local Development**: Optional - scraper tries direct requests first

See [FLARESOLVERR.md](FLARESOLVERR.md) for detailed setup and configuration.

## Project Structure

```
newscientist-rss-scraper/
├── scraper.py              # Main scraper script (with FlareSolverr support)
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── update-feed.yml # GitHub Actions workflow (includes FlareSolverr)
├── docker-compose.yml      # Docker setup (includes FlareSolverr service)
├── Dockerfile              # Docker image for scraper
├── feed.xml               # Generated RSS feed (auto-created)
├── index.html             # Landing page
├── FLARESOLVERR.md        # FlareSolverr setup and troubleshooting
└── README.md              # This file
```

## Feed Structure

Each RSS item includes:
- **Title**: Article headline
- **Link**: Direct URL to the article
- **Description**: Article category and type
- **Publication Date**: Current date/time
- **Image**: Thumbnail enclosure with proper MIME type
- **Category**: Article category (Health, Technology, etc.)

## Customization

### Change Update Frequency

Edit `.github/workflows/update-feed.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Change this line (currently 6 AM UTC daily)
```

Cron format: `minute hour day month weekday`

Examples:
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight
- `0 12 * * 1` - Every Monday at noon

### Modify Feed Metadata

Edit `scraper.py` to change:
- Feed title
- Feed description
- Feed language
- Maximum number of articles

## Requirements

- Python 3.8+
- beautifulsoup4
- requests
- lxml
- Docker (optional, for FlareSolverr)

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment options
- **[FLARESOLVERR.md](FLARESOLVERR.md)** - FlareSolverr setup and configuration
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Troubleshooting

### Feed not updating?

1. Check GitHub Actions tab for errors
2. Verify workflow permissions are set correctly
3. Ensure gh-pages branch exists and is set in Pages settings

### Articles not appearing?

The scraper targets specific HTML structure. If New Scientist changes their website, the CSS selectors may need updating in `scraper.py`.

### Images not loading?

Ensure the enclosure URLs are accessible. Some images may have hotlink protection.

## Legal Notice

This tool is for personal use and educational purposes. Please respect New Scientist's terms of service and robots.txt. Consider subscribing to New Scientist to support quality science journalism.

## License

MIT License - See LICENSE file for details

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- New Scientist for their excellent science journalism
- BeautifulSoup for HTML parsing
- GitHub Actions for free automation
