"""
End-to-end pipeline for scraping images and generating captions.
"""

from typing import List, Dict, Optional
from pathlib import Path
import logging

from src.scraper import WebScraper, ImageDownloader
from src.captioning import CaptionGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageCaptionPipeline:
    """
    Complete pipeline for scraping images and generating captions.
    
    This class orchestrates the entire workflow:
    1. Scrape images from URL
    2. Download images
    3. Generate captions
    4. Return structured results
    """
    
    def __init__(
        self,
        model_name: str = "Salesforce/blip2-opt-2.7b",
        min_image_size: int = 200,
        timeout: int = 10
    ):
        """
        Initialize pipeline with all components.
        
        Args:
            model_name: BLIP-2 model identifier
            min_image_size: Minimum image dimension
            timeout: Request timeout in seconds
        """
        logger.info("Initializing ImageCaptionPipeline...")
        
        self.scraper = WebScraper(timeout=timeout)
        self.downloader = ImageDownloader(timeout=timeout)
        self.generator = CaptionGenerator(model_name=model_name)
        self.min_image_size = min_image_size
        
        logger.info("Pipeline initialized successfully!")
    
    def process_url(
        self,
        url: str,
        prompt: Optional[str] = None,
        max_images: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Process all images from a URL.
        
        Args:
            url: URL to scrape
            prompt: Optional caption prompt
            max_images: Maximum number of images to process
            
        Returns:
            Dictionary containing:
            {
                'url': str,
                'title': str,
                'total_images_found': int,
                'images_processed': int,
                'results': [
                    {
                        'image_url': str,
                        'caption': str,
                        'alt': str,
                        'width': int,
                        'height': int,
                        'index': int
                    },
                    ...
                ],
                'errors': [...]
            }
        """
        logger.info(f"Processing URL: {url}")
        
        # 1. Get page title
        page_title = self.scraper.get_page_title(url)
        
        # 2. Scrape images
        images = self.scraper.scrape_images(url)
        logger.info(f"Found {len(images)} images")
        
        # Limit if specified
        if max_images:
            images = images[:max_images]
        
        # 3. Process each image
        results = []
        errors = []
        
        for idx, img_data in enumerate(images, start=1):
            logger.info(f"Processing image {idx}/{len(images)}")
            
            try:
                # Download image
                image = self.downloader.download_image(
                    img_data['url'],
                    min_size=self.min_image_size
                )
                
                if image is None:
                    logger.warning(f"Skipping image {idx}: Download failed or too small")
                    errors.append({
                        'index': idx,
                        'url': img_data['url'],
                        'error': 'Download failed or image too small'
                    })
                    continue
                
                # Generate caption
                caption = self.generator.model.generate_caption(
                    image,
                    prompt=prompt
                )
                
                # Store result
                result = {
                    'image_url': img_data['url'],
                    'caption': caption,
                    'alt': img_data.get('alt', ''),
                    'title': img_data.get('title', ''),
                    'width': image.size[0],
                    'height': image.size[1],
                    'index': idx
                }
                
                results.append(result)
                logger.info(f"✅ Image {idx}: {caption}")
                
            except Exception as e:
                logger.error(f"Error processing image {idx}: {str(e)}")
                errors.append({
                    'index': idx,
                    'url': img_data.get('url', 'unknown'),
                    'error': str(e)
                })
        
        # 4. Return summary
        summary = {
            'url': url,
            'title': page_title,
            'total_images_found': len(images),
            'images_processed': len(results),
            'images_failed': len(errors),
            'results': results,
            'errors': errors
        }
        
        logger.info(f"Pipeline complete: {len(results)}/{len(images)} images processed")
        
        return summary
    
    def process_article(
        self,
        url: str,
        prompt: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Process images specifically from article content.
        
        Args:
            url: Article URL
            prompt: Optional caption prompt
            
        Returns:
            Same format as process_url()
        """
        logger.info(f"Processing article: {url}")
        
        # Get page title
        page_title = self.scraper.get_page_title(url)
        
        # Scrape article images
        images = self.scraper.scrape_article_images(url)
        logger.info(f"Found {len(images)} article images")
        
        # Process images
        results = []
        errors = []
        
        for idx, img_data in enumerate(images, start=1):
            try:
                # Download
                image = self.downloader.download_image(img_data['url'])
                
                if image is None:
                    errors.append({
                        'index': idx,
                        'url': img_data['url'],
                        'error': 'Download failed'
                    })
                    continue
                
                # Generate caption
                caption = self.generator.model.generate_caption(
                    image,
                    prompt=prompt
                )
                
                # Store with article-specific data
                result = {
                    'image_url': img_data['url'],
                    'caption': caption,
                    'original_caption': img_data.get('caption', ''),
                    'alt': img_data.get('alt', ''),
                    'width': image.size[0],
                    'height': image.size[1],
                    'index': idx
                }
                
                results.append(result)
                
            except Exception as e:
                errors.append({
                    'index': idx,
                    'url': img_data.get('url', 'unknown'),
                    'error': str(e)
                })
        
        return {
            'url': url,
            'title': page_title,
            'total_images_found': len(images),
            'images_processed': len(results),
            'images_failed': len(errors),
            'results': results,
            'errors': errors
        }
    
    def process_image_file(
        self,
        image_path: str,
        prompt: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Process a single local image file.
        
        Args:
            image_path: Path to image file
            prompt: Optional caption prompt
            
        Returns:
            Dictionary with image_path and caption
        """
        logger.info(f"Processing local image: {image_path}")
        
        result = self.generator.caption_single(image_path, prompt=prompt)
        
        return result
    
    def process_image_batch(
        self,
        image_paths: List[str],
        prompt: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Process multiple local image files.
        
        Args:
            image_paths: List of image file paths
            prompt: Optional caption prompt
            
        Returns:
            List of results
        """
        logger.info(f"Processing {len(image_paths)} local images")
        
        results = self.generator.caption_batch(image_paths, prompt=prompt)
        
        return results