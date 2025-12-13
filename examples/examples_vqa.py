"""
Example 2: Visual Question Answering (VQA)

This example demonstrates how to use custom prompts
to ask questions about images and get answers.
"""

from src.captioning import CaptionGenerator
from pathlib import Path


def main():
    """Run VQA example."""
    
    print("=" * 60)
    print("Example 2: Visual Question Answering (VQA)")
    print("=" * 60)
    
    # Initialize generator
    print("\n⏳ Loading BLIP-2 model...")
    generator = CaptionGenerator()
    print("✅ Model loaded successfully!")
    
    # Example image
    image_path = "examples/sample_images/cat.jpg"
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"\n⚠️  Image not found: {image_path}")
        print("Please provide a valid image path.")
        return
    
    print(f"\n📸 Image: {image_path}")
    
    # Define questions
    questions = [
        "Question: how many cats are there? Answer:",
        "Question: what color is the cat? Answer:",
        "Question: where is the cat sitting? Answer:",
        "Question: what is the cat doing? Answer:",
    ]
    
    # Ask questions
    print("\n" + "=" * 60)
    print("Asking questions about the image:")
    print("=" * 60)
    
    for idx, question in enumerate(questions, start=1):
        print(f"\n[{idx}/{len(questions)}] {question}")
        
        result = generator.caption_single(
            image_path,
            prompt=question
        )
        
        print(f"     Answer: {result['caption']}")
    
    # Example: Custom question
    print("\n" + "=" * 60)
    print("Custom Question Example:")
    print("=" * 60)
    
    custom_question = "Question: describe this image in detail. Answer:"
    print(f"\n{custom_question}")
    
    result = generator.caption_single(
        image_path,
        prompt=custom_question
    )
    
    print(f"Answer: {result['caption']}")
    
    print("\n" + "=" * 60)
    print("VQA Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    """
    Usage:
        python examples/example_vqa.py
    
    Expected output:
        Question: how many cats are there? Answer:
        Answer: two
        
        Question: what color is the cat? Answer:
        Answer: orange and white
    """
    main()