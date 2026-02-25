#!/usr/bin/env python3
"""
Build orchestration - coordinates data, logic, and HTML generation.

ARCHITECTURE LAYERS:
  1. page_builder.py   → Pure logic (paths, metadata, dates)
  2. html_generator.py → HTML rendering from metadata  
  3. build.py (this)   → Orchestration and file I/O

Data flow: JSON → page_builder (logic) → metadata dict → html_generator (render) → file I/O
"""

import json
from pathlib import Path

# Import logic layer
from page_builder import build_page_metadata, get_output_file

# Import rendering layer
from html_generator import render_complete_page

# Configuration
SITE_ROOT = Path(__file__).parent.parent
SRC_DIR = SITE_ROOT / "src"
OUTPUT_DIR = SITE_ROOT

# Load site data once
with open(SRC_DIR / "site-data.json", encoding="utf-8") as f:
    SITE_DATA = json.load(f)


def build_site():
    """
    Build entire site by orchestrating the three layers:
    
    For each page:
      1. Load page data from SITE_DATA
      2. Call page_builder.build_page_metadata() → get pure logic metadata dict
      3. Call html_generator.render_complete_page() → get HTML string
      4. Write to file
    """
    print("🏗️  Building Løvel website...")
    
    pages = SITE_DATA["pages"]
    
    for page_id, page_data in pages.items():
        # LOGIC LAYER: Build metadata (pure logic, no HTML)
        metadata = build_page_metadata(page_id, page_data, SITE_DATA)
        
        # RENDERING LAYER: Generate HTML from metadata
        html_content = render_complete_page(metadata, pages)
        
        # FILE I/O LAYER: Determine output path and write
        output_file = get_output_file(page_id, OUTPUT_DIR)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"  ✓ Generated {output_file.relative_to(SITE_ROOT)}")
    
    print("✅ Build complete!")


if __name__ == "__main__":
    build_site()
