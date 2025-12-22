"""
Launch script for AI Image Captioning Gradio UI.

Usage:
    python app.py

Then open browser to: http://127.0.0.1:7860
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.ui.gradio_app import create_app


def main():
    """Launch Gradio application."""
    
    print("=" * 60)
    print("🚀 AI Image Captioning System")
    print("=" * 60)
    print("\n⏳ Loading models and initializing interface...")
    
    # Create app
    app = create_app()
    
    print("✅ Ready!")
    print("\n🌐 Opening in browser...")
    print("   URL: http://127.0.0.1:7860")
    print("\n💡 Press Ctrl+C to stop\n")
    
    # Launch
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,  # Set True to create public link
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    main()