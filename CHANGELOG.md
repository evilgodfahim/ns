# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-09

### Added
- **FlareSolverr Integration** - Bypass Cloudflare protection automatically
  - GitHub Actions includes FlareSolverr service
  - Docker Compose includes FlareSolverr container
  - Automatic fallback: tries FlareSolverr first, then direct requests
  - Cloudflare detection and automatic switching
- Comprehensive FlareSolverr documentation (FLARESOLVERR.md)
- FlareSolverr health checks in GitHub Actions
- Network isolation for FlareSolverr in Docker

### Changed
- Scraper now supports environment variable `FLARESOLVERR_URL`
- Enhanced error handling with retry logic
- Improved logging with FlareSolverr status
- Updated Docker Compose with dedicated network
- GitHub Actions workflow includes FlareSolverr service

### Technical Details
- FlareSolverr runs on port 8191
- Automatic detection of Cloudflare challenges
- Retry logic: 3 attempts for both FlareSolverr and direct requests
- Timeout handling: 60s for FlareSolverr, 30s for direct
- User-Agent updated to Chrome 120

---

## [1.0.0] - 2026-02-09

### Added
- Initial release of New Scientist RSS Scraper
- Core scraping functionality for current issue articles
- RSS 2.0 feed generation with media enclosures
- GitHub Actions workflow for daily automatic updates
- GitHub Pages deployment support
- Docker and docker-compose support
- Beautiful responsive web landing page
- Feed validation tool
- Comprehensive documentation:
  - README.md with full project overview
  - QUICKSTART.md for rapid setup
  - DEPLOYMENT.md with 5 deployment options
  - CONTRIBUTING.md for contributors
  - PROJECT_STRUCTURE.md for code organization
- Automated setup script (setup.sh)
- Multiple deployment options:
  - GitHub Pages (free, automatic)
  - Docker containers
  - Cloud platforms (Heroku, Railway, DigitalOcean)
  - VPS servers
  - Home servers / Raspberry Pi
- Support for article images in RSS feed
- Category and subject type extraction
- Nginx configuration for self-hosted deployments

### Features
- Scrapes articles from New Scientist "On the cover" section
- Extracts editor's picks with thumbnail images
- Generates RSS feed with:
  - Article titles and links
  - Publication dates
  - Categories
  - Article descriptions
  - Image enclosures (media:content)
  - Proper RSS 2.0 namespaces
- Daily automatic updates via GitHub Actions (6 AM UTC)
- Mobile-responsive landing page with feed URL
- One-click feed URL copying
- XML validation tool
- Cross-origin resource sharing (CORS) support

### Technical Details
- Python 3.8+ compatible
- BeautifulSoup4 for HTML parsing
- Requests library for HTTP requests
- lxml for XML processing
- GitHub Actions for CI/CD
- GitHub Pages for free hosting
- Docker support for containerization
- Nginx for production serving

### Documentation
- Step-by-step setup guides
- Multiple deployment tutorials
- Troubleshooting sections
- Code contribution guidelines
- Project structure documentation
- Docker deployment guides
- Cloud platform tutorials

### Dependencies
- beautifulsoup4 4.12.3
- requests 2.31.0
- lxml 5.1.0

---

## [Unreleased]

### Planned Features
- [ ] Support for archived magazine issues
- [ ] Full article text extraction
- [ ] JSON Feed format support
- [ ] Atom feed format support
- [ ] Category-specific feeds (Health, Technology, Space, etc.)
- [ ] Author information extraction
- [ ] Article tags and keywords
- [ ] Search functionality
- [ ] Email notifications for new articles
- [ ] Telegram bot integration
- [ ] Discord webhook support
- [ ] API endpoint for programmatic access
- [ ] Article read time estimation
- [ ] Related articles linking
- [ ] Mobile app companion
- [ ] Browser extension
- [ ] RSS feed analytics
- [ ] Article archiving
- [ ] Offline reading support

### Potential Improvements
- [ ] Better error handling for network failures
- [ ] Retry logic for failed scrapes
- [ ] Caching to reduce server load
- [ ] Support for multiple languages
- [ ] Customizable feed item limits
- [ ] Article content preview in feed
- [ ] Better image resolution handling
- [ ] Support for article comments
- [ ] Integration with read-it-later services
- [ ] Custom feed branding options
- [ ] Multiple feed variants (full/summary)
- [ ] Historical issue browser
- [ ] Article popularity tracking
- [ ] Duplicate article detection
- [ ] Feed item deduplication
- [ ] Advanced filtering options
- [ ] User preference settings
- [ ] Admin dashboard
- [ ] Usage statistics
- [ ] Feed health monitoring

### Known Issues
- None reported yet

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-02-09 | Initial release |

---

## How to Update

### For GitHub Pages Users:
```bash
git pull origin main
git push origin main
# GitHub Actions will automatically deploy
```

### For Docker Users:
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### For Manual Installations:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python scraper.py
```

---

## Migration Guides

### From v1.0.0 to Future Versions
Migration guides will be added here when new versions are released.

---

## Support

For issues, feature requests, or questions:
- [Open an issue](https://github.com/YOUR_USERNAME/newscientist-rss-scraper/issues)
- Check existing documentation
- Review troubleshooting guides

---

## Contributors

Thank you to all contributors who help improve this project!

- Initial development: Community
- Documentation: Community
- Bug reports: Community
- Feature suggestions: Community

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note:** This project is not affiliated with or endorsed by New Scientist. Please support quality science journalism by subscribing to New Scientist at https://www.newscientist.com/subscribe/
