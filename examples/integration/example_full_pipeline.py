"""
Example: Full Pipeline - Scrape → Caption → Export

This example demonstrates the complete workflow from
scraping images to generating captions to exporting results.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline import ImageCaptionPipeline, CaptionExporter


def main():
    """Run full pipeline example."""
    
    print("=" * 70)
    print("Full Pipeline Example: Scrape → Caption → Export")
    print("=" * 70)
    
    # Initialize pipeline
    print("\n⏳ Initializing pipeline...")
    pipeline = ImageCaptionPipeline()
    print("✅ Pipeline ready!")
    
    # Target URL
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    print(f"\n📡 Processing URL: {url}")
    print("⏳ This may take a few minutes...")
    
    # Process (limit to 5 images for demo)
    results = pipeline.process_url(url, max_images=5)
    
    # Display summary
    print("\n" + "=" * 70)
    print("Processing Complete!")
    print("=" * 70)
    print(f"📄 Article: {results['title']}")
    print(f"🔍 Images found: {results['total_images_found']}")
    print(f"✅ Successfully processed: {results['images_processed']}")
    print(f"❌ Failed: {results['images_failed']}")
    
    # Display captions
    print("\n" + "=" * 70)
    print("Generated Captions:")
    print("=" * 70)
    
    for result in results['results']:
        print(f"\n[{result['index']}] {result['image_url'][:60]}...")
        print(f"    📝 Caption: {result['caption']}")
        print(f"    📐 Size: {result['width']}x{result['height']}")
    
    # Export results
    print("\n" + "=" * 70)
    print("Exporting Results...")
    print("=" * 70)
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    exporter = CaptionExporter()
    
    # Export to JSON
    exporter.to_json(results, "output/captions.json")
    print("✅ Exported: output/captions.json")
    
    # Export to CSV
    exporter.to_csv(results, "output/captions.csv")
    print("✅ Exported: output/captions.csv")
    
    # Export to HTML
    exporter.to_html(results, "output/captions.html")
    print("✅ Exported: output/captions.html")
    
    # Export to Markdown
    exporter.to_markdown(results, "output/captions.md")
    print("✅ Exported: output/captions.md")
    
    print("\n" + "=" * 70)
    print("✅ Pipeline Complete!")
    print("=" * 70)
    print("\n💡 Check the 'output/' folder for results")
    print("🌐 Open 'output/captions.html' in your browser to view")


if __name__ == "__main__":
    main()