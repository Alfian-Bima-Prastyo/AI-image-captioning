"""
Example: Web Scraping for Image Extraction

This example demonstrates how to scrape images from news websites
and prepare them for caption generation.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.scraper import WebScraper, ImageDownloader
from pathlib import Path


def example_basic_scraping():
    """Example 1: Basic image scraping."""
    
    print("=" * 60)
    print("Example 1: Basic Web Scraping")
    print("=" * 60)
    
    # Initialize scraper
    scraper = WebScraper()
    
    # Scrape images from Wikipedia
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    print(f"\n📡 Scraping images from: {url}")
    
    images = scraper.scrape_images(url)
    
    print(f"\n✅ Found {len(images)} images")
    
    # Display first 5
    print("\nFirst 5 images:")
    for idx, img in enumerate(images[:5], start=1):
        print(f"\n[{idx}] URL: {img['url'][:80]}...")
        print(f"    Alt: {img['alt'][:50] if img['alt'] else 'N/A'}")


def example_article_scraping():
    """Example 2: Article-specific scraping."""
    
    print("\n\n" + "=" * 60)
    print("Example 2: Article Content Scraping")
    print("=" * 60)
    
    scraper = WebScraper()
    
    url = "https://en.wikipedia.org/wiki/Machine_learning"
    
    print(f"\n📰 Scraping article images from: {url}")
    
    # Get page title
    title = scraper.get_page_title(url)
    print(f"📄 Article title: {title}")
    
    # Scrape article images
    images = scraper.scrape_article_images(url)
    
    print(f"\n✅ Found {len(images)} images in article content")


def example_download_images():
    """Example 3: Download images."""
    
    print("\n\n" + "=" * 60)
    print("Example 3: Download Images")
    print("=" * 60)
    
    scraper = WebScraper()
    downloader = ImageDownloader()
    
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    print(f"\n📡 Scraping: {url}")
    images = scraper.scrape_images(url)
    
    # Create output directory
    output_dir = Path("downloads")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n💾 Downloading first 3 images to {output_dir}/")
    
    for idx, img_data in enumerate(images[:3], start=1):
        print(f"\n[{idx}/3] Downloading...")
        
        image = downloader.download_image(img_data['url'])
        
        if image:
            output_path = output_dir / f"image_{idx}.jpg"
            image.save(output_path)
            print(f"✅ Saved: {output_path} ({image.size[0]}x{image.size[1]})")
        else:
            print(f"❌ Failed to download")


def main():
    """Run all examples."""
    
    print("\n" + "🌐" * 30)
    print("Web Scraping Examples")
    print("🌐" * 30)
    
    example_basic_scraping()
    example_article_scraping()
    example_download_images()
    
    print("\n\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()