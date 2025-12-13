"""
Example 1: Basic Image Captioning

This example demonstrates the simplest way to generate
captions for images using the convenience function.
"""
import sys
import os
# Menambahkan folder 'src' ke dalam sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


# from src.captioning import generate_caption
from captioning.caption_generator import generate_caption

# from src.captioning.caption_generator import generate_caption
from pathlib import Path


def main():
    """Run basic captioning example."""
    
    print("=" * 60)
    print("Example 1: Basic Image Captioning")
    print("=" * 60)
    
    # Example image path (replace with your image)
    image_path = "examples\sample.jpg"
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"\n⚠️  Image not found: {image_path}")
        print("Please provide a valid image path.")
        
        # Create dummy example
        print("\nUsing dummy example...")
        image_path = "sample.jpg"
        print(f"\nUsage:")
        print(f"caption = generate_caption('{image_path}')")
        print(f"print(caption)")
        return
    
    # Generate caption
    print(f"\n📸 Processing image: {image_path}")
    print("⏳ Generating caption...")
    
    caption = generate_caption(image_path)
    
    # Display result
    print(f"\n✅ Caption: {caption}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    """
    Usage:
        python examples/example_basic.py
    
    Expected output:
        Caption: "a cat sitting on a couch"
    """
    main()