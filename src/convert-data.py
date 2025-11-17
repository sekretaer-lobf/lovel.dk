#!/usr/bin/env python3
"""
Convert old HTML-embedded site-data.json to new clean structure
This script transforms embedded HTML into semantic data structures
"""

import json
from pathlib import Path
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """Extract text and structure from HTML content"""
    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self.current_text = []
        self.in_tag = None
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        if tag in ['p', 'li']:
            if self.current_text:
                text = ''.join(self.current_text).strip()
                if text:
                    self.paragraphs.append(text)
                self.current_text = []
        elif tag == 'a':
            self.in_tag = ('a', dict(attrs))
            
    def handle_data(self, data):
        text = data.strip()
        if text:
            self.current_text.append(text)
            
    def handle_endtag(self, tag):
        if tag in ['p', 'li']:
            if self.current_text:
                text = ''.join(self.current_text).strip()
                if text:
                    self.paragraphs.append(text)
                self.current_text = []
        elif tag == 'a' and self.in_tag:
            text = ''.join(self.current_text).strip()
            if text and self.in_tag[0] == 'a':
                href = self.in_tag[1].get('href', '')
                self.links.append({'text': text, 'url': href})
            self.current_text = []
            self.in_tag = None

def extract_from_html(html_content: str):
    """Extract paragraphs and links from HTML"""
    if not html_content:
        return [], []
    
    extractor = TextExtractor()
    try:
        extractor.feed(html_content)
    except:
        pass
    
    # Finalize any pending text
    if extractor.current_text:
        text = ''.join(extractor.current_text).strip()
        if text:
            extractor.paragraphs.append(text)
    
    return extractor.paragraphs, extractor.links

def extract_title_from_html(html_content: str) -> str:
    """Extract first <h2> or <h3> as title"""
    match = re.search(r'<h[23]>(.*?)</h[23]>', html_content)
    if match:
        return match.group(1).strip()
    return ""

def convert_section(section: dict) -> dict:
    """Convert old section format to new format"""
    section_type = section.get("type")
    
    if section_type == "header":
        return {
            "type": "header",
            "title": section.get("title", ""),
            "id": section.get("id"),
            "collapsible": section.get("collapsible", False)
        }
    
    elif section_type == "text":
        html_content = section.get("content", "")
        paragraphs, links = extract_from_html(html_content)
        title = extract_title_from_html(html_content)
        
        new_section = {
            "type": "text",
            "paragraphs": paragraphs
        }
        if title:
            new_section["title"] = title
        if section.get("id"):
            new_section["id"] = section.get("id")
        if section.get("collapsible"):
            new_section["collapsible"] = True
            
        return new_section
    
    elif section_type == "content":
        layout = section.get("layout", "single")
        columns = section.get("columns", [])
        
        new_columns = []
        for col in columns:
            col_type = col.get("type")
            
            if col_type == "text":
                html_content = col.get("content", "")
                paragraphs, links = extract_from_html(html_content)
                title = extract_title_from_html(html_content)
                
                new_col = {
                    "type": "text",
                    "paragraphs": paragraphs
                }
                if title:
                    new_col["title"] = title
                if col.get("width"):
                    new_col["width"] = col.get("width")
                    
                new_columns.append(new_col)
            
            elif col_type == "image":
                new_columns.append({
                    "type": "image",
                    "src": col.get("src", ""),
                    "alt": col.get("alt", "")
                })
            
            elif col_type == "gallery":
                new_columns.append({
                    "type": "gallery",
                    "images": col.get("images", [])
                })
            
            elif col_type == "map":
                new_columns.append({
                    "type": "map",
                    "src": col.get("src", ""),
                    "alt": col.get("alt", "")
                })
        
        return {
            "type": "content",
            "layout": layout,
            "columns": new_columns,
            "collapsible": section.get("collapsible", False),
            "id": section.get("id")
        }
    
    return section

def convert_page(page: dict) -> dict:
    """Convert old page format to new format"""
    new_page = {
        "title": page.get("title", ""),
        "description": page.get("description", "")
    }
    
    if "hero" in page:
        new_page["hero"] = page["hero"]
    
    if "sections" in page:
        new_page["sections"] = [convert_section(s) for s in page.get("sections", [])]
    
    return new_page

def main():
    """Convert site-data.json"""
    site_root = Path(__file__).parent.parent
    old_file = site_root / "src" / "site-data.json"
    new_file = site_root / "src" / "site-data-converted.json"
    
    print("📝 Konverterer site-data.json...")
    
    with open(old_file) as f:
        old_data = json.load(f)
    
    new_data = {
        "site": old_data.get("site", {}),
        "pages": {}
    }
    
    for page_id, page_data in old_data.get("pages", {}).items():
        print(f"  Converting {page_id}...")
        new_data["pages"][page_id] = convert_page(page_data)
    
    with open(new_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Konverteret! Gemt som: {new_file}")
    print("\nNæste trin:")
    print("1. Gennemse site-data-converted.json")
    print("2. Hvis det ser godt ud: mv site-data-converted.json site-data.json")
    print("3. Kør: python3 src/build.py")

if __name__ == "__main__":
    main()
