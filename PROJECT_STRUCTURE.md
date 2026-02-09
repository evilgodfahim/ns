# Project Structure

Complete overview of the New Scientist RSS Scraper repository.

```
newscientist-rss-scraper/
│
├── 📄 Core Application Files
│   ├── scraper.py              # Main scraper script - fetches articles and generates RSS
│   ├── validate_feed.py        # Feed validation tool - checks RSS XML validity
│   └── requirements.txt        # Python dependencies (beautifulsoup4, requests, lxml)
│
├── 🌐 Web Interface
│   ├── index.html             # Landing page for GitHub Pages
│   ├── feed.xml               # Generated RSS feed (auto-created)
│   └── nginx.conf             # Nginx configuration for serving feed
│
├── 🐳 Container Deployment
│   ├── Dockerfile             # Docker image definition
│   └── docker-compose.yml     # Docker Compose for easy deployment
│
├── ⚙️ GitHub Automation
│   └── .github/
│       └── workflows/
│           └── update-feed.yml # GitHub Actions workflow for daily updates
│
├── 📚 Documentation
│   ├── README.md              # Main documentation and overview
│   ├── QUICKSTART.md          # 5-minute setup guide
│   ├── DEPLOYMENT.md          # Complete deployment options
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   └── PROJECT_STRUCTURE.md   # This file
│
├── 🔧 Setup & Configuration
│   ├── setup.sh               # Automated setup script for local development
│   ├── .gitignore            # Git ignore rules
│   └── LICENSE               # MIT License
│
└── 📊 Generated Content (Not in Git)
    └── feed.xml              # RSS feed (auto-generated, served via GitHub Pages)
```

## 📄 File Descriptions

### Core Application

**scraper.py** (Main Script)
- Fetches New Scientist current issue page
- Parses HTML using BeautifulSoup
- Extracts articles with titles, URLs, categories, images
- Generates RSS 2.0 XML feed with media enclosures
- ~200 lines of Python

**validate_feed.py** (Validation Tool)
- Validates generated RSS XML
- Checks required elements
- Counts articles and images
- Reports feed statistics
- ~100 lines of Python

**requirements.txt**
- beautifulsoup4==4.12.3 (HTML parsing)
- requests==2.31.0 (HTTP requests)
- lxml==5.1.0 (XML processing)

### Web Interface

**index.html**
- Beautiful landing page
- Feed URL display and copy button
- Instructions for RSS readers
- Mobile-responsive design
- ~250 lines of HTML/CSS/JS

**feed.xml** (Generated)
- RSS 2.0 compliant feed
- Contains all current issue articles
- Includes media:content for images
- Updated daily automatically
- ~1-5 KB typical size

**nginx.conf**
- Serves feed with correct Content-Type
- Enables gzip compression
- CORS headers for cross-origin access
- Cache control (1 hour)

### Container Deployment

**Dockerfile**
- Python 3.11 slim base
- Installs dependencies
- Runs scraper script
- ~15 lines

**docker-compose.yml**
- Scraper service
- Optional Nginx service
- Volume mounts for feed.xml
- ~30 lines

### GitHub Automation

**update-feed.yml** (GitHub Actions)
- Triggers: Daily (6 AM UTC), manual, on push
- Steps:
  1. Checkout code
  2. Setup Python
  3. Install dependencies
  4. Run scraper
  5. Deploy to gh-pages
- Permissions: Write access required

### Documentation

**README.md**
- Project overview
- Features list
- Setup instructions
- How it works
- Requirements
- ~400 lines

**QUICKSTART.md**
- 5-minute setup guide
- GitHub deployment steps
- Local testing
- Common schedules
- Troubleshooting
- ~200 lines

**DEPLOYMENT.md**
- 5 deployment options:
  1. GitHub Pages (recommended)
  2. Docker
  3. Cloud platforms (Heroku, Railway)
  4. VPS
  5. Home server/Raspberry Pi
- Comparison table
- Security considerations
- ~600 lines

**CONTRIBUTING.md**
- Bug reporting
- Enhancement suggestions
- Pull request process
- Code style guidelines
- Testing procedures
- ~150 lines

### Setup & Configuration

**setup.sh**
- Automated setup script
- Creates virtual environment
- Installs dependencies
- Provides next steps
- Works on Linux/macOS
- ~40 lines

**.gitignore**
- Python cache files
- Virtual environments
- IDE files
- OS files
- Generated feed.xml

**LICENSE**
- MIT License
- Free to use, modify, distribute

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Trigger                   │
│              (Daily 6 AM UTC / Manual / Push)                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Run scraper.py                          │
│  1. Fetch https://www.newscientist.com/issues/current/     │
│  2. Parse HTML with BeautifulSoup                           │
│  3. Extract articles (title, URL, category, image)          │
│  4. Generate RSS 2.0 XML                                     │
│  5. Save to feed.xml                                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Deploy to gh-pages branch                   │
│  - feed.xml → GitHub Pages                                   │
│  - index.html → Landing page                                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│            Accessible at GitHub Pages URL                    │
│  https://USERNAME.github.io/newscientist-rss-scraper/       │
│  - /feed.xml (RSS feed)                                      │
│  - / (landing page)                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                RSS Readers Fetch Feed                        │
│  - Feedly, Inoreader, NetNewsWire, etc.                     │
│  - Users read New Scientist articles                         │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Features by File

| Feature | Implemented In | Description |
|---------|---------------|-------------|
| Article Scraping | scraper.py | BeautifulSoup HTML parsing |
| Image Extraction | scraper.py | Srcset parsing, enclosure tags |
| RSS Generation | scraper.py | XML ElementTree, media tags |
| Feed Validation | validate_feed.py | XML parsing, element checking |
| Daily Updates | update-feed.yml | GitHub Actions cron |
| Web Interface | index.html | Responsive HTML/CSS/JS |
| Container Support | Dockerfile, docker-compose.yml | Docker deployment |
| Easy Setup | setup.sh | Automated configuration |

## 🔢 Statistics

- **Total Files:** 16 core files
- **Total Lines:** ~2,000+ lines (code + docs)
- **Languages:** Python, YAML, HTML/CSS/JS, Shell, Markdown
- **Dependencies:** 3 Python packages
- **Deployment Options:** 5 major options
- **Documentation:** 5 comprehensive guides

## 🚀 Quick Commands

```bash
# Local development
./setup.sh                 # Initial setup
python scraper.py          # Run scraper
python validate_feed.py    # Validate output

# Docker
docker-compose up -d       # Start services
docker-compose logs        # View logs

# Git operations
git clone URL              # Clone repo
git add .                  # Stage changes
git commit -m "message"    # Commit
git push                   # Deploy
```

## 📝 Customization Points

1. **Update Frequency**
   - File: `.github/workflows/update-feed.yml`
   - Line: 5 (cron schedule)

2. **Feed Metadata**
   - File: `scraper.py`
   - Lines: 95-105 (channel info)

3. **Article Limit**
   - File: `scraper.py`
   - Line: 68 (editors_picks[:10])

4. **CSS Selectors**
   - File: `scraper.py`
   - Lines: 50-75 (HTML parsing)

5. **Page Design**
   - File: `index.html`
   - Lines: 15-100 (styles)

## 🎓 Learning Path

For newcomers to the project:

1. **Start Here:** README.md → QUICKSTART.md
2. **Understand Code:** scraper.py → validate_feed.py
3. **Deploy:** DEPLOYMENT.md → Choose method
4. **Customize:** Modify scraper.py selectors
5. **Contribute:** CONTRIBUTING.md → Submit PR

## 🔗 External Dependencies

- **New Scientist:** Source website
- **GitHub:** Hosting and automation
- **Python:** Runtime environment
- **BeautifulSoup:** HTML parsing
- **GitHub Pages:** Feed hosting

## 📈 Future Enhancement Ideas

- [ ] Support for archived issues
- [ ] Full article text extraction
- [ ] Multiple feed formats (JSON Feed, Atom)
- [ ] Category-specific feeds
- [ ] Author information extraction
- [ ] Article full-text search
- [ ] API endpoint for programmatic access
- [ ] Mobile app integration
- [ ] Telegram/Discord notifications

---

**Last Updated:** February 2026
**Version:** 1.0
**Maintainer:** Community
