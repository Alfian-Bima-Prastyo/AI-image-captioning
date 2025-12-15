"""
Export caption results to various formats (JSON, CSV, HTML).
"""

import json
import csv
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CaptionExporter:
    """Export caption results to different formats."""
    
    @staticmethod
    def to_json(
        data: Dict,
        output_path: str,
        indent: int = 2
    ) -> None:
        """
        Export results to JSON file.
        
        Args:
            data: Pipeline results dictionary
            output_path: Output file path
            indent: JSON indentation
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        logger.info(f"Exported to JSON: {output_path}")
    
    @staticmethod
    def to_csv(
        data: Dict,
        output_path: str
    ) -> None:
        """
        Export results to CSV file.
        
        Args:
            data: Pipeline results dictionary
            output_path: Output file path
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Index',
                'Image URL',
                'Caption',
                'Alt Text',
                'Width',
                'Height'
            ])
            
            # Data
            for result in data.get('results', []):
                writer.writerow([
                    result.get('index', ''),
                    result.get('image_url', ''),
                    result.get('caption', ''),
                    result.get('alt', ''),
                    result.get('width', ''),
                    result.get('height', '')
                ])
        
        logger.info(f"Exported to CSV: {output_path}")
    
    @staticmethod
    def to_html(
        data: Dict,
        output_path: str,
        template: str = "default"
    ) -> None:
        """
        Export results to HTML file with images and captions.
        
        Args:
            data: Pipeline results dictionary
            output_path: Output file path
            template: HTML template style
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate HTML
        html = CaptionExporter._generate_html(data, template)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"Exported to HTML: {output_path}")
    
    @staticmethod
    def _generate_html(data: Dict, template: str) -> str:
        """Generate HTML content."""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Captions - {data.get('title', 'Untitled')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .header .meta {{
            color: #666;
            font-size: 14px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .image-card {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .image-card img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
        }}
        .image-card .content {{
            padding: 20px;
        }}
        .image-card .caption {{
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.5;
        }}
        .image-card .meta {{
            font-size: 12px;
            color: #999;
        }}
        .footer {{
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{data.get('title', 'Image Captions')}</h1>
        <div class="meta">
            <strong>Source:</strong> {data.get('url', 'N/A')}<br>
            <strong>Generated:</strong> {timestamp}
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="number">{data.get('total_images_found', 0)}</div>
            <div class="label">Images Found</div>
        </div>
        <div class="stat-card">
            <div class="number">{data.get('images_processed', 0)}</div>
            <div class="label">Successfully Processed</div>
        </div>
        <div class="stat-card">
            <div class="number">{data.get('images_failed', 0)}</div>
            <div class="label">Failed</div>
        </div>
    </div>
    
    <div class="image-grid">
"""
        
        # Add images
        for result in data.get('results', []):
            html += f"""
        <div class="image-card">
            <img src="{result.get('image_url', '')}" alt="{result.get('caption', '')}" loading="lazy">
            <div class="content">
                <div class="caption">{result.get('caption', 'No caption')}</div>
                <div class="meta">
                    {result.get('width', 0)} × {result.get('height', 0)} px
                    {' • ' + result.get('alt', '') if result.get('alt') else ''}
                </div>
            </div>
        </div>
"""
        
        html += """
    </div>
    
    <div class="footer">
        Generated by AI Image Captioning System
    </div>
</body>
</html>
"""
        
        return html
    
    @staticmethod
    def to_markdown(
        data: Dict,
        output_path: str
    ) -> None:
        """
        Export results to Markdown file.
        
        Args:
            data: Pipeline results dictionary
            output_path: Output file path
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        md = f"""# {data.get('title', 'Image Captions')}

**Source:** {data.get('url', 'N/A')}  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Images Found:** {data.get('total_images_found', 0)}
- **Successfully Processed:** {data.get('images_processed', 0)}
- **Failed:** {data.get('images_failed', 0)}

## Captions

"""
        
        for result in data.get('results', []):
            md += f"""
### Image {result.get('index', 0)}

![{result.get('caption', '')}]({result.get('image_url', '')})

**Caption:** {result.get('caption', 'No caption')}  
**Dimensions:** {result.get('width', 0)} × {result.get('height', 0)} px  
**Alt Text:** {result.get('alt', 'N/A')}

---

"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        logger.info(f"Exported to Markdown: {output_path}")