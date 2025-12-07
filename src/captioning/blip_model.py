"""
BLIP-2 Model wrapper for image captioning.
"""

from transformers import AutoProcessor, Blip2ForConditionalGeneration
from PIL import Image
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BLIP2Model:
    """Wrapper class for BLIP-2 image captioning model."""
    
    def __init__(self, model_name: str = "Salesforce/blip2-opt-2.7b"):
        """
        Initialize BLIP-2 model and processor.
        
        Args:
            model_name: Hugging Face model identifier
                Options:
                - "Salesforce/blip2-opt-2.7b" (OPT-based, recommended)
                - "Salesforce/blip2-opt-6.7b" (larger, better quality)
                - "Salesforce/blip2-flan-t5-xl" (T5-based)
        """
        logger.info(f"Loading BLIP-2 model: {model_name}")
        
        # Use AutoProcessor (recommended for BLIP-2)
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        # Use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
        logger.info(f"Model loaded successfully on {self.device}")
    
    def generate_caption(
        self, 
        image: Image.Image, 
        prompt: str = None,
        max_length: int = 50
    ) -> str:
        """
        Generate caption for a single image.
        
        Args:
            image: PIL Image object
            prompt: Optional text prompt (e.g., "a photo of")
            max_length: Maximum length of generated caption
            
        Returns:
            Generated caption as string
        """
        try:
            # Preprocess image (and optional prompt)
            if prompt:
                inputs = self.processor(
                    images=image, 
                    text=prompt,
                    return_tensors="pt"
                ).to(self.device, torch.float16 if self.device == "cuda" else torch.float32)
            else:
                inputs = self.processor(
                    images=image,
                    return_tensors="pt"
                ).to(self.device, torch.float16 if self.device == "cuda" else torch.float32)
            
            # Generate caption
            generated_ids = self.model.generate(
                **inputs,
                max_length=max_length
            )
            
            # Decode caption
            caption = self.processor.batch_decode(
                generated_ids, 
                skip_special_tokens=True
            )[0].strip()
            
            logger.info(f"Generated caption: {caption}")
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            raise
    
    def generate_caption_from_path(
        self, 
        image_path: str, 
        prompt: str = None,
        max_length: int = 50
    ) -> str:
        """
        Generate caption from image file path.
        
        Args:
            image_path: Path to image file
            prompt: Optional text prompt
            max_length: Maximum length of generated caption
            
        Returns:
            Generated caption as string
        """
        try:
            image = Image.open(image_path).convert("RGB")
            return self.generate_caption(image, prompt, max_length)
        except Exception as e:
            logger.error(f"Error loading image from {image_path}: {str(e)}")
            raise