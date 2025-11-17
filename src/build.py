#!/usr/bin/env python3
"""
Build script for Løvel website
Generates HTML pages from templates and data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from templates import (
    render_header, render_text_section, render_two_column_section,
    render_hero_section, render_navbar
)

# Configuration
SITE_ROOT = Path(__file__).parent.parent
SRC_DIR = SITE_ROOT / "src"
OUTPUT_DIR = SITE_ROOT
ASSET_DIR = SITE_ROOT / "assets"

# Load site data
with open(SRC_DIR / "site-data.json") as f:
    SITE_DATA = json.load(f)

# Utility functions
def get_root_path(page_path: str) -> str:
    """Get relative path to root from current page."""
    depth = page_path.count("/") + 1 if page_path else 0
    return "../" * depth if depth > 0 else ""

def render_section(section: dict, root_path: str) -> str:
    """
    Render a section using template functions.
    Dispatches to appropriate template based on section type.
    Supports both old HTML-embedded and new clean data formats.
    """
    section_type = section.get("type")
    is_collapsible = section.get("collapsible", False)
    section_id = section.get("id", "")
    
    if section_type == "header":
        return render_header(section.get('title', ''), is_collapsible, section_id)
    
    elif section_type == "text":
        return render_text_section(
            content=section.get('content'),
            title=section.get('title'),
            paragraphs=section.get('paragraphs'),
            bullets=section.get('bullets'),
            is_collapsible=is_collapsible,
            section_id=section_id
        )
    
    elif section_type == "content":
        layout = section.get("layout", "single")
        columns = section.get("columns", [])
        
        if layout == "two-col":
            return render_two_column_section(columns, root_path, is_collapsible, section_id)
        else:
            # Single column layout
            html = f"<div class='section'><div class='container'>"
            for col in columns:
                if col.get("type") == "text":
                    html += col.get("content", "")
            html += "</div></div>\n"
            return html
    
    return ""

def render_page(page_id: str, page_data: dict) -> str:
    """Render a complete HTML page."""
    # Handle home page path
    if page_id == "home":
        page_path = ""
    else:
        page_path = page_id
    
    root_path = get_root_path(page_path)
    
    # Determine if it's home page
    is_home = page_id == "home"
    
    # Fix asset paths for nested pages
    css_path = root_path + "assets/styles.css" if "/" in page_id else "assets/styles.css"
    
    # Build navigation dynamically
    nav_html = render_navbar(SITE_DATA['pages'], root_path, is_home)
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="index, follow">
    <meta name="description" content="{page_data.get('description', SITE_DATA['site']['description'])}">
    <title>{page_data.get('title', '')} - Løvel - lige i nærheden</title>
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" rel="stylesheet">
    <link href="{css_path}" rel="stylesheet">
</head>
<body>
    {nav_html}

    <main>
"""
    
    # Add hero section if present
    if is_home and "hero" in page_data:
        hero = page_data["hero"]
        html += f"""        <div class="hero" style="background-image: url('{root_path}{hero.get('image', '')}');">
            <div class="container">
                <h1>{hero.get('title', '')}</h1>
                <h3>{hero.get('subtitle', '')}</h3>
            </div>
        </div>
"""
    
    # Add sections
    for section in page_data.get("sections", []):
        html += render_section(section, root_path)
    
    # Footer with last updated date
    last_updated = datetime.now().strftime("%d. %B %Y")
    html += f"""    </main>

    <button id="scrollToTop" aria-label="Tilbage til toppen">↑</button>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <p><strong>Henvendelser vedr. hjemmesiden:</strong></p>
                    <p><a href="mailto:support@lovel.dk">support@lovel.dk</a></p>
                </div>
                <div class="footer-section">
                    <p><strong>Sitemap</strong></p>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li><a href="{root_path}index.html">Forside</a></li>
                        <li><a href="{root_path}dagtilbud/vuggestue/">Dagtilbud</a></li>
                        <li><a href="{root_path}foreninger/luif/">Foreninger</a></li>
                        <li><a href="{root_path}informationer/placering/">Informationer</a></li>
                        <li><a href="{root_path}erhverv.html">Erhverv</a></li>
                        <li><a href="{root_path}film.html">Film</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <p>© 2025 | Løvel - lige i nærheden</p>
                    <p><small>Sidst opdateret: {last_updated}</small></p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Scroll to top button
        const scrollToTopBtn = document.getElementById('scrollToTop');
        
        window.addEventListener('scroll', function() {{
            if (window.pageYOffset > 300) {{
                scrollToTopBtn.classList.add('show');
            }} else {{
                scrollToTopBtn.classList.remove('show');
            }}
        }});
        
        scrollToTopBtn.addEventListener('click', function() {{
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }});

        // Mobile menu toggle
        const toggle = document.getElementById('navbar-toggle');
        const menu = document.getElementById('navbar-menu');
        
        if (toggle && menu) {{
            toggle.addEventListener('click', function() {{
                menu.classList.toggle('active');
            }});
        }}
        
        // Dropdown menus
        document.querySelectorAll('.dropdown').forEach(dropdown => {{
            const toggle = dropdown.querySelector('.dropdown-toggle');
            if (toggle) {{
                toggle.addEventListener('click', function(e) {{
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                }});
            }}
        }});

        // Collapsible sections
        document.querySelectorAll('.collapse-toggle').forEach(toggle => {{
            toggle.addEventListener('click', function() {{
                const header = this.closest('.collapsible-header');
                if (!header) return;
                
                const sectionId = header.getAttribute('data-section');
                if (!sectionId) return;
                
                // Toggle header itself
                header.classList.toggle('collapsed');
                this.setAttribute('aria-expanded', header.classList.contains('collapsed') ? 'true' : 'false');
                
                // Find and toggle ALL consecutive content sections with the same ID
                let nextElement = header.nextElementSibling;
                while (nextElement) {{
                    if (nextElement.classList.contains('collapsible-content') && 
                        nextElement.getAttribute('data-section') === sectionId) {{
                        nextElement.classList.toggle('collapsed');
                        nextElement = nextElement.nextElementSibling;
                    }} else if (nextElement.classList.contains('collapsible-header')) {{
                        // Stop when we hit the next header
                        break;
                    }} else {{
                        nextElement = nextElement.nextElementSibling;
                    }}
                }}
            }});

            // Handle keyboard Enter/Space
            toggle.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' || e.key === ' ') {{
                    e.preventDefault();
                    this.click();
                }}
            }});
        }});
    </script>
</body>
</html>"""
    
    return html

def build_site():
    """Build the entire site."""
    print("🏗️  Building Løvel website...")
    
    for page_id, page_data in SITE_DATA["pages"].items():
        # Handle index files
        if "/" in page_id:
            output_dir = OUTPUT_DIR / page_id
            output_file = output_dir / "index.html"
            output_dir.mkdir(parents=True, exist_ok=True)
        elif page_id == "home":
            output_file = OUTPUT_DIR / "index.html"
        else:
            output_file = OUTPUT_DIR / f"{page_id}.html"
        
        # Generate and write HTML
        html_content = render_page(page_id, page_data)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"  ✓ Generated {output_file.relative_to(SITE_ROOT)}")
    
    print("✅ Build complete!")

if __name__ == "__main__":
    build_site()
