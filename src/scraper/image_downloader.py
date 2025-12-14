"""
Image downloader for fetching images from URLs.
"""

import requests
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageDownloader:
    """Download and process images from URLs."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize image downloader.
        
        Args:
            timeout: Download timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def download_image(
        self, 
        url: str,
        min_size: int = 200
    ) -> Optional[Image.Image]:
        """
        Download image from URL and return PIL Image.
        
        Args:
            url: Image URL
            min_size: Minimum width*height (skip small images)
            
        Returns:
            PIL Image object or None if failed
        """
        try:
            logger.info(f"Downloading image: {url}")
            
            # Download image
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Open as PIL Image
            image = Image.open(BytesIO(response.content))
            
            # Check size
            width, height = image.size
            if width * height < min_size:
                logger.warning(f"Image too small: {width}x{height}")
                return None
            
            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            logger.info(f"Downloaded successfully: {width}x{height}")
            
            return image
            
        except requests.RequestException as e:
            logger.error(f"Download error: {str(e)}")
            return None
        except OSError as e:
            logger.error(f"Image processing error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None
    
    def download_and_save(
        self,
        url: str,
        output_path: str,
        max_size: Optional[Tuple[int, int]] = None
    ) -> bool:
        """
        Download image and save to file.
        
        Args:
            url: Image URL
            output_path: Output file path
            max_size: Optional (width, height) to resize
            
        Returns:
            True if successful
        """
        try:
            image = self.download_image(url)
            
            if image is None:
                return False
            
            # Resize if needed
            if max_size:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save
            image.save(output_path)
            logger.info(f"Saved to: {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Save error: {str(e)}")
            return False
    
    def get_image_info(self, url: str) -> Optional[dict[str, any]]:
        """
        Get image information without full download.
        
        Args:
            url: Image URL
            
        Returns:
            Dictionary with image info or None
        """
        try:
            response = requests.head(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            info = {
                "url": url,
                "content_type": response.headers.get("Content-Type", ""),
                "content_length": int(response.headers.get("Content-Length", 0)),
                "status_code": response.status_code
            }
            
            return info
            
        except Exception as e:
            logger.error(f"Info error: {str(e)}")
            return None
    
    def is_image_accessible(self, url: str) -> bool:
        """
        Check if image URL is accessible.
        
        Args:
            url: Image URL
            
        Returns:
            True if accessible
        """
        try:
            response = requests.head(url, headers=self.headers, timeout=self.timeout)
            return response.status_code == 200
        except:
            return False