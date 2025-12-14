"""
Web scraper for extracting images from news articles and websites.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Web scraper for extracting images from web pages."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize web scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def scrape_images(
        self, 
        url: str, 
        min_width: int = 200,
        min_height: int = 200
    ) -> List[Dict[str, str]]:
        """
        Scrape all images from a given URL.
        
        Args:
            url: URL of the webpage to scrape
            min_width: Minimum image width to include
            min_height: Minimum image height to include
            
        Returns:
            List of dictionaries containing image metadata:
            [
                {
                    'url': 'https://example.com/image.jpg',
                    'alt': 'Image description',
                    'title': 'Image title',
                    'width': '800',
                    'height': '600'
                },
                ...
            ]
        """
        logger.info(f"Scraping images from: {url}")
        
        try:
            # Fetch webpage
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            logger.info(f"Status: {response.status_code}, HTML size: {len(response.text)} bytes")
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find all image elements
            img_elements = soup.find_all("img")
            logger.info(f"Found {len(img_elements)} <img> tags")
            
            images = []
            
            for idx, img in enumerate(img_elements, start=1):
                # Extract image URL
                img_url = self._extract_image_url(img, url)
                
                if not img_url:
                    continue
                
                # Skip SVG files
                if self._is_svg(img_url):
                    logger.debug(f"Skipping SVG: {img_url}")
                    continue
                
                # Skip data URIs
                if img_url.startswith("data:"):
                    logger.debug(f"Skipping data URI")
                    continue
                
                # Extract metadata
                image_data = {
                    "url": img_url,
                    "alt": img.get("alt", ""),
                    "title": img.get("title", ""),
                    "width": img.get("width", ""),
                    "height": img.get("height", ""),
                    "index": idx
                }
                
                images.append(image_data)
            
            logger.info(f"Extracted {len(images)} valid image URLs")
            
            return images
            
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error parsing HTML: {str(e)}")
            raise
    
    def _extract_image_url(self, img_element, base_url: str) -> Optional[str]:
        """
        Extract image URL from img element.
        
        Args:
            img_element: BeautifulSoup img element
            base_url: Base URL for resolving relative URLs
            
        Returns:
            Absolute image URL or None
        """
        # Try different attributes
        img_url = img_element.get("src") or img_element.get("data-src")
        
        # Try srcset if src not found
        if not img_url and img_element.has_attr("srcset"):
            srcset = img_element["srcset"]
            # Get first URL from srcset
            img_url = srcset.split()[0].split(",")[0]
        
        if not img_url:
            return None
        
        # Convert relative URLs to absolute
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        elif img_url.startswith("/"):
            img_url = urljoin(base_url, img_url)
        elif not img_url.startswith("http"):
            img_url = urljoin(base_url, img_url)
        
        return img_url
    
    def _is_svg(self, url: str) -> bool:
        """
        Check if URL points to an SVG file.
        
        Args:
            url: Image URL
            
        Returns:
            True if SVG, False otherwise
        """
        return url.lower().endswith(".svg") or ".svg" in url.lower()
    
    def scrape_article_images(
        self, 
        url: str,
        content_selectors: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """
        Scrape images specifically from article content area.
        
        Args:
            url: Article URL
            content_selectors: CSS selectors for article content area
            
        Returns:
            List of image metadata dictionaries
        """
        if content_selectors is None:
            # Common article content selectors
            content_selectors = [
                "article",
                ".article-content",
                ".post-content",
                ".entry-content",
                "#content",
                "main"
            ]
        
        logger.info(f"Scraping article images from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Try to find article content
            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    logger.info(f"Found article content with selector: {selector}")
                    break
            
            # If no content found, use entire page
            if not content:
                logger.warning("No article content found, using entire page")
                content = soup
            
            # Find images in content
            img_elements = content.find_all("img")
            logger.info(f"Found {len(img_elements)} images in article")
            
            images = []
            
            for idx, img in enumerate(img_elements, start=1):
                img_url = self._extract_image_url(img, url)
                
                if not img_url or self._is_svg(img_url) or img_url.startswith("data:"):
                    continue
                
                image_data = {
                    "url": img_url,
                    "alt": img.get("alt", ""),
                    "title": img.get("title", ""),
                    "caption": self._extract_caption(img),
                    "index": idx
                }
                
                images.append(image_data)
            
            logger.info(f"Extracted {len(images)} article images")
            
            return images
            
        except Exception as e:
            logger.error(f"Error scraping article: {str(e)}")
            raise
    
    def _extract_caption(self, img_element) -> str:
        """
        Try to extract image caption from nearby elements.
        
        Args:
            img_element: BeautifulSoup img element
            
        Returns:
            Caption text or empty string
        """
        # Check for figcaption
        parent = img_element.parent
        if parent and parent.name == "figure":
            figcaption = parent.find("figcaption")
            if figcaption:
                return figcaption.get_text(strip=True)
        
        # Check for caption in sibling elements
        next_sibling = img_element.find_next_sibling()
        if next_sibling and next_sibling.name in ["p", "div", "span"]:
            if "caption" in next_sibling.get("class", []):
                return next_sibling.get_text(strip=True)
        
        return ""
    
    def get_page_title(self, url: str) -> str:
        """
        Extract page title from URL.
        
        Args:
            url: Page URL
            
        Returns:
            Page title
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("title")
            
            return title.get_text(strip=True) if title else ""
            
        except Exception as e:
            logger.error(f"Error getting page title: {str(e)}")
            return ""
    
    def is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid and accessible.
        
        Args:
            url: URL to check
            
        Returns:
            True if valid and accessible
        """
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            
            response = requests.head(url, headers=self.headers, timeout=self.timeout)
            return response.status_code == 200
            
        except:
            return False