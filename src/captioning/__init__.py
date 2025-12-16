"""
Image captioning module using BLIP-2 transformer model.
"""


from src.captioning.blip_model import BLIP2Model
from .caption_generator import CaptionGenerator, generate_caption

__all__ = ["BLIP2Model", "CaptionGenerator", "generate_caption"]
