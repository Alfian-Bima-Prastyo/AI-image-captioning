"""
Unit tests for BLIP-2 model wrapper.
"""

import pytest
from PIL import Image
import numpy as np
import torch
from src.captioning.blip_model import BLIP2Model


# ============================================
# Fixtures
# ============================================

@pytest.fixture
def blip2_model():
    """Fixture to create BLIP-2 model instance."""
    return BLIP2Model("Salesforce/blip2-opt-2.7b")


@pytest.fixture
def sample_image():
    """Fixture to create a simple test image."""
    # Create a simple red square image
    img_array = np.zeros((224, 224, 3), dtype=np.uint8)
    img_array[:, :] = [255, 0, 0]  # Red color
    return Image.fromarray(img_array)


@pytest.fixture
def sample_image_path(tmp_path, sample_image):
    """Fixture to create a temporary image file."""
    image_path = tmp_path / "test_image.jpg"
    sample_image.save(image_path)
    return str(image_path)


# # ============================================
# # Initialization Tests
# # ============================================

# def test_model_initialization(blip2_model):
#     """Test that model initializes correctly."""
#     assert blip2_model is not None
#     assert blip2_model.processor is not None
#     assert blip2_model.model is not None
#     assert blip2_model.device in ["cuda", "cpu"]


# def test_model_device_selection():
#     """Test that device is selected correctly."""
#     model = BLIP2Model()
    
#     if torch.cuda.is_available():
#         assert model.device == "cuda"
#     else:
#         assert model.device == "cpu"


# ============================================
# Caption Generation Tests
# ============================================

def test_generate_caption(blip2_model, sample_image):
    """Test caption generation with a sample image."""
    caption = blip2_model.generate_caption(sample_image)
    
    assert caption is not None
    assert isinstance(caption, str)
    assert len(caption) > 0


# def test_generate_caption_from_path(blip2_model, sample_image_path):
#     """Test caption generation from image file path."""
#     caption = blip2_model.generate_caption_from_path(sample_image_path)
    
#     assert caption is not None
#     assert isinstance(caption, str)
#     assert len(caption) > 0


# def test_generate_caption_with_prompt(blip2_model, sample_image):
#     """Test caption generation with custom prompt."""
#     prompt = "Question: what color is this? Answer:"
#     caption = blip2_model.generate_caption(sample_image, prompt=prompt)
    
#     assert caption is not None
#     assert isinstance(caption, str)
#     assert len(caption) > 0


# def test_generate_caption_max_length(blip2_model, sample_image):
#     """Test caption generation with max_length parameter."""
#     caption_short = blip2_model.generate_caption(sample_image, max_length=10)
#     caption_long = blip2_model.generate_caption(sample_image, max_length=50)
    
#     assert caption_short is not None
#     assert caption_long is not None
#     assert isinstance(caption_short, str)
#     assert isinstance(caption_long, str)


# ============================================
# Error Handling Tests
# ============================================

# def test_generate_caption_invalid_image():
#     """Test that invalid image raises appropriate error."""
#     model = BLIP2Model()
    
#     with pytest.raises(Exception):
       
#         model.generate_caption("not_an_image")


# def test_generate_caption_from_nonexistent_path():
#     """Test that nonexistent file path raises error."""
#     model = BLIP2Model()
    
#     with pytest.raises(Exception):
#         model.generate_caption_from_path("nonexistent_file.jpg")


# def test_generate_caption_with_invalid_max_length(blip2_model, sample_image):
#     """Test caption generation with invalid max_length."""
   
#     with pytest.raises((ValueError, TypeError)):
#         blip2_model.generate_caption(sample_image, max_length=-1)


# ============================================
# Integration Tests
# ============================================

# def test_multiple_caption_generations(blip2_model, sample_image):
#     """Test generating multiple captions sequentially."""
#     captions = []
    
#     for _ in range(3):
#         caption = blip2_model.generate_caption(sample_image)
#         captions.append(caption)
    
#     assert len(captions) == 3
#     assert all(isinstance(c, str) for c in captions)
#     assert all(len(c) > 0 for c in captions)


# def test_different_prompts_different_outputs(blip2_model, sample_image):
#     """Test that different prompts produce different outputs."""
#     caption1 = blip2_model.generate_caption(sample_image)
#     caption2 = blip2_model.generate_caption(
#         sample_image, 
#         prompt="Describe this in detail:"
#     )
    
#     assert caption1 is not None
#     assert caption2 is not None
    # Note: Outputs might be similar but test ensures both work


# ============================================
# Performance Tests (Optional)
# ============================================

# @pytest.mark.slow
# def test_caption_generation_speed(blip2_model, sample_image):
#     """Test that caption generation completes in reasonable time."""
#     import time
    
#     start = time.time()
#     caption = blip2_model.generate_caption(sample_image)
#     duration = time.time() - start
    
    
#     assert duration < 30
#     assert caption is not None