"""
Example: News Article Processing

Process a real news article and generate accessibility-focused captions.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline import ImageCaptionPipeline, CaptionExporter


def main():
    """Process news article with accessibility focus."""
    
    print("=" * 70)
    print("News Article Processing Example")
    print("=" * 70)
    
    # Initialize
    pipeline = ImageCaptionPipeline()
    
    # Wikipedia article (simulating news article)
    url = "https://en.wikipedia.org/wiki/2024_Summer_Olympics"
    
    print(f"\n📰 Processing article: {url}")
    
    # Use detailed prompt for better descriptions
    prompt = "A detailed description of"
    
    results = pipeline.process_article(url)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📄 {results['title']}")
    print("=" * 70)
    print(f"✅ Processed: {results['images_processed']} images")
    
    # Show results
    for result in results['results'][:3]:  # First 3
        print(f"\n📸 Image {result['index']}")
        print(f"   Caption: {result['caption']}")
        if result.get('original_caption'):
            print(f"   Original: {result['original_caption']}")
    
    # Export for web use
    output_dir = Path("output/news")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    exporter = CaptionExporter()
    exporter.to_html(results, "output/news/article_captions.html")
    
    print(f"\n✅ Exported to: output/news/article_captions.html")
    print("🌐 Open in browser to see results with images")


if __name__ == "__main__":
    main()