"""
Caption Generator Interface
"""

from typing import List, Dict, Optional
from PIL import Image
import logging
from .blip_model import BLIP2Model

logger=logging.getLogger(__name__)

class CaptionGenerator:
    """ 
    interface for caption generator wrapper
    """

    def __init__(
        self,
        model_name: str = "Salesforce/blip2-opt-2.7b",
        default_prompt: Optional[str] = None
    ):
        """
        Initialize caption generator.

        Args:
            model_name: BLIP-2 model identifier
            default_prompt: Default Prompt to use (e.g., "a photo of")
        """
        self.model=BLIP2Model(model_name)
        self.default_prompt=default_prompt

    def caption_single(
        self,
        image_path: str,
        prompt: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate caption for single image

        Args: 
            image_path : path to image
            prompt: Optional prompt (overrides default_prompt)

        retruns:
            A dictionary of image_path and generated caption
        """

        used_prompt = prompt or self.default_prompt
        caption = self.model.generate_caption_from_path(image_path, used_prompt)

        return{
            "image_path": image_path,
            "prompt": used_prompt,
            "caption": caption
        }

    def caption_batch(
        self,
        image_paths: List[str],
        prompt: Optional[str] = None
    ) -> List[Dict[str,str]]:
        """
        Generate captions for multiple images.
        
        Args:
            image_paths: List of image file paths
            prompt: Optional prompt for all images
            
        Returns:
            List of dictionaries with image paths and captions
        """
    
        results = []

        for idx, image_path in enumerate(image_path, start=1):
            logger.info(f"Processing image {idx}/ len{image_paths} : {image_path}")

            try:
                result = self.caption_single(image_path, prompt)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {image_path}: str{e}")
                results.append({
                    "image_path" : image_path,
                    "caption" : None,
                    "error" : str(e)
                })

        return results
    

    
# Convenience function for quick usage
def generate_caption(
    image_path: str, 
    prompt: Optional[str] = None
) -> str:
    """
    Quick function to generate caption for an image.
    
    Args:
        image_path: Path to image file
        prompt: Optional text prompt
        
    Returns:
        Generated caption
    """
    generator = CaptionGenerator()
    result = generator.caption_single(image_path, prompt)
    return result["caption"]





