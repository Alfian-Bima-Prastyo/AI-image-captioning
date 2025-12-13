"""
Example 3: Detailed Descriptions & Batch Processing

This example demonstrates:
1. Generating detailed descriptions with custom prompts
2. Processing multiple images in batch
3. Handling errors gracefully
"""

from src.captioning import CaptionGenerator
from pathlib import Path
import json


def example_detailed_description():
    """Example of detailed image description."""
    
    print("=" * 60)
    print("Part 1: Detailed Image Descriptions")
    print("=" * 60)
    
    generator = CaptionGenerator()
    
    image_path = "examples/sample_images/news_photo.jpg"
    
    if not Path(image_path).exists():
        print(f"\n⚠️  Image not found: {image_path}")
        return
    
    # Different prompts for different styles
    prompts = {
        "Basic": None,  # No prompt
        "Detailed": "A detailed description of",
        "Professional": "A professional photo showing",
        "News Style": "This news photograph depicts",
    }
    
    print(f"\n📸 Image: {image_path}\n")
    
    for style, prompt in prompts.items():
        print(f"\n[{style}]")
        if prompt:
            print(f"Prompt: '{prompt}'")
        
        result = generator.caption_single(image_path, prompt=prompt)
        print(f"Caption: {result['caption']}")


def example_batch_processing():
    """Example of batch processing multiple images."""
    
    print("\n\n" + "=" * 60)
    print("Part 2: Batch Processing")
    print("=" * 60)
    
    generator = CaptionGenerator()
    
    # List of images to process
    image_paths = [
        "examples/sample_images/cat.jpg",
        "examples/sample_images/dog.jpg",
        "examples/sample_images/landscape.jpg",
    ]
    
    # Filter existing images
    existing_images = [p for p in image_paths if Path(p).exists()]
    
    if not existing_images:
        print("\n⚠️  No sample images found.")
        print("Please add images to examples/sample_images/")
        return
    
    print(f"\n📦 Processing {len(existing_images)} images...")
    
    # Process batch
    results = generator.caption_batch(existing_images)
    
    # Display results
    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)
    
    for idx, result in enumerate(results, start=1):
        print(f"\n[{idx}/{len(results)}] {result['image_path']}")
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Caption: {result['caption']}")
    
    # Save results to JSON
    output_file = "examples/batch_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")


def example_error_handling():
    """Example of handling errors."""
    
    print("\n\n" + "=" * 60)
    print("Part 3: Error Handling")
    print("=" * 60)
    
    generator = CaptionGenerator()
    
    # Test with non-existent file
    print("\n1️⃣ Testing with non-existent file...")
    result = generator.caption_single("nonexistent_image.jpg")
    
    if 'error' in result:
        print(f"✅ Error handled gracefully: {result['error']}")
    else:
        print(f"⚠️  Expected error but got: {result}")
    
    # Test batch with mixed valid/invalid files
    print("\n2️⃣ Testing batch with mixed files...")
    mixed_paths = [
        "examples/sample_images/cat.jpg",  # May or may not exist
        "nonexistent.jpg",  # Definitely doesn't exist
        "invalid_path.jpg",  # Also doesn't exist
    ]
    
    results = generator.caption_batch(mixed_paths)
    
    success_count = sum(1 for r in results if 'error' not in r)
    error_count = sum(1 for r in results if 'error' in r)
    
    print(f"\n✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total: {len(results)}")


def main():
    """Run all examples."""
    
    print("\n" + "🚀" * 30)
    print("Example 3: Detailed Descriptions & Batch Processing")
    print("🚀" * 30)
    
    # Run examples
    example_detailed_description()
    example_batch_processing()
    example_error_handling()
    
    print("\n\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)
    
    print("\n💡 Tips:")
    print("  - Use detailed prompts for better descriptions")
    print("  - Batch processing is efficient for multiple images")
    print("  - Always handle errors in production code")
    print("  - Results can be saved to JSON for later use")


if __name__ == "__main__":
    """
    Usage:
        python examples/example_detailed.py
    
    This will demonstrate:
    1. Different caption styles with various prompts
    2. Batch processing of multiple images
    3. Proper error handling
    """
    main()
