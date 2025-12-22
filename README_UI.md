# Gradio UI - User Guide

## Quick Start
```bash
# Launch the application
python app.py
```

Open browser to: http://127.0.0.1:7860

## Features

### 1. Single Image Captioning
- Upload any image (JPG, PNG, WebP)
- Optional: Add custom prompt for specific caption style
- Get instant caption

### 2. URL Scraping
- Paste any webpage URL
- Set maximum images to process
- System will:
  - Scrape all images
  - Download them
  - Generate captions
  - Export results

### 3. Batch Processing
- Upload multiple images at once
- Process all images with same prompt
- Download results as JSON

## Custom Prompts

### VQA (Visual Question Answering)
```
Question: how many cats are there? Answer:
Question: what color is the car? Answer:
```

### Detailed Descriptions
```
A detailed description of
A professional photo showing
This news photograph depicts
```

## Export Formats

- **JSON**: Structured data for API integration
- **CSV**: Spreadsheet format
- **HTML**: Visual preview with images
- **Markdown**: Documentation format

## Keyboard Shortcuts

- `Ctrl+Enter`: Submit in text fields
- `Ctrl+C`: Stop server

## Troubleshooting

### Port Already in Use
Change port in `app.py`:
```python
app.launch(server_port=7861)  # Use different port
```

### Model Loading Slow
First load downloads ~5GB model (one-time).
Subsequent loads are instant.

### Out of Memory
Use smaller model:
```python
CaptionGenerator("Salesforce/blip2-opt-2.7b")  # Default
# Or smaller:
CaptionGenerator("Salesforce/blip-image-captioning-base")  # ~500MB
```