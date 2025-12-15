"""
Pipeline module for end-to-end image captioning workflow.

This module integrates web scraping and caption generation
into a complete pipeline for processing news articles and websites.
"""

from .image_captioner import ImageCaptionPipeline
from .caption_exporter import CaptionExporter

__all__ = ["ImageCaptionPipeline", "CaptionExporter"]