#!/usr/bin/env python3
"""
New Scientist RSS Feed Scraper with FlareSolverr Support
Fetches articles from the current issue and generates an RSS feed
Bypasses Cloudflare protection using FlareSolverr when enabled
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import sys
import os
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()


class NewScientistScraper:
    def __init__(self):
        self.base_url = "https://www.newscientist.com"
        self.current_issue_url = f"{self.base_url}/issues/current/"

        # Get user agent from env or use default
        self.user_agent = os.getenv('USER_AGENT', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.headers = {
            'User-Agent': self.user_agent
        }

        # FlareSolverr configuration
        self.use_flaresolverr = os.getenv('FLARESOLVERR_ENABLED', 'false').lower() == 'true'
        self.flaresolverr_url = os.getenv('FLARESOLVERR_URL', 'http://localhost:8191/v1')
        self.flaresolverr_timeout = int(os.getenv('FLARESOLVERR_TIMEOUT', '60000'))

        if self.use_flaresolverr:
            print(f"FlareSolverr enabled at: {self.flaresolverr_url}")
        else:
            print("Using direct HTTP requests (FlareSolverr disabled)")

    def fetch_with_flaresolverr(self, url, max_retries=3):
        """Fetch URL using FlareSolverr to bypass Cloudflare"""
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": self.flaresolverr_timeout
        }

        for attempt in range(max_retries):
            try:
                print(f"FlareSolverr attempt {attempt + 1}/{max_retries}...")
                response = requests.post(self.flaresolverr_url, json=payload, timeout=120)
                response.raise_for_status()

                data = response.json()

                if data.get('status') == 'ok':
                    solution = data.get('solution', {})
                    html = solution.get('response')

                    if html:
                        print(f"✓ FlareSolverr successfully fetched page ({len(html)} bytes)")
                        return html
                    else:
                        print(f"⚠ FlareSolverr returned empty response")
                else:
                    error_msg = data.get('message', 'Unknown error')
                    print(f"⚠ FlareSolverr error: {error_msg}")

                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)

            except requests.exceptions.Timeout:
                print(f"⚠ FlareSolverr timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(10)
            except requests.exceptions.RequestException as e:
                print(f"⚠ FlareSolverr request error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
            except json.JSONDecodeError as e:
                print(f"⚠ FlareSolverr JSON decode error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)

        raise Exception(f"Failed to fetch URL with FlareSolverr after {max_retries} attempts")

    def fetch_directly(self, url, max_retries=3):
        """Fetch URL directly using requests"""
        for attempt in range(max_retries):
            try:
                print(f"Direct request attempt {attempt + 1}/{max_retries}...")
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                print(f"✓ Successfully fetched page ({len(response.text)} bytes)")
                return response.text

            except requests.RequestException as e:
                print(f"⚠ Request error: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    print(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)

        raise Exception(f"Failed to fetch URL directly after {max_retries} attempts")

    def fetch_page(self):
        """Fetch the current issue page using configured method"""
        try:
            if self.use_flaresolverr:
                return self.fetch_with_flaresolverr(self.current_issue_url)
            else:
                return self.fetch_directly(self.current_issue_url)
        except Exception as e:
            print(f"❌ Error fetching page: {e}")

            # Fallback: try the opposite method
            if self.use_flaresolverr:
                print("Attempting fallback to direct request...")
                try:
                    return self.fetch_directly(self.current_issue_url)
                except Exception as e2:
                    print(f"❌ Fallback also failed: {e2}")

            sys.exit(1)

    def parse_articles(self, html_content):
        """Parse articles from the HTML content"""
        soup = BeautifulSoup(html_content, 'lxml')
        articles = []

        # Find the magazine hero section
        hero_section = soup.find('div', class_='ThisWeeksMagazineHero__Subjects')

        if not hero_section:
            print("⚠ Warning: Could not find magazine hero section")
            # Try alternative selectors
            hero_section = soup.find('div', class_=lambda x: x and 'MagazineHero' in x)

        if hero_section:
            # Find all subject sections
            subject_sections = hero_section.find_all('div', class_='ThisWeeksMagazineHero__Subject')

            for section in subject_sections:
                # Get category
                category_elem = section.find('div', class_='ThisWeeksMagazine__Category')
                category = category_elem.get_text(strip=True) if category_elem else "General"

                # Find all article links in this section
                article_links = section.find_all('a', class_='ThisWeeksMagazine__CopyLink')

                for link in article_links:
                    article = {
                        'title': link.get_text(strip=True),
                        'url': self.base_url + link.get('href', ''),
                        'category': category,
                        'image_url': None
                    }
                    articles.append(article)

        # Also get editor's picks with images — no limit
        editors_picks = soup.find_all('article', class_='Card--Article')

        for card in editors_picks:
            title_elem = card.find('h3', class_='Card__Title')
            link_elem = card.find_parent('a', class_='CardLink')
            category_elem = card.find('h4', class_='Card__Category')
            image_elem = card.find('img', class_='Image')
            subject_type = card.find('p', class_='Card__SubjectType')

            if title_elem and link_elem:
                title = title_elem.get_text(strip=True)

                # Skip if already in articles list
                if any(a['title'] == title for a in articles):
                    continue

                article = {
                    'title': title,
                    'url': self.base_url + link_elem.get('href', ''),
                    'category': category_elem.get_text(strip=True) if category_elem else "General",
                    'image_url': None,
                    'subject_type': subject_type.get_text(strip=True) if subject_type else None
                }

                # Extract image URL
                if image_elem:
                    # Try src first, then srcset
                    img_src = image_elem.get('src')
                    if img_src and img_src.startswith('http'):
                        article['image_url'] = img_src
                    else:
                        # Try to get highest resolution from srcset
                        srcset = image_elem.get('srcset')
                        if srcset:
                            sources = srcset.split(',')
                            if sources:
                                # Get the last (highest resolution) source
                                last_source = sources[-1].strip().split()[0]
                                if last_source.startswith('http'):
                                    article['image_url'] = last_source

                articles.append(article)

        return articles

    def generate_rss_feed(self, articles):
        """Generate RSS 2.0 feed from articles"""
        # Create RSS root element
        rss = Element('rss', version='2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')

        channel = SubElement(rss, 'channel')

        # Channel metadata
        SubElement(channel, 'title').text = 'New Scientist - Current Issue'
        SubElement(channel, 'link').text = self.current_issue_url
        SubElement(channel, 'description').text = 'Latest articles from New Scientist magazine current issue (powered by FlareSolverr)'
        SubElement(channel, 'language').text = 'en-us'
        SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        SubElement(channel, 'generator').text = 'NewScientist RSS Scraper v2.0 (with FlareSolverr)'

        # Self-referencing atom link (update with your GitHub Pages URL)
        atom_link = SubElement(channel, '{http://www.w3.org/2005/Atom}link')
        atom_link.set('href', 'https://YOUR_USERNAME.github.io/newscientist-rss-scraper/feed.xml')
        atom_link.set('rel', 'self')
        atom_link.set('type', 'application/rss+xml')

        # Add image
        image = SubElement(channel, 'image')
        SubElement(image, 'url').text = 'https://www.newscientist.com/wp-content/themes/newscientist/assets/img/meta/apple-touch-icon.png'
        SubElement(image, 'title').text = 'New Scientist'
        SubElement(image, 'link').text = self.base_url

        # Add articles as items
        for article in articles:
            item = SubElement(channel, 'item')

            SubElement(item, 'title').text = article['title']
            SubElement(item, 'link').text = article['url']
            SubElement(item, 'guid', isPermaLink='true').text = article['url']
            SubElement(item, 'pubDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            SubElement(item, 'category').text = article['category']

            # Create description
            description = f"Category: {article['category']}"
            if article.get('subject_type'):
                description += f" | Type: {article['subject_type']}"
            SubElement(item, 'description').text = description

            # Add image as enclosure if available
            if article.get('image_url'):
                enclosure = SubElement(item, 'enclosure')
                enclosure.set('url', article['image_url'])
                enclosure.set('type', 'image/jpeg')

                # Add media:content for better image support
                media_content = SubElement(item, '{http://search.yahoo.com/mrss/}content')
                media_content.set('url', article['image_url'])
                media_content.set('medium', 'image')

                # Add media:thumbnail
                media_thumb = SubElement(item, '{http://search.yahoo.com/mrss/}thumbnail')
                media_thumb.set('url', article['image_url'])

        return rss

    def prettify_xml(self, elem):
        """Return a pretty-printed XML string"""
        rough_string = tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

    def save_feed(self, rss_element, filename='feed.xml'):
        """Save RSS feed to file"""
        xml_string = self.prettify_xml(rss_element)

        # Remove empty lines
        lines = [line for line in xml_string.split('\n') if line.strip()]
        xml_string = '\n'.join(lines)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_string)

        print(f"✓ RSS feed saved to {filename}")

    def run(self):
        """Main execution method"""
        print("="*60)
        print("New Scientist RSS Scraper v2.0 (with FlareSolverr)")
        print("="*60)

        print("\nFetching New Scientist current issue page...")
        html_content = self.fetch_page()

        print("\nParsing articles...")
        articles = self.parse_articles(html_content)

        if not articles:
            print("⚠ Warning: No articles found!")
            print("This might indicate:")
            print("  - Website structure has changed")
            print("  - Cloudflare is blocking access")
            print("  - Network connectivity issues")
        else:
            print(f"✓ Found {len(articles)} articles")

        print("\nGenerating RSS feed...")
        rss_feed = self.generate_rss_feed(articles)

        print("Saving RSS feed...")
        self.save_feed(rss_feed)

        print("\n" + "="*60)
        print(f"✅ SUCCESS: {len(articles)} articles added to feed")
        print("="*60)

        # Print summary
        if articles:
            print("\nFirst 5 articles:")
            for i, article in enumerate(articles[:5], 1):
                img_indicator = "🖼️ " if article.get('image_url') else "  "
                print(f"{i}. {img_indicator}{article['title'][:55]}...")
            if len(articles) > 5:
                print(f"... and {len(articles) - 5} more")

        print(f"\nFlareSolverr: {'Enabled ✓' if self.use_flaresolverr else 'Disabled'}")
        print("="*60)


def main():
    scraper = NewScientistScraper()
    scraper.run()


if __name__ == '__main__':
    main()
