# Contributing to New Scientist RSS Scraper

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If the scraper stops working or produces incorrect results:

1. Check if New Scientist has changed their website structure
2. Open an issue with:
   - Description of the problem
   - Error messages (if any)
   - Date when the issue started
   - Your environment (Python version, OS)

### Suggesting Enhancements

Have an idea to improve the scraper? Open an issue describing:

- The enhancement you'd like to see
- Why it would be useful
- How it might be implemented

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/newscientist-rss-scraper.git
cd newscientist-rss-scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing Changes

Before submitting a PR:

1. Run the scraper and verify it produces valid XML
2. Check that all articles are captured correctly
3. Verify images are included in the feed
4. Test the feed in an RSS reader

## Updating Selectors

If New Scientist changes their website structure:

1. Inspect the new HTML structure
2. Update CSS selectors in `scraper.py`
3. Test thoroughly with current and recent issues
4. Document the changes in your PR

## Questions?

Open an issue or reach out via GitHub discussions!
