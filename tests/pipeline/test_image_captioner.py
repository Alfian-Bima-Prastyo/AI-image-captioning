"""
Unit tests for ImageCaptionPipeline.
"""

import pytest
from src.pipeline import ImageCaptionPipeline


@pytest.fixture
def pipeline():
    """Fixture to create pipeline instance."""
    return ImageCaptionPipeline()


def test_pipeline_initialization(pipeline):
    """Test pipeline initializes correctly."""
    assert pipeline is not None
    assert pipeline.scraper is not None
    assert pipeline.downloader is not None
    assert pipeline.generator is not None


def test_process_url():
    """Test processing URL end-to-end."""
    pipeline = ImageCaptionPipeline()
    
    url = "https://en.wikipedia.org/wiki/Cat"
    
    result = pipeline.process_url(url, max_images=2)
    
    assert result is not None
    assert 'url' in result
    assert 'title' in result
    assert 'results' in result
    assert isinstance(result['results'], list)


def test_process_article():
    """Test processing article images."""
    pipeline = ImageCaptionPipeline()
    
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    result = pipeline.process_article(url)
    
    assert result is not None
    assert result['images_processed'] >= 0