#!/usr/bin/env python3
"""
Test script to validate the RSS feed
"""

import xml.etree.ElementTree as ET
import sys
import os


def validate_feed(filename='feed.xml'):
    """Validate the generated RSS feed"""
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found!")
        return False
    
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        
        print(f"✓ XML is well-formed")
        
        # Check RSS version
        if root.tag != 'rss':
            print(f"❌ Root element is not 'rss', found: {root.tag}")
            return False
        
        version = root.get('version')
        if version != '2.0':
            print(f"⚠️  Warning: RSS version is {version}, expected 2.0")
        else:
            print(f"✓ RSS version 2.0")
        
        # Find channel
        channel = root.find('channel')
        if channel is None:
            print("❌ No channel element found")
            return False
        
        print(f"✓ Channel element found")
        
        # Check required channel elements
        required_elements = ['title', 'link', 'description']
        for elem in required_elements:
            if channel.find(elem) is None:
                print(f"❌ Missing required element: {elem}")
                return False
            else:
                value = channel.find(elem).text
                print(f"✓ {elem}: {value[:50]}...")
        
        # Count items
        items = channel.findall('item')
        item_count = len(items)
        
        if item_count == 0:
            print("⚠️  Warning: No items found in feed")
        else:
            print(f"✓ Found {item_count} items")
        
        # Validate items
        items_with_images = 0
        for i, item in enumerate(items[:5], 1):  # Check first 5 items
            title = item.find('title')
            link = item.find('link')
            
            if title is None or link is None:
                print(f"❌ Item {i} missing title or link")
                continue
            
            print(f"\n  Item {i}:")
            print(f"    Title: {title.text[:50]}...")
            print(f"    Link: {link.text[:60]}...")
            
            # Check for image
            enclosure = item.find('enclosure')
            media_content = item.find('{http://search.yahoo.com/mrss/}content')
            
            if enclosure is not None or media_content is not None:
                items_with_images += 1
                print(f"    ✓ Has image")
            else:
                print(f"    ⚠️  No image")
        
        if item_count > 5:
            print(f"\n  ... and {item_count - 5} more items")
        
        print(f"\n✓ {items_with_images}/{min(5, item_count)} items have images")
        
        # File size check
        file_size = os.path.getsize(filename)
        print(f"\n✓ Feed size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        print("\n" + "="*50)
        print("✅ Feed validation passed!")
        print("="*50)
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'feed.xml'
    success = validate_feed(filename)
    sys.exit(0 if success else 1)
