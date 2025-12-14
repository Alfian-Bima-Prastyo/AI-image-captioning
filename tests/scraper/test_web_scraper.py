"""
Unit tests for web scraper.
"""

import pytest
from src.scraper.web_scraper import WebScraper
from src.scraper.image_downloader import ImageDownloader


# ============================================
# Fixtures
# ============================================

@pytest.fixture
def scraper():
    """Fixture to create scraper instance."""
    return WebScraper()


@pytest.fixture
def downloader():
    """Fixture to create downloader instance."""
    return ImageDownloader()


# ============================================
# WebScraper Tests
# ============================================

def test_scraper_initialization(scraper):
    """Test scraper initializes correctly."""
    assert scraper is not None
    assert scraper.timeout == 10
    assert "User-Agent" in scraper.headers


def test_scrape_images_wikipedia():
    """Test scraping images from Wikipedia."""
    scraper = WebScraper()
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    images = scraper.scrape_images(url)
    
    assert len(images) > 0
    assert all("url" in img for img in images)
    assert all(img["url"].startswith("http") for img in images)


def test_scrape_article_images():
    """Test scraping article-specific images."""
    scraper = WebScraper()
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    images = scraper.scrape_article_images(url)
    
    assert len(images) > 0
    assert all("url" in img for img in images)


def test_get_page_title(scraper):
    """Test extracting page title."""
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    title = scraper.get_page_title(url)
    
    assert title is not None
    assert len(title) > 0
    assert "Python" in title


def test_is_valid_url(scraper):
    """Test URL validation."""
    assert scraper.is_valid_url("https://www.wikipedia.org") == True
    assert scraper.is_valid_url("not-a-url") == False
    assert scraper.is_valid_url("") == False


def test_extract_image_url(scraper):
    """Test image URL extraction."""
    from bs4 import BeautifulSoup
    
    html = '<img src="/test.jpg" alt="Test">'
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img")
    
    base_url = "https://example.com"
    result = scraper._extract_image_url(img, base_url)
    
    assert result == "https://example.com/test.jpg"


def test_is_svg(scraper):
    """Test SVG detection."""
    assert scraper._is_svg("image.svg") == True
    assert scraper._is_svg("image.jpg") == False
    assert scraper._is_svg("path/to/image.SVG") == True


# ============================================
# ImageDownloader Tests
# ============================================

def test_downloader_initialization(downloader):
    """Test downloader initializes correctly."""
    assert downloader is not None
    assert downloader.timeout == 10


def test_download_image():
    """Test downloading an image."""
    downloader = ImageDownloader()
    
    # Wikipedia logo (reliable test image)
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Wikipedia-logo.png/200px-Wikipedia-logo.png"
    
    image = downloader.download_image(url)
    
    assert image is not None
    assert image.mode == "RGB"
    assert image.size[0] > 0
    assert image.size[1] > 0


def test_is_image_accessible(downloader):
    """Test checking image accessibility."""
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Wikipedia-logo.png/200px-Wikipedia-logo.png"
    
    assert downloader.is_image_accessible(url) == True
    assert downloader.is_image_accessible("https://invalid-url.com/fake.jpg") == False


def test_get_image_info(downloader):
    """Test getting image information."""
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Wikipedia-logo.png/200px-Wikipedia-logo.png"
    
    info = downloader.get_image_info(url)
    
    assert info is not None
    assert "url" in info
    assert "content_type" in info
    assert info["status_code"] == 200


# ============================================
# Error Handling Tests
# ============================================

def test_scrape_invalid_url(scraper):
    """Test scraping from invalid URL."""
    with pytest.raises(Exception):
        scraper.scrape_images("not-a-valid-url")


def test_download_invalid_image():
    """Test downloading invalid image."""
    downloader = ImageDownloader()
    
    image = downloader.download_image("https://invalid-url.com/fake.jpg")
    
    assert image is None